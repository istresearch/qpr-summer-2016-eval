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
	ads = set(gt['ads']) & set(sub['ads'])
	temp_dict['recall'] = (len(ads) * 100)/float(len(gt['ads']))
	recalls.append((len(ads) * 100)/float(len(gt['ads'])))

	#TODO Answer "score" is simply recall of answer list?
	if 'answer' in gt.keys():
		# If submission also has answer, score it
		if 'answer' in sub.keys():
			answers = set(gt['answer']) & set(sub['answer'])
			temp_dict['answer_score'] = (len(answers) * 100)/float(len(gt['answer']))
		# If submission does not have answer, score it as zero
		else:
			temp_dict['answer_score'] = 0.0

	results_dict[entry] = temp_dict
	del(sub)

avg_recall =  sum(recalls)/float(len(recalls))

# DEBUG
for entry in results_dict.keys():
	print("Question ID {0}:".format(entry), file=output_file)
	if 'answer_score' in results_dict[entry].keys():
		print("ANSWER SCORE: {0}".format(results_dict[entry]['answer_score']), file=output_file)
	print("RECALL: {0}".format(results_dict[entry]['recall']), file=output_file)
	print(" ", file=output_file)

print("AVERAGE RECALL FOR ALL QUESTIONS ANSWERED: {0}".format(avg_recall), file=output_file)
