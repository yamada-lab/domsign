# this file is used to construct cross validation samples from one source file
# data file
# proteinID EC1,EC2 dom1 
# proteinID EC1,EC2 dom1,dom2
# EC can be EC=x.x.x.x or Non-enzyme
# basic logic:
# 1. start to scan the source.dat file (also dat of uniprot_protein_with_one_ec)
# 2. based on mode, seperate the .dat line into different samples, at the same time, find corresponding seq in fasta_dic and write in corresponding query.fasta and all other ref.fasta

# /////////////////////////////
# first of all, set the dir of your source fasta and source dat
import sys
source_dat=sys.argv[1]

import os

# directory of the query
query_dir=os.environ['training_dataset_dir']

# fold of validation
sample_number=int(os.environ['validation_fold'])
# range of number to get one used file, if equals to 1, then all are selected
sample_mode=sample_number/int(os.environ['validation_number'])

# number of file which is used for validation
selected_number=[]
for i in range(sample_number):
    if i%sample_mode==0:
        selected_number.append(i)

# dic to store the key to the opened file which will be written in
query_dat_storage={}
reference_dat_storage={}

# construct dir and query and ref file (dat and fasta), respectively
for i in range(sample_number):
    if i in selected_number:
        os.system("mkdir %s/cross_validation/sample%d"%(query_dir,i))
        os.system("cat /dev/null > %s/cross_validation/sample%d/query%d.dat"%(query_dir,i,i))
        os.system("cat /dev/null > %s/cross_validation/sample%d/reference%d.dat"%(query_dir,i,i))
        query_dat_storage[i]=open('%s/cross_validation/sample%d/query%d.dat'%(query_dir,i,i),'w')
        reference_dat_storage[i]=open('%s/cross_validation/sample%d/reference%d.dat'%(query_dir,i,i),'w')

# give a protein ID, write corresponding dat line in corresponding dat file 
# written_line is the dat line to be written in 
# thus, given a position, query[position] will be written; ref[other positions] will be written
def write_dat(position,written_line):
    global query_dat_storage
    global reference_dat_storage
    global selected_number
    if position in selected_number:
        query_dat_storage[position].write(written_line)
    for i in reference_dat_storage:
        if i!=position:
            reference_dat_storage[i].write(written_line)

# ///////////////////////////////
# begin to have sample and build fasta and dat query and ref
# write in query file based on the mode of line number in uniprot_protein_with_one_ec.dat
f=open(source_dat,'r')
#f=open('test.dat','r')
for i, line in enumerate(f):
    mode_of_line=i%(sample_number)
    write_dat(mode_of_line,line)
f.close()

# close everything    
for i in range(sample_number):
    if i in selected_number:
        query_dat_storage[i].close()
        reference_dat_storage[i].close()

    
    


 
