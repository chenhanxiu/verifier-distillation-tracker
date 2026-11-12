"""Offline integration test using a random tiny Llama, not a useful judge."""
import os
import subprocess
import sys
from pathlib import Path
import torch
from transformers import LlamaConfig, LlamaModel, PreTrainedTokenizerFast
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Whitespace

root=Path(sys.argv[1] if len(sys.argv)>1 else 'runs/smoke')
root.mkdir(parents=True,exist_ok=False)
base=root/'base'
tokenizer=Tokenizer(WordLevel({'[UNK]':0,'[PAD]':1,'判断':2,'证据':3},unk_token='[UNK]'))
tokenizer.pre_tokenizer=Whitespace()
PreTrainedTokenizerFast(tokenizer_object=tokenizer,unk_token='[UNK]',pad_token='[PAD]').save_pretrained(base)
LlamaModel(LlamaConfig(vocab_size=4,hidden_size=32,intermediate_size=64,num_hidden_layers=1,
                      num_attention_heads=4,num_key_value_heads=2,max_position_embeddings=2048)).save_pretrained(base)

def run(*args):
    subprocess.run([sys.executable,'run.py',*map(str,args)],check=True)

run('split','--data','examples/demo.jsonl','--out',root/'split')
for mode in ['single','multi']:
    checkpoint=root/mode
    run('train','--base',base,'--train',root/'split/train.jsonl','--dev',root/'split/dev.jsonl',
        '--out',checkpoint,'--mode',mode,'--epochs',1,'--batch-size',3,'--max-length',2048)
    run('calibrate','--checkpoint',checkpoint,'--data',root/'split/calibration.jsonl','--out',root/f'{mode}-calibration.json')
    run('evaluate','--checkpoint',checkpoint,'--data',root/'split/test.jsonl','--calibration',root/f'{mode}-calibration.json','--out',root/f'{mode}-metrics.json')
    run('predict','--checkpoint',checkpoint,'--data',root/'split/test.jsonl','--calibration',root/f'{mode}-calibration.json','--out',root/f'{mode}-predictions.jsonl')
print('PASS: both modes trained, saved, loaded, calibrated, evaluated, and predicted offline.')
