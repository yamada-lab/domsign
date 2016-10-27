#!/usr/bin/python

# this script is used to construct another script to automatically conduct ds based annotation for many files

import os
import sys

# the directory which contains a lot if files as sample0 sample 1 ...
sample_dir=sys.argv[1]
# other environment variables
training_dataset_dir=os.environ['training_dataset_dir']
DomSign_tool_path=os.environ['SCRIPTPATH']
specificity_threshold=os.environ['specificity_threshold']
specific_enzyme_signature=os.environ['specific_enzyme_signature_file']

# fold of validation
sample_number=int(os.environ['validation_fold'])
# range of number to get one used file, if equals to 1, then all are selected
sample_mode=sample_number/int(os.environ['validation_number'])

selected_number=[]
for i in range(sample_number):
    if i%sample_mode==0:
        selected_number.append(i)

os.system('cat /dev/null > %s/parallel_annotation.sh'%(training_dataset_dir))
g=open('%s/parallel_annotation.sh'%(training_dataset_dir),'r+')
os.system('mkdir %s/result_store/'%(training_dataset_dir))

for i in selected_number:
    # construct file with required format in DomSogn.prediction.sh
    g.write('cut -f 1,3 %ssample%d/query%d.dat > %ssample%d/temp%d.dat\n'%(sample_dir,i,i,sample_dir,i,i))
    g.write('%s/DomSign.prediction.sh -i %ssample%d/temp%d.dat -r %ssample%d/reference%d.dat -e %s -s %s -o crossVal_result.%d\n'%(DomSign_tool_path,sample_dir,i,i,sample_dir,i,i,specific_enzyme_signature,specificity_threshold,i))
    g.write('rm %ssample%d/temp%d.dat\n'%(sample_dir,i,i))
    # evaluate the result and the record file will be output to the query direcotry
    g.write('python %s/cross_validation_file_processing/result_comparison/result_compare_with_official.py %ssample%d/query%d.dat %ssample%d/crossVal_result.%d %s %ssample%d/ crossVal_result_evaluation_%s_%d.txt\n'%(DomSign_tool_path,sample_dir,i,i,sample_dir,i,i,specificity_threshold,sample_dir,i,specificity_threshold,i))
    g.write('cp %ssample%d/crossVal_result_evaluation_%s_%d.txt %s/result_store/\n'%(sample_dir,i,specificity_threshold,i,training_dataset_dir))
g.close()

    
