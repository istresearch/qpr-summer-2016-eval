#!/usr/bin/env python

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
import sys
import json

# how to use: python CP1_eval_script.py ground_truth_sample_CP1.json submission_sample_CP1.json

################################################
# do not edit - eval data
gt_id = []
gt_phones = []
gt_scores = []
gt_outputs = open(sys.argv[1], "r")
for line in gt_outputs:
    entry = json.loads(line)
    gt_id.append(entry['cdr_id'])
    gt_phones.append(entry['phone'])
    gt_scores.append(entry['class'])
gt_outputs.close()
################################################

################################################
# group data ingest - edit to fit your data as needed
sub_id = []
sub_phones = []
sub_scores = []
sub_outputs = open(sys.argv[2], "r")
for line in sub_outputs:
    entry = json.loads(line)
    sub_phones.append(entry['phone'])
    sub_id.append(entry['cdr_id'])
    sub_scores.append(entry['score'])
sub_outputs.close()
################################################

################################################
# ids should be well-ordered, but just in case...
# note that if you did not include ids but instead only phone numbers in your file, the below needs modification
if any([a != b for a, b in zip(sub_id, gt_id)]):
    print 'submission ids do not match ground truth ids, please check submission data'   
################################################ 

else:
    fpr ,tpr, thresholds = roc_curve(gt_scores, sub_scores)
    auc = roc_auc_score(gt_scores, sub_scores)
    print 'ROC-AUC is:', auc
    print 'ROC curve plotting'
    plt.plot(fpr, tpr, '.-')
    plt.xlim(-0.01, 1.01)
    plt.ylim(-0.01, 1.01)
    plt.show()