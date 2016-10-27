# this file is used to form the domain signature-EC number machine learning model to annotate enzymes at the first EC hierarchy level

# basic algorithm:
# covert the raw data to another dataset 
# raw data:
# {ds:[ec1,ec2, ...], ...}
# new dataset
# {ds:{ec1:abundance, ec2:abundance, ...}, ds:{}, ...}

import pickle
ds_ec_raw_dic=pickle.load(open('ec_domain_1_pickle','rb'))
# data structure
# {ds:[ec1,ec2, ...], ...}

# used to convert a [ec1,ec2, ...] to {ec1:abundance, ec2:abundance, ...}
def calculate_abundabce(ec_list):
    nr_set=[]
    abun_dic={}
    total_num=0
    for ec in ec_list:
        if ec not in nr_set:
            abun_dic[ec]=1
            nr_set.append(ec)
        else:
            abun_dic[ec]+=1
        total_num+=1
    for ec in abun_dic:
        abun_dic[ec]=float(abun_dic[ec])/float(total_num)
    return abun_dic

# convert the raw ds_ec dic to the abundance matrix as described at the very begining
abundance_matrix={}
for ds in ds_ec_raw_dic:
    ec_list=ds_ec_raw_dic[ds]
    abundance_matrix[ds]=calculate_abundabce(ec_list)

 
def get_dominant_ec(abundance_dic): # get the dominant ec subgroup and use its abunance as specificity
    dominant_ec='' # to store the dominant ec subgroup
    dominant_abundance=0.0
    for ec in abundance_dic:
        if abundance_dic[ec]>dominant_abundance:
            dominant_ec=ec
            dominant_abundance=abundance_dic[ec]
    return {'EC':[dominant_ec],'Specificity':[dominant_abundance]}

# construct the prediction model
domain_signature_ec_dic={} # the prediction model at this ec hierarchical level
specific_number=0
for ds in abundance_matrix:
    dominat_ec_subgroup=get_dominant_ec(abundance_matrix[ds])
    domain_signature_ec_dic[ds]=dominat_ec_subgroup
    if dominat_ec_subgroup['Specificity'][0]==1.0:
        specific_number+=1
    #print ds,
    #print '   ',
    #print dominat_ec_subgroup

print "number of ds-ec pairs for the 1st ec hierarchy level:  ",
print len(domain_signature_ec_dic)
print "number of 100% specific ds-ec pairs for the 1st ec hierarchy level:  ",
print str(specific_number)
pickle.dump(domain_signature_ec_dic,open('domain_signature_ec_dic_1st_pickle','wb'))


