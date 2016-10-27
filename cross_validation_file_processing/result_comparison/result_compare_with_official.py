# this file is used to compare ds based anootation result with that of official approach
# several files are needed to do the annotation. Firstly, one file named after 'query.dat', stored with data structure like:
# proteinID EC ds1 ds2 ds3
# Secondly, several result_with_specificity_xx.dat files as result of ds annotation, with data sturcutre:
# proteinID EC

# annotation result which has been annotated by ds
import os
import sys
original_query=sys.argv[1]
DomSign_prediction_result=sys.argv[2]
specificity_threshold=sys.argv[3]
output_dir=sys.argv[4]
output_name=sys.argv[5]

specificity=str(int(float(specificity_threshold)*100))
# ///////////////
# to construct true annotation dictionary
f=open(original_query,'r')
protein_annotation_by_others_dic={}  # dic to store the protein annotation info of the last file   data structure:{protein ID:{'EC':[x,x,x,x]}, protein ID:{'EC':[y,y,y,y]}} the x.x.x.x is the EC number on level 1,2,3,4, respectively
for line in f:
    row=line.rstrip().split('\t')
    protein_ID=row[0]
    EC=row[1] 
    protein_annotation_by_others_dic[protein_ID]={} # store 
    protein_annotation_by_others_dic[protein_ID]['EC']=EC # store 
f.close()

# ///////////////
# the annotation by DomSign.tool
f=open(DomSign_prediction_result,'r')
protein_annotation_by_ds_dic={} # dic to store the protein annotation by domain signature   data structure:{protein ID:{'EC':[x,x,x,x],'Domain Signature':string,'Specificity':x.x}, protein ID:{'EC':[x,x,x,x],'Domain Signature':string,'Specificity':x.x}} the x.x.x.x is the EC number on level 1,2,3,4, respectively. It has a domain signature more than the by_others one because it needs this info for further annotation
for i,line in enumerate(f):
    row=line.rstrip().split('\t')
    protein_ID=row[0]
    EC=row[1] 
    protein_annotation_by_ds_dic[protein_ID]={} # initiation
    protein_annotation_by_ds_dic[protein_ID]['EC']=EC # initiation
f.close()

# get the file to record the result evaluation
os.system("cat /dev/null >%s/%s"%(output_dir,output_name)) # costructed for final results storage
g=open('%s/%s'%(output_dir,output_name),'a')

def list_str_trans(lst): # used to transfer list of domain signature to string so that we can use it as dic key
    lst.sort()
    name=''
    for i in lst:
        name+=i
    return name

#///////////////////////////////////////////////////////
# ok, now we define a function to compare result with official annotation

def annotation_comparison(ec_ds,ec_official,limit): # used to compare on which level two annotations of EC are the same. Limit is the highest level that above which no ec of these two are '-'
    # we have limit parameter here just to avoid the problem like that '3.-.-.-' and '3.-.-.-' is pipelined to have a reliable annotation level 4 rather than 1. Actually, 1 is correct
    if 'Non-enzyme' in ec_ds or 'Non-enzyme' in ec_official:
        return -1.0
    else:
        ec1=ec_ds[3:].split('.')  # get the list of ec
        ec2=ec_official[3:].split('.') # get the list of ec
        if limit==0 or ec1[0]!=ec2[0]: # compare on each level 'or limit==x' means here is the last level we have both of the two not to be '-', thus it has been the limit of reliable level
            return 0.0
        elif limit==1 or ec1[1]!=ec2[1]:
            return 1.0
        elif limit==2 or ec1[2]!=ec2[2]:
            return 2.0
        elif limit==3 or ec1[3]!=ec2[3]:
            return 3.0
        else:
            return 4.0

