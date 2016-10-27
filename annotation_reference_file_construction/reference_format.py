# this script is used to format the reference from
# reference.dat
# proteinID ec1,ec2,ec3 d1,d2,d3
# to reference.dat.formated
# ec1\td1\td2\td3
# ec2\td1\td2\td3
# ec3\td1\td2\td3

import os
import sys

reference_file=sys.argv[1]
f=open(reference_file,'r')
os.system('cat /dev/null > %s.formated'%(reference_file))
g=open('%s.formated'%(reference_file),'r+')

for line in f:
    row=line.rstrip().split('\t')
    proteinID=row[0]
    ec_list=row[1].split(',')
    domain_list=row[2].split(',')
    for ec in ec_list:
        written_line=ec+'\t'
        for domain in domain_list:
            written_line+=domain+'\t'
        g.write(written_line[:-1]+'\n')
f.close()
g.close()

