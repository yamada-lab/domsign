import sys
argvs = sys.argv
if len(argvs) != 2:
	print "Usage: $python %s ***.reference" %argvs[0]
	quit()
list = open(argvs[1],'r').readlines()
kmers = []
try:
	for l in list:
		temp = l.rstrip().split('\t')
		if temp[1] != "Non-enzyme":
			kmers.append(sorted(temp[2].split(',')))
except:
	print "format error"
	quit()
stringkmers = []
for k in kmers:
	stringkmers.append("".join(k))
sorted_stringkmers = sorted(stringkmers)

OUTPUT = ""
tmp = ""
i = 0
while i < len(sorted_stringkmers):
	if tmp != sorted_stringkmers[i]:
		tmp = sorted_stringkmers[i]
		OUTPUT += tmp+'\n' 
	i += 1

f = open(argvs[1]+'_string.list','w')
f.writelines(OUTPUT)
f.close