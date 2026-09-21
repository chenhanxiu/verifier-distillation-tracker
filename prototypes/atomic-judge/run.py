"""CLI: split -> train -> calibrate -> evaluate/predict."""
import argparse
import hashlib
import json
import random
import time
from pathlib import Path
from data import load, dump, split, assert_disjoint, groups, LABELS
from metrics import softmax, fit_temperature, evaluate


def write_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2))


def manifest(rows):
    return {k:sorted({r[k] for r in rows}) for k in ['task_family_id','trajectory_id']}


def reject_overlap(rows, manifests):
    current = manifest(rows)
    for previous in manifests:
        for key in current:
            if set(current[key]) & set(previous[key]):
                raise ValueError(f'Cross-stage data leakage: {key}')


def checkpoint_id(folder):
    h = hashlib.sha256()
    for p in sorted(folder.rglob('*')):
        if p.is_file() and (p.name in ['config.json','head.pt'] or p.parent.name=='adapter'):
            h.update(str(p.relative_to(folder)).encode())
            with p.open('rb') as f:
                for chunk in iter(lambda:f.read(1024*1024),b''):
                    h.update(chunk)
    return h.hexdigest()


def infer(judge, tokenizer, rows, mode, max_length, batch_size, device):
    import torch
    from model import collate
    batches = groups(rows,mode)
    output, latencies = [], []
    judge.eval()
    with torch.inference_mode():
        for start in range(0,len(batches),batch_size):
            records = batches[start:start+batch_size]
            if device.startswith('cuda'):
                torch.cuda.synchronize()
            t = time.perf_counter()
            inputs,_ = collate(tokenizer,records,max_length,device)
            logits = judge(**inputs).float().cpu().tolist()
            latencies.append(time.perf_counter()-t)
            for b,rs in enumerate(records):
                for j,r in enumerate(rs):
                    output.append((r,logits[b][j]))
    timing = {'batch_latency_seconds':latencies,'criteria_per_second':len(rows)/sum(latencies),
              'note':'Tokenization + transfer + forward, excluding loading; includes cold first batch. Not serving P95.'}
    return output,timing


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command',required=True)
    s = sub.add_parser('split'); s.add_argument('--data',required=True); s.add_argument('--out',required=True); s.add_argument('--seed',type=int,default=42)
    t = sub.add_parser('train')
    for key in ['train','dev','base','out']:
        t.add_argument('--'+key,required=True)
    t.add_argument('--mode',choices=['single','multi'],default='single')
    t.add_argument('--epochs',type=int,default=3); t.add_argument('--lr',type=float,default=1e-4)
    t.add_argument('--rank',type=int,default=8); t.add_argument('--seed',type=int,default=42)
    t.add_argument('--max-length',type=int,default=4096)
    t.add_argument('--dtype',choices=['float32','bfloat16'],default='float32')
    for name in ['calibrate','evaluate','predict']:
        c = sub.add_parser(name)
        c.add_argument('--checkpoint',required=True); c.add_argument('--data',required=True); c.add_argument('--out',required=True)
        c.add_argument('--base',help='Override local base model path after moving machines')
        if name!='calibrate':
            c.add_argument('--calibration')
    for parser in [t,*[sub.choices[n] for n in ['calibrate','evaluate','predict']]]:
        parser.add_argument('--device',default='cpu'); parser.add_argument('--batch-size',type=int,default=1)
    args = p.parse_args()
    if args.command=='split':
        out = Path(args.out); out.mkdir(parents=True,exist_ok=False)
        for name,rows in split(load(args.data),args.seed).items():
            dump(out/(name+'.jsonl'),rows)
        return
    import torch
    from model import build, collate
    if args.batch_size<1:
        raise ValueError('batch-size must be positive')
    if args.command=='train':
        if args.epochs<1 or args.lr<=0 or args.rank<1:
            raise ValueError('epochs/lr/rank must be positive')
        train,dev = load(args.train),load(args.dev)
        assert_disjoint(train,dev)
        random.seed(args.seed); torch.manual_seed(args.seed)
        out = Path(args.out); out.mkdir(parents=True,exist_ok=False)
        judge,tok = build(args.base,rank=args.rank,dtype=args.dtype)
        judge.to(args.device)
        max_length = min(args.max_length,getattr(judge.backbone.config,'max_position_embeddings',args.max_length))
        config = {'base':str(Path(args.base).resolve()),'mode':args.mode,'max_length':max_length,
                  'dtype':args.dtype,'labels':LABELS,'seed':args.seed,'rank':args.rank,
                  'lr':args.lr,'epochs':args.epochs,'train_manifest':manifest(train),'dev_manifest':manifest(dev)}
        opt = torch.optim.AdamW([v for v in judge.parameters() if v.requires_grad],lr=args.lr)
        records = groups(train,args.mode)
        best = float('inf'); history=[]
        for epoch in range(args.epochs):
            random.shuffle(records); judge.train(); total=0; count=0
            for start in range(0,len(records),args.batch_size):
                inputs,y = collate(tok,records[start:start+args.batch_size],max_length,args.device)
                opt.zero_grad(set_to_none=True)
                z = judge(**inputs)
                loss = torch.nn.functional.cross_entropy(z.reshape(-1,3),y.reshape(-1),ignore_index=-100)
                loss.backward(); torch.nn.utils.clip_grad_norm_(judge.parameters(),1.0); opt.step()
                n = int((y!=-100).sum()); total+=loss.item()*n; count+=n
            results,_ = infer(judge,tok,dev,args.mode,max_length,args.batch_size,args.device)
            report = evaluate([softmax(z) for _,z in results],[LABELS.index(r['label']) for r,_ in results])
            history.append({'epoch':epoch+1,'train_loss':total/count,'dev':report})
            print(json.dumps(history[-1],ensure_ascii=False))
            if report['nll']<best:
                best=report['nll']; config['best_epoch']=epoch+1
                judge.backbone.save_pretrained(out/'adapter'); tok.save_pretrained(out)
                torch.save(judge.head.state_dict(),out/'head.pt'); write_json(out/'config.json',config)
        write_json(out/'history.json',history)
        return
    folder = Path(args.checkpoint); config=json.loads((folder/'config.json').read_text())
    if config['labels']!=LABELS:
        raise ValueError('Checkpoint label order mismatch')
    rows=load(args.data,labeled=args.command!='predict')
    calibration=None
    if getattr(args,'calibration',None):
        calibration=json.loads(Path(args.calibration).read_text())
        if calibration['checkpoint_id']!=checkpoint_id(folder):
            raise ValueError('Calibration belongs to a different checkpoint')
    if args.command!='predict':
        used=[config['train_manifest'],config['dev_manifest']]
        if calibration:
            used.append(calibration['manifest'])
        reject_overlap(rows,used)
    judge,tok=build(args.base or config['base'],checkpoint=folder,dtype=config['dtype']); judge.to(args.device)
    results,timing=infer(judge,tok,rows,config['mode'],config['max_length'],args.batch_size,args.device)
    zs=[z for _,z in results]
    if args.command=='calibrate':
        ys=[LABELS.index(r['label']) for r,_ in results]
        temperature=fit_temperature(zs,ys)
        write_json(args.out,{'temperature':temperature,'checkpoint_id':checkpoint_id(folder),'manifest':manifest(rows),
                            'before':evaluate([softmax(z) for z in zs],ys),'after':evaluate([softmax(z,temperature) for z in zs],ys),
                            'method':'Bounded log-grid NLL minimization, T in exp([-4,4])'})
        return
    temperature=calibration['temperature'] if calibration else 1.0
    probs=[softmax(z,temperature) for z in zs]
    if args.command=='evaluate':
        write_json(args.out,{'metrics':evaluate(probs,[LABELS.index(r['label']) for r,_ in results]),'timing':timing,'temperature':temperature})
    else:
        dump(args.out,[{'trajectory_id':r['trajectory_id'],'criterion_id':r['criterion_id'],
                       'prediction':LABELS[max(range(3),key=lambda k:prob[k])],
                       'probabilities':dict(zip(LABELS,prob)),'max_probability':max(prob),
                       'temperature':temperature,'calibrated':calibration is not None}
                      for (r,_),prob in zip(results,probs)])

if __name__=='__main__':
    main()
