# this script is used to construct another script to automatically conduct ds based annotation for many files

import os
import sys

# the directory which contains a lot if files as sample0 sample 1 ...
sample_dir=sys.argv[1]

# fold of validation
sample_number=10
# number of file which is used for validation
selected_number=[]
sample_mode=1  # range of number to get one used file, if equals to 1, then all are selected
for i in range(sample_number):
    if i%sample_mode==0:
        selected_number.append(i)

os.system('cat /dev/null > parallel_annotation.sh')
g=open('parallel_annotation.sh','r+')
# place to store all these result files
os.system('mkdir result_store/')

for i in selected_number:
    g.write('cp %ssample%d/query%d.dat ./query.dat\n'%(sample_dir,i,i))
    g.write('cp %ssample%d/reference%d.dat ./reference.dat\n'%(sample_dir,i,i))
  #  g.write('cp %ssample%d/specific_enzyme_domain_signature.dat ../annotation_reference_file_construction/purify_reference/specific_enzyme_ds_in_string.list\n'%(sample_dir,i))
    g.write('bash ../domain_sign_based_enzyme_annotation_pipeline.sh\n')
    g.write('mv domain_signature_final_result.txt result_store/ds_final_result%d.txt\n'%(i))
g.close()

    
