# this file is used to remove the homolog of query from reference by blast result

# /////////////////////////////
import sys
crossVal_sample_dir=sys.argv[1]
blast_result=sys.argv[2]
# fold of validation
sample_number=int(sys.argv[3])  # fold of cross validation
sample_size=int(sys.argv[4])   # number of times which are actually conducted, validation number, used to calculate the standard erro
sample_mode=sample_number/sample_size

import os
# number of file which is used for validation
selected_number=[]
for i in range(sample_number):
    if i%sample_mode==0:
        selected_number.append(i)

# construct dir and query and ref file (dat and fasta), respectively
for i in range(sample_number):
    if i in selected_number:
        os.system("cut -f 1 %ssample%d/query%d.dat > %s/sample%d/query%d.list"%(crossVal_sample_dir,i,i,crossVal_sample_dir,i,i))
        os.system("fgrep -wf %ssample%d/query%d.list %s |cut -f 2 > %s/sample%d/homolog_removed%d.list"%(crossVal_sample_dir,i,i,blast_result,crossVal_sample_dir,i,i))
        os.system("fgrep -wvf %ssample%d/homolog_removed%d.list %s/sample%d/reference%d.dat > %s/sample%d/temp.dat"%(crossVal_sample_dir,i,i,crossVal_sample_dir,i,i,crossVal_sample_dir,i))
        os.system("mv %ssample%d/temp.dat %s/sample%d/reference%d.dat"%(crossVal_sample_dir,i,crossVal_sample_dir,i,i))
        os.system("rm %ssample%d/*.list"%(crossVal_sample_dir,i))

