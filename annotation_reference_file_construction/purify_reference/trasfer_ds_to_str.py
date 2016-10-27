# this file is used to transfer reference.dat into temp.dat which is like
# proteinID ds1ds2
# proteinID ds1ds3

f=open('reference.dat','r')
import os
os.system("cat /dev/null > temp.dat")
g=open('temp.dat','r+')

def lst_trans_str(lst):
    lst.sort()
    ds_in_str=''
    for item in lst:
        ds_in_str+=item
    return ds_in_str

for line in f:
    row=line.rstrip().split('\t')
    ds_lst=row[2].split(',')
    proteinID=row[0]
    g.write(proteinID+'\t'+lst_trans_str(ds_lst)+'\n')

f.close()
g.close()    
