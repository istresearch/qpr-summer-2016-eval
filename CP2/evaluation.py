#!/usr/bin/env python

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import precision_recall_curve, average_precision_score

import sys
import simplejson as json
import ftfy
import codecs
import os
import numpy as np

'''
Usage:
python evaluation.py <ground_truth_file> <submission_file_or_dir_of_submissions> <output_dir> <team_name>
Example: python evaluation.py 12_2_performer_gt.jl test.json ~/Desktop/CP2/results/J/ TeamJ

Will also write a metrics.txt file out.

'''

def saveROC(gt_scores, sub_scores, roc_name,f):
    fpr, tpr, thresholds = roc_curve(gt_scores, sub_scores)
    auc = roc_auc_score(gt_scores, sub_scores)

    fig = plt.figure()
    plt.step(fpr, tpr, '-')
    plt.xlim(-0.01, 1.01)
    plt.ylim(-0.01, 1.01)
    title = team + " " + roc_name + ' ROC-AUC = {0}'.format(auc)
    plt.title(title)
    plt.ylabel("True Positive Rate")
    plt.xlabel("False Positive Rate")

    # grab the input_file name
    head, tail = os.path.split(f)
    tail = tail.split(".")[0]
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    plt.savefig(output_path + "/" + team + "_" + tail + "_" + roc_name + ".pdf")

    # write out metrics to file for comparison
    metrics_out.write("\t".join(("ROC",team,tail,roc_name,str(auc))) + "\n")

def doROC(ground_truth_slice, roc_name,f):
    gt_id = []
    gt_scores = []

    sub_id = []
    sub_scores = []

    for entry in ground_truth_slice:
        gt_id.append(entry)
        sub_id.append(entry)
        
        gt_scores.append(ground_truth[entry])

        # Provide score if submission had one, else fill with 0
        if entry in submissions:
            sub_scores.append(submissions[entry])
        else:
            sub_scores.append(0)

    saveROC(gt_scores,sub_scores,roc_name,f)
        
# MAIN

ground_truth = {}
c_names = {}
d_names = {}

submissions = {}

gt_file = sys.argv[1]
submissions_file = sys.argv[2]
output_path = sys.argv[3]
team = sys.argv[4]

metrics_out = open("metrics.txt","a")

# Read in ground truth
print "** Loading Ground Truth **"
with codecs.open(gt_file, "r", encoding='utf8') as gt_outputs:
    for line in gt_outputs:
        line = unicode(line)
        entry = json.loads(line)

        c = ftfy.fix_text(entry["site_c"])
        d = ftfy.fix_text(entry["site_d"])

        # Create tuple with positive class
        ground_truth[(c,d)] = 1

        # Add unique name to each names set
        c_names[c] = entry
        d_names[d] = entry

# Total Matches
match_count = len(ground_truth)

# Populate negative class tuples
for c in c_names:
    for d in d_names:
        if (c,d) not in ground_truth:
            ground_truth[(c,d)] = 0

# Print stats
print match_count, "ground truth matches"
print len(ground_truth) - match_count, "ground truth non-matches"
print len(ground_truth), "ground truth total"


# Read submission
# Handling many submissions now...
print "** Loading Submission(s) **"
files = []

# Check if it's a file or a directory
if os.path.isfile(submissions_file):
    files.append(submissions_file)
elif os.path.isdir(submissions_file):
    for f in os.listdir(submissions_file):
        files.append(submissions_file + f)

for f in files:
    print "-- Chewing on", f
    with codecs.open(f, "r", encoding='utf8') as sub_outputs:
        bad_c_names = set()
        bad_d_names = set()
        for line in sub_outputs:
            uniline = unicode(line)
            entry = json.loads(uniline)
            c = ftfy.fix_text(entry["site_c"])
            d = ftfy.fix_text(entry["site_d"])
            score = entry["score"]

            # Check for names that don't match up
            if c not in c_names and c not in bad_c_names:
                print c, "not in c, skipping all matches with this user in c"
                bad_c_names.add(c)
            if d not in d_names and d not in bad_d_names:
                print d, "not in d, skipping all matches with this user in d"
                bad_d_names.add(d)

            # Add sumission
            submissions[(c,d)] = score

    print len(submissions), "total submissions"
    print len(bad_d_names) * len(c_names) + len(bad_c_names) * len(d_names), "bad submissions"
    
    # Generate different ones based on different data slices #
    print "** Generating Plots **"

    # All Matches
    doROC(ground_truth,"All",f)

    # Easy
    easy_pairings = filter(lambda x: c_names[x[0]]["type"] in ["easy"] or \
        d_names[x[1]]["type"] in ["easy"], ground_truth)
    doROC(easy_pairings,"Easy",f)

    # Hard
    hard_pairings = filter(lambda x: c_names[x[0]]["type"] in ["hard"] or \
        d_names[x[1]]["type"] in ["hard"], ground_truth)
    doROC(hard_pairings,"Hard",f)

    # Hard with some data
    hard_pairings_some_data = filter(lambda x: (c_names[x[0]]["type"] in ["hard"] and \
        d_names[x[1]]["site_d_data"] > 0 ) or (d_names[x[1]]["type"] in ["hard"] \
        and d_names[x[1]]["site_c_data"] > 0), ground_truth)
    doROC(hard_pairings_some_data,"Hard_w_Data",f)

    # Hard with no data - how did you find these?
    hard_pairings_no_data = filter(lambda x: (c_names[x[0]]["type"] in ["hard"] and \
        d_names[x[1]]["site_d_data"] == 0 ) or (d_names[x[1]]["type"] in ["hard"] \
        and d_names[x[1]]["site_c_data"] == 0), ground_truth)
    doROC(hard_pairings_no_data,"Hard_no_Data",f)

metrics_out.close()

