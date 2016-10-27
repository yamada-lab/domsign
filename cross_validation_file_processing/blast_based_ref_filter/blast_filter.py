# this script is used to extract the desired hits from a blast result based on several thresholds:
# identity, coverage for query, coverage for hit;

# first of all get the query and database fastafile, respectively
import os
import sys

query_file=sys.argv[1]
blast_result_file=sys.argv[2]

identity_thre=False
identity=0.0
flag=raw_input("Whether you would like to use identity as threshold (yes or no):   ")
if flag=='yes':
    identity_thre=True
    identity=float(raw_input("Type in the cutoff for identity (0.0-1.0 real number):   "))
print 'Identity: %s'%str(identity)

# coverage for query
flag='no'
queryCoverage_thre=False
queryCoverage=0.0
flag=raw_input("Whether you would like to use query coverage as threshold (yes or no):   ")
if flag=='yes':
    queryCoverage_thre=True
    queryCoverage=float(raw_input("Type in the cutoff for query coverage (0.0-1.0 real number):   "))
print 'queryCoverage: %s'%str(queryCoverage)


# now construct the query length dic with data structure like this
# {queryID:float,queryID:float}
query_length_dic={}
proteinID='' # to store the protein ID now
f=open(query_file,'r')
for line in f:
    if line[0]=='>':
        proteinID=line[1:(-1)].split(' ')[0]
        query_length_dic[proteinID]=0.0
    else:
        query_length_dic[proteinID]+=float(len(line.rstrip()))
f.close()        

# now it is time for filtering
f=open(blast_result_file,'r')
os.system('cat /dev/null > %s.trim.iden%s.queCo%s'%(blast_result_file,str(int(identity*100)),str(int(queryCoverage*100))))
g=open('%s.trim.iden%s.queCo%s'%(blast_result_file,str(int(identity*100)),str(int(queryCoverage*100))),'r+')
keys=['queryId', 'subjectId', 'percIdentity', 'alnLength', 'mismatchCount', 'gapOpenCount', 'queryStart', 'queryEnd', 'subjectStart', 'subjectEnd', 'eVal', 'bitScore']
blast_result=[]
for line in f:
    row=dict.fromkeys(keys)
    elements=line.rstrip().split('\t')
    for i, elem in enumerate(elements):
        row[keys[i]]=elem
    flag=True  # judge whether this result pass or not
    if identity_thre:
        if float(row['percIdentity'])/100.0<identity:
            flag=False
    if queryCoverage_thre:
        result_queryCoverage=float(row['alnLength'])/float(query_length_dic[row['queryId']])
        if result_queryCoverage<queryCoverage:
            flag=False
    if flag:
        g.write(line)
f.close()
g.close()







# trim the result and 
