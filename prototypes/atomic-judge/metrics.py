"""Dependency-free probability calibration and evaluation."""
import math


def softmax(z, temperature=1.0):
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError('Temperature must be finite and positive')
    if len(z) != 3 or any(not math.isfinite(v) for v in z):
        raise ValueError('Expected three finite logits')
    v = [x/temperature for x in z]
    m = max(v)
    e = [math.exp(x-m) for x in v]
    return [x/sum(e) for x in e]


def nll(probs, labels):
    return -sum(math.log(max(p[y], 1e-15)) for p,y in zip(probs,labels))/len(labels)


def fit_temperature(logits, labels):
    # Transparent bounded log-grid search; T=1 is included, so fitting cannot
    # worsen calibration-set NLL. This does not imply held-out improvement.
    candidates = [math.exp(-4 + i*0.02) for i in range(401)]
    return min(candidates, key=lambda t: nll([softmax(z,t) for z in logits], labels))


def evaluate(probs, labels):
    if not labels or len(probs) != len(labels):
        raise ValueError('Empty or mismatched predictions')
    pred = [max(range(3), key=lambda k:p[k]) for p in probs]
    cm = [[0]*3 for _ in range(3)]
    for y,h in zip(labels,pred):
        cm[y][h] += 1
    f1 = []
    for k in range(3):
        denom = sum(cm[k]) + sum(row[k] for row in cm)
        f1.append(2*cm[k][k]/denom if denom else 0.0)
    curve = []
    for threshold in [0, .5, .7, .8, .9, .95, .99]:
        selected = [i for i,p in enumerate(probs) if max(p)>=threshold and pred[i]!=2]
        curve.append({'threshold':threshold, 'coverage':len(selected)/len(labels),
                      'error_rate':sum(pred[i]!=labels[i] for i in selected)/len(selected) if selected else None})
    bins = []
    for b in range(10):
        ix = [i for i,p in enumerate(probs) if min(9,int(max(p)*10))==b]
        if ix:
            bins.append({'count':len(ix),'confidence':sum(max(probs[i]) for i in ix)/len(ix),
                         'accuracy':sum(pred[i]==labels[i] for i in ix)/len(ix)})
    return {'n':len(labels),'accuracy':sum(y==h for y,h in zip(labels,pred))/len(labels),
            'macro_f1':sum(f1)/3,'class_f1':f1,'confusion_true_by_pred':cm,
            'nll':nll(probs,labels),
            'brier':sum(sum((p[k]-int(y==k))**2 for k in range(3)) for p,y in zip(probs,labels))/len(labels),
            'ece_10_bins':sum(b['count']*abs(b['accuracy']-b['confidence']) for b in bins)/len(labels),
            'reliability_bins':bins,'coverage_risk':curve,
            'violation_miss_rate':1-cm[1][1]/sum(cm[1]) if sum(cm[1]) else None}
