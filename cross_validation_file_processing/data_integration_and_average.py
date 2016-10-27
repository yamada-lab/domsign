# this file is used to integrate the ten files for 10-cross validation 

# firstly, get the common name of the annotation result
import sys
file_dir=sys.argv[1]
common_name=sys.argv[2]
sample_number=int(sys.argv[3])  # fold of cross validation
sample_size=int(sys.argv[4])   # number of times which are actually conducted, validation number, used to calculate the standard erro
sample_mode=sample_number/sample_size
# this name of the real result should be commmon_name0.txt, ... common_name9.txt
selected_number=[]

data_array=[]
for i in range(sample_number):
    data_array.append({})
    if i%sample_mode==0:
        selected_number.append(i)

integrated_data={}
# dictinary with all the same data structure from the second layer of data_array, but with a difference on the first level about average and standard error
final_result={'Average':{},'Standard Error':{}}
for i in selected_number:
    data_array[i]={}
    # array to store the data derived from this result like 
    # {'Specificity:99%':{}, 'Specificity:90%':{}, ...}
    # down-layer data structure
    # {'False Positive':[], 'False Negative':[], 'Equality':[], 'Improvement':[]}
    # the sequence in the list is failure, 1st, 2nd, 3rd and 4th
    f=open('%s/%s%d.txt'%(file_dir,common_name,i),'r')
    key_of_this_item=''
    flag=False # to see whether it is time to push data into array
    for line in f:
        if line[:12]=='Specificity:':
            key_of_this_item=line.rstrip()
            integrated_data[key_of_this_item]={}
            final_result['Average'][key_of_this_item]={}
            final_result['Standard Error'][key_of_this_item]={}
            final_result['Average'][key_of_this_item]={'False Positive':{'Non-enzyme':0.0,'Zero digit':0.0,'1st':0.0,'2nd':0.0,'3rd':0.0,'4th':0.0}, 'False Negative':{'Non-enzyme':0.0,'Zero digit':0.0,'1st':0.0,'2nd':0.0,'3rd':0.0,'4th':0.0}, 'Equality':{'Non-enzyme':0.0,'Zero digit':0.0,'1st':0.0,'2nd':0.0,'3rd':0.0,'4th':0.0}, 'Improvement':{'Non-enzyme':0.0,'Zero digit':0.0,'1st':0.0,'2nd':0.0,'3rd':0.0,'4th':0.0}}
            final_result['Standard Error'][key_of_this_item]={'False Positive':{'Non-enzyme':0.0,'Zero digit':0.0,'1st':0.0,'2nd':0.0,'3rd':0.0,'4th':0.0}, 'False Negative':{'Non-enzyme':0.0,'Zero digit':0.0,'1st':0.0,'2nd':0.0,'3rd':0.0,'4th':0.0}, 'Equality':{'Non-enzyme':0.0,'Zero digit':0.0,'1st':0.0,'2nd':0.0,'3rd':0.0,'4th':0.0}, 'Improvement':{'Non-enzyme':0.0,'Zero digit':0.0,'1st':0.0,'2nd':0.0,'3rd':0.0,'4th':0.0}}
            integrated_data[key_of_this_item]={'False Positive':{'Non-enzyme':[],'Zero digit':[],'1st':[],'2nd':[],'3rd':[],'4th':[]}, 'False Negative':{'Non-enzyme':[],'Zero digit':[],'1st':[],'2nd':[],'3rd':[],'4th':[]}, 'Equality':{'Non-enzyme':[],'Zero digit':[],'1st':[],'2nd':[],'3rd':[],'4th':[]}, 'Improvement':{'Non-enzyme':[],'Zero digit':[],'1st':[],'2nd':[],'3rd':[],'4th':[]}}
            data_array[i][key_of_this_item]={'False Positive':[], 'False Negative':[], 'Equality':[], 'Improvement':[]}
        if line.rstrip().split('\t')[0]=='Annotation Level':
            flag=True
            #print data_array[i][key_of_this_item]
        if flag and line.rstrip().split('\t')[0] in ['Non-enzyme','Zero digit','1st','2nd','3rd','4th']:
            data_row=line.rstrip().split('\t')[1:]
            # retrieve the data row
            #print data_row
            data_array[i][key_of_this_item]['False Positive'].append(float(data_row[0])*float(data_row[4]))
            data_array[i][key_of_this_item]['False Negative'].append(float(data_row[1])*float(data_row[4]))
            data_array[i][key_of_this_item]['Equality'].append(float(data_row[2])*float(data_row[4]))
            data_array[i][key_of_this_item]['Improvement'].append(float(data_row[3])*float(data_row[4]))
        if line=='\n':
            flag=False
    f.close()