def annotation_level(ec): # function to give the annotation level of a string like 'EC=x.x.x.x'
    result={'Annotation Level':'Non-enzyme','Annotation Level in Number':-1.0} # the result is compressed in a dic with two item, each represents annotation level one in string another in float
    if 'Non-enzyme' in ec:
        return result
    elif '-.-.-.-' in ec:
        result={'Annotation Level':'Zero digit','Annotation Level in Number':0.0}
        return result
    elif '.-.-.-' in ec:
        result={'Annotation Level':'1st','Annotation Level in Number':1.0}
        return result
    elif '.-.-' in ec:
        result={'Annotation Level':'2nd','Annotation Level in Number':2.0}
        return result
    elif '.-' in ec:
        result={'Annotation Level':'3rd','Annotation Level in Number':3.0}
        return result
    else:
        result={'Annotation Level':'4th','Annotation Level in Number':4.0}
        return result

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

comparison_result={}
comparison_result['Reliability Comparison']={'-1.0':0.0,'0.0':0.0,'4.0':0.0,'3.0':0.0,'2.0':0.0,'1.0':0.0}

comparison_result['By Domain']={'Non-enzyme':{'Total':0.0,'Eq':0.0,'FP':0.0,'FN':0.0,'IM':0.0},'Zero digit':{'Total':0.0,'Eq':0.0,'FP':0.0,'FN':0.0,'IM':0.0},'4th':{'Total':0.0,'Eq':0.0,'FP':0.0,'FN':0.0,'IM':0.0},'3rd':{'Total':0.0,'Eq':0.0,'FP':0.0,'FN':0.0,'IM':0.0},'2nd':{'Total':0.0,'Eq':0.0,'FP':0.0,'FN':0.0,'IM':0.0},'1st':{'Total':0.0,'Eq':0.0,'FP':0.0,'FN':0.0,'IM':0.0}}

comparison_result['By Official']={'Non-enzyme':0.0,'Zero digit':0.0,'4th':0.0,'3rd':0.0,'2nd':0.0,'1st':0.0}

annotation_false_positive=0 # a list used to store all the above relaible_level(other annotation pipeline)-annotated_level
annotation_false_negative=0 # a list used to store all the below relaible_level(other annotation pipeline)-annotated_level
annotation_equal=0 # a record used to store all the equal relaible_level(other annotation pipeline)-annotated_level
annotation_improvement=0 # to record number of annotation improved than official but don't know whether it is correct or wrong
#////////////////////////////////////
for i in protein_annotation_by_ds_dic: # count percentage of annotation on every level
    ds_annotated_level=-1.0 # on which level we do the annotation
    others_annotated_level=-1.0 # on which level we do the annotation
    by_ds_annotation={}
    by_others_annotation={}
    by_ds_annotation=annotation_level(protein_annotation_by_ds_dic[i]['EC'])
    by_others_annotation=annotation_level(protein_annotation_by_others_dic[i]['EC'])
    comparison_result['By Domain'][by_ds_annotation['Annotation Level']]['Total']+=1.0
    comparison_result['By Official'][by_others_annotation['Annotation Level']]+=1.0
    ds_annotated_level=by_ds_annotation['Annotation Level in Number'] # on which level we do the annotation
    others_annotated_level=by_others_annotation['Annotation Level in Number'] # on which level we do the annotation
