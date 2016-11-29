# Challenge Problem 1

In this directory, the following files are provided towards the goal of evaluating team submission data against ground truth data for Challenge Problem #1:

### CP1_eval_script.py
This is the Python script that will be used to compare team submission data against ground truth data.

### ground_truth_sample_CP1.json
This file contains the known ground truth data against which team submissions will be compared.  Each line of this file is a JSON formatted dictionary with the following key-value pairs:
##### key: value
cluster_id: Cluster id assigned to test set of clusters

class: An integer that takes values 0 or 1 and indicates if associated cluster is related to human-trafficking.

### submission_sample_CP1.json
This file contains the data submitted by the team, which is to be compared against the known ground truth data.  Each line of this file is a JSON formatted dictionary with the following key-value pairs:
##### key: value
cluster_id: Cluster id assigned to clusters

score: An number that takes values between 0 and 1 inclusively, and is a measure of the probability that the extracted cluster is a positive, with values closer to 1 indicating a higher probability that the phone number is a positive

### output_sample_CP1.pdf
This file provides a sample of expected output of the evaluation script when run on the sample data files provided with the example usage command shown below.

The file contains an image showing the reciever operating characteristic (ROC) curve for the evaluation of the submission data against the ground truth data.  The value of the area under the curve (AUC) is also noted at the top of the figure.

Note that while this sample output file is in PDF format, the output format is variable and is dependent on the tag of the output file name provided in the command to run the evaluation script.  For example, substituting `output_sample_CP1.pdf` for `output_sample_CP1.png` in the example usage command below will produce an output file format of PNG rather than PDF.

### output_cg_sample_CP1.pdf
This file provides a sample of expected output of the evaluation script when run on the sample data files provided with the example usage command shown below.

The file contains an image showing the cumulative gain chart for the submission data against the ground truth data.  It also provides a linear baseline (the dotted red line) for comparison.

Note that while this sample output file is in PDF format, the output format is variable and is dependent on the tag of the output file name provided in the command to run the evaluation script.  For example, substituting `output_cg_sample_CP1.pdf` for `output_cg_sample_CP1.png` in the example usage command below will produce an output file format of PNG rather than PDF.

### Example Usage

Note that the file names given in the example usage command below (i.e., `ground_truth_sample_CP1.json submission_sample_CP1.json output_sample_CP1.pdf output_cg_sample_CP1.pdf`) are example file names and can be substituted for the appropriate file names.

To run the evaluation of submission data contained in a file named `submission_sample_CP1.json` against ground truth data contained in a file named `ground_truth_sample_CP1.json` and save the output to new files named `output_sample_CP1.pdf` and `output_cg_sample_CP1.pdf` use:

`python CP1_eval_script.py ground_truth_sample_CP1.json submission_sample_CP1.json output_sample_CP1.pdf output_cg_sample_CP1.pdf`
