import copy
import unittest
from data import load, split, assert_disjoint, encode, groups
from metrics import softmax, fit_temperature, evaluate, nll

class Tokenizer:
    def encode(self,s,add_special_tokens=True):
        return list(s.encode())

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.rows=load('examples/demo.jsonl')
    def test_split_and_leakage(self):
        parts=split(self.rows)
        assert_disjoint(*parts.values())
        with self.assertRaises(ValueError):
            assert_disjoint(parts['train'],parts['train'])
        self.assertEqual(sum(map(len,parts.values())),len(self.rows))
    def test_labels_never_enter_input(self):
        rows=groups(self.rows,'multi')[0]
        a=encode(Tokenizer(),rows,10000)
        other=copy.deepcopy(rows)
        for r in other:
            r['label']='insufficient_evidence'; r['evidence_refs']=['SECRET']; r['label_source']='SECRET'
        self.assertEqual(a,encode(Tokenizer(),other,10000))
        self.assertEqual(len(a[1]),2)
        with self.assertRaises(ValueError):
            encode(Tokenizer(),rows,3)
    def test_calibration(self):
        logits=[[10.,0.,0.]]*4; labels=[0,0,0,1]
        t=fit_temperature(logits,labels)
        self.assertGreater(t,1)
        self.assertLessEqual(nll([softmax(z,t) for z in logits],labels),nll([softmax(z) for z in logits],labels))
    def test_metrics_and_abstention(self):
        report=evaluate([[1,0,0],[0,1,0],[0,0,1]],[0,1,2])
        self.assertEqual(report['accuracy'],1)
        self.assertEqual(report['brier'],0)
        self.assertAlmostEqual(report['coverage_risk'][0]['coverage'],2/3)
        self.assertEqual(report['violation_miss_rate'],0)

if __name__=='__main__':
    unittest.main()