# /////////////////////////
# to test the reliability
    reliable_level=annotation_comparison(protein_annotation_by_ds_dic[i]['EC'],protein_annotation_by_others_dic[i]['EC'],int(min(ds_annotated_level,others_annotated_level))) # on which level we have the same annotation; the min give to which level we can use to compare, further compare have no meaning
    comparison_result['Reliability Comparison'][str(reliable_level)]+=1.0
    if others_annotated_level==-1.0: # query is non-enzyme
        if ds_annotated_level>reliable_level: # incorrectly regard non-enzyme as enzyme
            annotation_false_positive+=1
            comparison_result['By Domain'][by_ds_annotation['Annotation Level']]['FP']+=1.0 
        elif ds_annotated_level==reliable_level: # set correctly as enzyme
            annotation_equal+=1
            comparison_result['By Domain'][by_ds_annotation['Annotation Level']]['Eq']+=1.0 
    elif ds_annotated_level>reliable_level and others_annotated_level==reliable_level: # when our approach gives even deeper but possibly correct anotation than reliable one, we might face a problem of false positive (we should annotate more cautiously)
        annotation_improvement+=1
        comparison_result['By Domain'][by_ds_annotation['Annotation Level']]['IM']+=1.0 
    elif ds_annotated_level>reliable_level and others_annotated_level>reliable_level: # when our approach gives even deeper but possibly correct anotation than reliable one, we might face a problem of false positive (we should annotate more cautiously)
        annotation_false_positive+=1
        comparison_result['By Domain'][by_ds_annotation['Annotation Level']]['FP']+=1.0 
    elif others_annotated_level>reliable_level and ds_annotated_level==reliable_level: # when official annotation is more intensive than our approach which equals to reliable annotation level, we should annotate more than that
        annotation_false_negative+=1
        comparison_result['By Domain'][by_ds_annotation['Annotation Level']]['FN']+=1.0 
    elif others_annotated_level==reliable_level and ds_annotated_level==reliable_level:
        annotation_equal+=1 # the annotated level by two approach and reliable level are the same
        comparison_result['By Domain'][by_ds_annotation['Annotation Level']]['Eq']+=1.0 
    
print 'fraction of false positive: %s'%(str(float(annotation_false_positive)/float(len(protein_annotation_by_ds_dic))))        
print 'fraction of false negative: %s'%(str(float(annotation_false_negative)/float(len(protein_annotation_by_ds_dic))))        
print 'fraction of equal: %s'%(str(float(annotation_equal)/float(len(protein_annotation_by_ds_dic))))        
print 'fraction of improvement: %s'%(str(float(annotation_improvement)/float(len(protein_annotation_by_ds_dic))))    
for i in comparison_result:
    if i=='Official Annotation' or i=='Reliability Comparison':
        for j in comparison_result[i]:
            comparison_result[i][j]=comparison_result[i][j]/float(len(protein_annotation_by_ds_dic))

for i in comparison_result['By Domain']:
    if comparison_result['By Domain'][i]['Total']>0:
        comparison_result['By Domain'][i]['FN']=comparison_result['By Domain'][i]['FN']/comparison_result['By Domain'][i]['Total']
        comparison_result['By Domain'][i]['FP']=comparison_result['By Domain'][i]['FP']/comparison_result['By Domain'][i]['Total']
        comparison_result['By Domain'][i]['Eq']=comparison_result['By Domain'][i]['Eq']/comparison_result['By Domain'][i]['Total']
        comparison_result['By Domain'][i]['IM']=comparison_result['By Domain'][i]['IM']/comparison_result['By Domain'][i]['Total']
    else:
        comparison_result['By Domain'][i]['FN']=0.0
        comparison_result['By Domain'][i]['FP']=0.0
        comparison_result['By Domain'][i]['Eq']=0.0
        comparison_result['By Domain'][i]['IM']=0.0

for i in comparison_result['By Domain']:
    comparison_result['By Domain'][i]['Total']=comparison_result['By Domain'][i]['Total']/float(len(protein_annotation_by_ds_dic))
