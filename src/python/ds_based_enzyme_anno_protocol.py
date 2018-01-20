# this file is used to annotation protein based on their domain signature from EC x.-.-.-.- to EC x.x.x.x
# Five files are needed to do the annotation. Firstly, one file named after 'query.dat', stored with data structure like:
# proteinID EC ds1 ds2 ds3
# Secondly, four pickle files as annotation reference

# ///////////////
# to construct the geneID-ds dici
import argparse, pickle

parser = argparse.ArgumentParser(
        prog='purify_reference.py'
        )
parser.add_argument('-q', dest='query_filename', required=True)
parser.add_argument('-d', dest='pickle_directry', required=True)
parser.add_argument('-t', dest='threshold', required=True)
parser.add_argument('-s', dest='session_id', required=True)
parser.add_argument('-o', dest='output_filename', required=True)
args = parser.parse_args()



dom_posi=1

count=0
record=0
query_protein_domain_sign_dic={} # to store {geneID:[domain1, domain2, ],  }
f=open(args.query_filename,'r')
for line in f:
    row=line.rstrip().split('\t')
    geneID=row[0]
    domain_signature=row[dom_posi].split(',')
    domain_signature.sort()
    query_protein_domain_sign_dic[geneID]=domain_signature
f.close()


def list_str_trans(lst): # used to transfer list of domain signature to string so that we can use it as dic key
    lst.sort()
    name=''
    for i in lst:
        name+=i
    return name

domain_signature_ec_dic_uniprot_1st=pickle.load(open(args.pickle_directry+'/domain_signature_ec_dic_1st_pickle_'+args.session_id,'rb'))
domain_signature_ec_dic_uniprot_2nd=pickle.load(open(args.pickle_directry+'/domain_signature_ec_dic_2nd_pickle_'+args.session_id,'rb'))
domain_signature_ec_dic_uniprot_3rd=pickle.load(open(args.pickle_directry+'/domain_signature_ec_dic_3rd_pickle_'+args.session_id,'rb'))
domain_signature_ec_dic_uniprot_4th=pickle.load(open(args.pickle_directry+'/domain_signature_ec_dic_4th_pickle_'+args.session_id,'rb'))

#///////////////////////////////////////
# for domain signatures on each level, there is always a situation that this domain signature occur in the last level but not in this(it actually happenned because the basical protein number to form the four level domain signature ec dic is a little bit different, because you remove EC:x.x.x.- in level 4).
# list used to store the increase ds from the bigger level to the lower level
surplus_from_1_to_2=[]
surplus_from_2_to_3=[]
surplus_from_3_to_4=[]

# list to store all the ds in four ds_ec_dic files
ds_1=[]
ds_2=[]
ds_3=[]
ds_4=[]

# append ds into them
for i in domain_signature_ec_dic_uniprot_1st:
    ds_1.append(i)
for i in domain_signature_ec_dic_uniprot_2nd:
    ds_2.append(i)
for i in domain_signature_ec_dic_uniprot_3rd:
    ds_3.append(i)
for i in domain_signature_ec_dic_uniprot_4th:
    ds_4.append(i)

for i in ds_3:
    if i not in ds_4:
        surplus_from_3_to_4.append(i)
for i in ds_2:
    if i not in ds_3:
        surplus_from_2_to_3.append(i)
for i in ds_1:
    if i not in ds_2:
        surplus_from_1_to_2.append(i)

print ('number of domain signature in annotation file 1 but not in 2:{}'.format(str(len(surplus_from_1_to_2))))
print ('number of domain signature in annotation file 2 but not in 3:{}'.format(str(len(surplus_from_2_to_3))))
print ('number of domain signature in annotation file 3 but not in 4:{}'.format(str(len(surplus_from_3_to_4))))