import numpy as np
for i in selected_number:
    for specificity in data_array[i]:
        #print specificity
        integrated_data[specificity]['False Positive']['Non-enzyme'].append(data_array[i][specificity]['False Positive'][0]) 
        integrated_data[specificity]['False Positive']['Zero digit'].append(data_array[i][specificity]['False Positive'][1]) 
        integrated_data[specificity]['False Positive']['1st'].append(data_array[i][specificity]['False Positive'][2]) 
        integrated_data[specificity]['False Positive']['2nd'].append(data_array[i][specificity]['False Positive'][3]) 
        integrated_data[specificity]['False Positive']['3rd'].append(data_array[i][specificity]['False Positive'][4]) 
        integrated_data[specificity]['False Positive']['4th'].append(data_array[i][specificity]['False Positive'][5]) 
        integrated_data[specificity]['False Negative']['Non-enzyme'].append(data_array[i][specificity]['False Negative'][0]) 
        integrated_data[specificity]['False Negative']['Zero digit'].append(data_array[i][specificity]['False Negative'][1]) 
        integrated_data[specificity]['False Negative']['1st'].append(data_array[i][specificity]['False Negative'][2]) 
        integrated_data[specificity]['False Negative']['2nd'].append(data_array[i][specificity]['False Negative'][3]) 
        integrated_data[specificity]['False Negative']['3rd'].append(data_array[i][specificity]['False Negative'][4]) 
        integrated_data[specificity]['False Negative']['4th'].append(data_array[i][specificity]['False Negative'][5]) 
        integrated_data[specificity]['Equality']['Non-enzyme'].append(data_array[i][specificity]['Equality'][0]) 
        integrated_data[specificity]['Equality']['Zero digit'].append(data_array[i][specificity]['Equality'][1]) 
        integrated_data[specificity]['Equality']['1st'].append(data_array[i][specificity]['Equality'][2]) 
        integrated_data[specificity]['Equality']['2nd'].append(data_array[i][specificity]['Equality'][3]) 
        integrated_data[specificity]['Equality']['3rd'].append(data_array[i][specificity]['Equality'][4]) 
        integrated_data[specificity]['Equality']['4th'].append(data_array[i][specificity]['Equality'][5]) 
        integrated_data[specificity]['Improvement']['Non-enzyme'].append(data_array[i][specificity]['Improvement'][0]) 
        integrated_data[specificity]['Improvement']['Zero digit'].append(data_array[i][specificity]['Improvement'][1]) 
        integrated_data[specificity]['Improvement']['1st'].append(data_array[i][specificity]['Improvement'][2]) 
        integrated_data[specificity]['Improvement']['2nd'].append(data_array[i][specificity]['Improvement'][3]) 
        integrated_data[specificity]['Improvement']['3rd'].append(data_array[i][specificity]['Improvement'][4]) 
        integrated_data[specificity]['Improvement']['4th'].append(data_array[i][specificity]['Improvement'][5]) 


for specificity in integrated_data:
    for key_of_item in ['Non-enzyme','Zero digit','1st','2nd','3rd','4th']:
        final_result['Average'][specificity]['False Positive'][key_of_item]=np.mean(integrated_data[specificity]['False Positive'][key_of_item])
        final_result['Standard Error'][specificity]['False Positive'][key_of_item]=np.std(integrated_data[specificity]['False Positive'][key_of_item])/np.sqrt(sample_size)
        final_result['Average'][specificity]['False Negative'][key_of_item]=np.mean(integrated_data[specificity]['False Negative'][key_of_item])
        final_result['Standard Error'][specificity]['False Negative'][key_of_item]=np.std(integrated_data[specificity]['False Negative'][key_of_item])/np.sqrt(sample_size)
        final_result['Average'][specificity]['Equality'][key_of_item]=np.mean(integrated_data[specificity]['Equality'][key_of_item])
        final_result['Standard Error'][specificity]['Equality'][key_of_item]=np.std(integrated_data[specificity]['Equality'][key_of_item])/np.sqrt(sample_size)
        final_result['Average'][specificity]['Improvement'][key_of_item]=np.mean(integrated_data[specificity]['Improvement'][key_of_item])
        final_result['Standard Error'][specificity]['Improvement'][key_of_item]=np.std(integrated_data[specificity]['Improvement'][key_of_item])/np.sqrt(sample_size)

print final_result['Average']

import os
os.system('cat /dev/null > %s/result_of_crossVal.txt'%(file_dir)) 
g=open('%s/result_of_crossVal.txt'%(file_dir),'r+')
for specificity in final_result['Average']:
    g.write('///////////////////////////'+'\n')
    g.write('Specificity:  %s'%(specificity)+'\n')
    g.write('Average'+'\t'+'Non-eznyme'+'\t'+'Zero digit'+'\t'+'1st'+'\t'+'2nd'+'\t'+'3rd'+'\t'+'4th'+'\n')
    for key_of_item in ['False Positive','False Negative','Equality','Improvement']:
        item_mean=final_result['Average'][specificity][key_of_item]
        mean_non_enzyme=item_mean['Non-enzyme']
        mean_zero_digit=item_mean['Zero digit']
        mean_first=item_mean['1st']
        mean_second=item_mean['2nd']
        mean_third=item_mean['3rd']
        mean_fourth=item_mean['4th']
        g.write(key_of_item+'\t'+str(mean_non_enzyme)+'\t'+str(mean_zero_digit)+'\t'+str(mean_first)+'\t'+str(mean_second)+'\t'+str(mean_third)+'\t'+str(mean_fourth)+'\n')
    g.write('Standard Error'+'\t'+'Non-eznyme'+'\t'+'Zero digit'+'\t'+'1st'+'\t'+'2nd'+'\t'+'3rd'+'\t'+'4th'+'\n')
    for key_of_item in ['False Positive','False Negative','Equality','Improvement']:
        item_ste=final_result['Standard Error'][specificity][key_of_item]
        ste_non_enzyme=item_ste['Non-enzyme']
        ste_zero_digit=item_ste['Zero digit']
        ste_first=item_ste['1st']
        ste_second=item_ste['2nd']
        ste_third=item_ste['3rd']
        ste_fourth=item_ste['4th']
        g.write(key_of_item+'\t'+str(ste_non_enzyme)+'\t'+str(ste_zero_digit)+'\t'+str(ste_first)+'\t'+str(ste_second)+'\t'+str(ste_third)+'\t'+str(ste_fourth)+'\n')
g.close()        