g.write('#//////////////////////////'+'\n')
g.write('Specificity:  '+str(specificity)+'\n')    
g.write('fraction of false positive:'+'\t'+str(float(annotation_false_positive)/float(len(protein_annotation_by_ds_dic)))+'\n')
g.write('fraction of false negative:'+'\t'+str(float(annotation_false_negative)/float(len(protein_annotation_by_ds_dic)))+'\n')
g.write('fraction of equal:'+'\t'+str(float(annotation_equal)/float(len(protein_annotation_by_ds_dic)))+'\n')
g.write('fraction of improvement:'+'\t'+str(float(annotation_improvement)/float(len(protein_annotation_by_ds_dic)))+'\n')
for i in comparison_result:
    if i=='By Official':
        g.write('item: '+i+'\n')
        g.write('Non-enzyme'+'\t'+str(comparison_result[i]['Non-enzyme'])+'\n')
        g.write('Zero digit'+'\t'+str(comparison_result[i]['Zero digit'])+'\n')
        g.write('1st'+'\t'+str(comparison_result[i]['1st'])+'\n')
        g.write('2nd'+'\t'+str(comparison_result[i]['2nd'])+'\n')
        g.write('3rd'+'\t'+str(comparison_result[i]['3rd'])+'\n')
        g.write('4th'+'\t'+str(comparison_result[i]['4th'])+'\n')
    elif i=='Reliability Comparison':
        g.write('item: '+i+'\n')
        g.write('Non-enzyme'+'\t'+str(comparison_result[i]['-1.0'])+'\n')
        g.write('Zero digit'+'\t'+str(comparison_result[i]['0.0'])+'\n')
        g.write('1st'+'\t'+str(comparison_result[i]['1.0'])+'\n')
        g.write('2nd'+'\t'+str(comparison_result[i]['2.0'])+'\n')
        g.write('3rd'+'\t'+str(comparison_result[i]['3.0'])+'\n')
        g.write('4th'+'\t'+str(comparison_result[i]['4.0'])+'\n')

g.write('By Domain'+'\n')
g.write('Annotation Level'+'\t'+'False Positive'+'\t'+'False Negative'+'\t'+'Equality'+'\t'+'Improvement'+'\t'+'Total percentage in all'+'\n')

temp=comparison_result['By Domain']['Non-enzyme']    
FN=temp['FN']
FP=temp['FP']
EQ=temp['Eq']
IM=temp['IM']
Total=temp['Total']
g.write('Non-enzyme'+'\t'+str(FP)+'\t'+str(FN)+'\t'+str(EQ)+'\t'+str(IM)+'\t'+str(Total)+'\n')
temp=comparison_result['By Domain']['Zero digit']    
FN=temp['FN']
FP=temp['FP']
EQ=temp['Eq']
IM=temp['IM']
Total=temp['Total']
g.write('Zero digit'+'\t'+str(FP)+'\t'+str(FN)+'\t'+str(EQ)+'\t'+str(IM)+'\t'+str(Total)+'\n')

temp=comparison_result['By Domain']['1st']    
FN=temp['FN']
FP=temp['FP']
EQ=temp['Eq']
IM=temp['IM']
Total=temp['Total']
g.write('1st'+'\t'+str(FP)+'\t'+str(FN)+'\t'+str(EQ)+'\t'+str(IM)+'\t'+str(Total)+'\n')
temp=comparison_result['By Domain']['2nd']    
FN=temp['FN']
FP=temp['FP']
EQ=temp['Eq']
IM=temp['IM']
Total=temp['Total']
g.write('2nd'+'\t'+str(FP)+'\t'+str(FN)+'\t'+str(EQ)+'\t'+str(IM)+'\t'+str(Total)+'\n')
temp=comparison_result['By Domain']['3rd']    
FN=temp['FN']
FP=temp['FP']
EQ=temp['Eq']
IM=temp['IM']
Total=temp['Total']
g.write('3rd'+'\t'+str(FP)+'\t'+str(FN)+'\t'+str(EQ)+'\t'+str(IM)+'\t'+str(Total)+'\n')
temp=comparison_result['By Domain']['4th']    
FN=temp['FN']
FP=temp['FP']
EQ=temp['Eq']
IM=temp['IM']
Total=temp['Total']
g.write('4th'+'\t'+str(FP)+'\t'+str(FN)+'\t'+str(EQ)+'\t'+str(IM)+'\t'+str(Total)+'\n')
g.close()
