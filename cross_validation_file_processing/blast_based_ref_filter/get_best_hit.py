# this script is used to extract only the best hit or several best hits for a particular query after outfmt -6 blast
# input: the raw outfmt 6 blast result

import os
import sys
blast_file=sys.argv[1]

def file_generator(filename):
    f=open(filename,'r')
    for line in f:
        yield line
    f.close()

os.system('cat /dev/null > %s.besthit'%(blast_file))
g=open('%s.besthit'%(blast_file),'r+')

the_last_query=''
best_hit_evalue=0.0
for line in file_generator(blast_file):
    row=line.rstrip().split('\t')
    query=row[0]
    evalue=float(row[10])
    if query!=the_last_query: # zone for the next query
        g.write(line)
        the_last_query=query
        best_hit_evalue=evalue
    else: # still in the zone of this query
        if evalue<=best_hit_evalue:
            g.write(line)
g.close()
