# use specific_enzyme_ds_in_string.list to purify
# and, output has at least one EC digit

import os
os.system("cat /dev/null > purified_reference.dat")
g=open('purified_reference.dat','w')

def lst_trans_str(lst):
    lst.sort()
    ds_in_str=''
    for item in lst:
        ds_in_str+=item
    return ds_in_str

specific_enzyme=[]
for line in open('specific_enzyme_ds_in_string.list', 'r'):
    specific_enzyme.append(line.strip())

for line in open('reference.dat', 'r'):
    row=line.rstrip().split('\t')
    ec=row[1]
    if ec=='EC=-.-.-.-' or ec=='Non-enzyme':
        continue
    ds_lst=row[2].split(',')
    ds_str=lst_trans_str(ds_lst)
    if ds_str in specific_enzyme:
        g.write(line)

g.close()    