protein_without_ref_ds_count=0
#///////////////////////////////////////////////////////
# ok, now we define a function to annotate enzyme from level 1 to level 4
def annotation_by_ds(domain_signature,specificity):  # use a domain signature to annotate an enzyme
    global domain_signature_ec_dic_uniprot_1st
    global domain_signature_ec_dic_uniprot_2nd
    global domain_signature_ec_dic_uniprot_3rd
    global domain_signature_ec_dic_uniprot_4th
    global ds_1  # ds_1 is all the possible domain sign in reference, we will use it as the first filter
    global surplus_from_3_to_4
    global surplus_from_2_to_3
    global surplus_from_1_to_2
    global protein_without_ref_ds_count
    return_item={'EC':'Non-enzyme','Specificity':0.0} # item need to return by this function
    # ////////////////////////
    # enter to the first level
    if domain_signature not in ds_1:  # use ds_1 as the first filter to filter some ds not in reference
        protein_without_ref_ds_count+=1
        return return_item
    if (domain_signature_ec_dic_uniprot_1st[domain_signature]['EC'][0]=='EC=-.-.-.-') or (domain_signature_ec_dic_uniprot_1st[domain_signature]['Specificity'][0]<specificity): # if on this level, it has been impossible to do further annotation or  when this level annotation is less than specificity
        return {'EC':'EC=-.-.-.-','Specificity':0.0} # return the result by last level annotation
    else:    
        return_item['EC']=(domain_signature_ec_dic_uniprot_1st[domain_signature]['EC'][0]+'.-.-.-')
        return_item['Specificity']=domain_signature_ec_dic_uniprot_1st[domain_signature]['Specificity'][0]
    if domain_signature in surplus_from_1_to_2: # to check whether to return or not
        return return_item
    # ////////////////////////
    # enter to the second level
    elif (domain_signature_ec_dic_uniprot_2nd[domain_signature]['EC'][0]=='EC=-.-.-.-') or (domain_signature_ec_dic_uniprot_2nd[domain_signature]['Specificity'][0]<specificity): # if on this level, it has been impossible to do further annotation or  when this level annotation is less than specificity: 
        return return_item # return the result by last level annotation
    else: # annotation
        return_item['EC']=(domain_signature_ec_dic_uniprot_2nd[domain_signature]['EC'][0]+'.-.-')
        return_item['Specificity']=domain_signature_ec_dic_uniprot_2nd[domain_signature]['Specificity'][0]
    if domain_signature in surplus_from_2_to_3: # to check whether to return or not,two conditions to return here
        return return_item
    # ////////////////////////
    # enter to the third level
    elif (domain_signature_ec_dic_uniprot_3rd[domain_signature]['EC'][0]=='EC=-.-.-.-') or (domain_signature_ec_dic_uniprot_3rd[domain_signature]['Specificity'][0]<specificity): # if on this level, it has been impossible to do further annotation or  when this level annotation is less than specificity:
        flag=True # prepare to return the result by last level annotation
    else: # annotation
        return_item['EC']=(domain_signature_ec_dic_uniprot_3rd[domain_signature]['EC'][0]+'.-')
        return_item['Specificity']=domain_signature_ec_dic_uniprot_3rd[domain_signature]['Specificity'][0]
    if domain_signature in surplus_from_3_to_4: # to check whether to return or not, two conditions to return here
        return return_item
    # ////////////////////////
    # enter to the fourth level
    # attention: about the return, for it is the last level, so a little different from others
    elif (domain_signature_ec_dic_uniprot_4th[domain_signature]['EC'][0]=='EC=-.-.-.-') or (domain_signature_ec_dic_uniprot_4th[domain_signature]['Specificity'][0]<specificity): # if on this level, it has been impossible to do further annotation or  when this level annotation is less than specificity
        return return_item
    else: # annotation
        return_item['EC']=domain_signature_ec_dic_uniprot_4th[domain_signature]['EC'][0]
        return_item['Specificity']=domain_signature_ec_dic_uniprot_4th[domain_signature]['Specificity'][0]
        return return_item    

# specificity used for annotation
specificity=float(args.threshold)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



# set new specificity and do another annotation and comparision
# ///////////////////////////////////////////////////
# Here is something important, to set the specificity to your annotation
name=int(specificity*100) # integrate name to be written in the file
g=open(args.output_filename,'w')
f=open(args.query_filename,'r')
protein_annotation_by_others_dic={}  # dic to store the protein annotation info of the last file   data structure:{protein ID:{'EC':[x,x,x,x]}, protein ID:{'EC':[y,y,y,y]}} the x.x.x.x is the EC number on level 1,2,3,4, respectively
protein_annotation_by_ds_dic={} # dic to store the protein annotation by domain signature   data structure:{protein ID:{'EC':[x,x,x,x],'Domain Signature':string,'Specificity':x.x}, protein ID:{'EC':[x,x,x,x],'Domain Signature':string,'Specificity':x.x}} the x.x.x.x is the EC number on level 1,2,3,4, respectively. It has a domain signature more than the by_others one because it needs this info for further annotation

# renew the two annotation dictionary to use another new specificity to do annotation
for line in f:
    row=line.rstrip().split('\t')
    protein_ID=row[0]
    EC=row[1] 
    protein_annotation_by_others_dic[protein_ID]={} # store 
    protein_annotation_by_others_dic[protein_ID]['EC']=EC # store 
    protein_annotation_by_ds_dic[protein_ID]={} # store 
    protein_annotation_by_ds_dic[protein_ID]['EC']='EC=-.-.-.-' # store 
    protein_annotation_by_ds_dic[protein_ID]['Domain Signature']=list_str_trans(query_protein_domain_sign_dic[protein_ID])  # transfer domain signature to it
f.close()

# begin to annotate
for i in protein_annotation_by_ds_dic: # annotate every protein
    annotation_dic=annotation_by_ds(protein_annotation_by_ds_dic[i]['Domain Signature'],specificity)
    g.write(i+'\t'+annotation_dic['EC']+'\n')

g.close()
