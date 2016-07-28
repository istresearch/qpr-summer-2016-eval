#!/usr/bin/env python
from __future__ import print_function
import sys
import json

# how to use: python CP4_eval_script.py ground_truth_sample_CP4.json submission_sample_CP4.json output_sample_CP4.txt
output_file = open(sys.argv[3], "w")

################################################
# ground truth data
gt_outputs = open(sys.argv[1], "r")
gt_dict = {}
for line in gt_outputs:
	entry = json.loads(line)
	question_id = entry['question_id']
	gt_dict[question_id] = entry
################################################

################################################
# submission data
sub_outputs = open(sys.argv[2], "r")
sub_dict = {}
for line in sub_outputs:
	entry = json.loads(line)
	question_id = entry['question_id']
	sub_dict[question_id] = entry
################################################

results_dict = {}
skipped_questions = []
recalls = []

for entry in gt_dict.keys():
	temp_dict = {}
	gt = gt_dict[entry]
	try:
		sub = sub_dict[entry]
	except:
		print("Submission for question id {0} not found".format(entry))
		skipped_questions.append(entry)
		continue

	# 'answer' is a list of dicts.  We are only concerned with the first dict.
	# Each dict must contains the key 'ads'.
	for key in gt['answer'][0].keys():
		if key =='ads':
			gt_ads = gt['answer'][0][key].split(',')
			sub_ads = sub['answer'][0][key].split(',')
			overlap = set(gt_ads) & set(sub_ads)
			recall = (len(overlap) * 100)/float(len(gt_ads))
			recalls.append(recall)
			temp_dict['RECALL'] = recall

		# Assumes at most one other key may be given
		else:
			# Some submissions may not provide answers to questions
			try:
				# This assumes formatting of strings (e.g., addresses)
				# must be perfect
				overlap = set(gt['answer'][0][key]) & set(sub['answer'][0][key])
				recall = (len(overlap) * 100)/float(len(gt['answer'][0][key]))
			except:
				recall = 0.0
			temp_dict['ANSWER'] = recall

	results_dict[entry] = temp_dict
	del(sub)

avg_recall =  sum(recalls)/float(len(recalls))

# DEBUG
for entry in results_dict.keys():
	print("Question ID {0}:".format(entry), file=output_file)
	for key in results_dict[entry].keys():
		print("{0}: {1}".format(key, results_dict[entry][key]), file=output_file)
	print(" ", file=output_file)

print("AVERAGE RECALL FOR ALL QUESTIONS ANSWERED: {0}".format(avg_recall), file=output_file)
