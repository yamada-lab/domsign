# this file is used to put domain info and ec number info together
# 1. input file with data structure like this:
#    EC ds1 ds2 ds3 ...

# 2. output file is in four pickle files with data structure 
#    {ds1:[EC1,EC2, ...]}
#    for every hierarchy level
#    EC=x, EC=x.x, EC=x.x.x, EC=x.x.x.x

# the basic method: in situ form data structure like above. Firstly, some ec has '-', 'x.-.-.-' only to first level, 'x.x.-.-' to first and second level, as it continue
# use ec_x to store ec in this level, if ec not in ec_list, creat a new key ec, point to [], if not, append to existing [] 


import argparse,pickle

parser = argparse.ArgumentParser(
        prog='purify_reference.py'
        )
parser.add_argument('-i', dest='input_filename', required=True)
parser.add_argument('-o', dest='output_directry', required=True)
parser.add_argument('-s', dest='session_id', required=True)
args = parser.parse_args()


def list_str_trans(lst):  # this is used to transfer list of domain signature to string so that it can be made as a dic
    name=''
    lst.sort()
    for i in lst:
        name+=i
    return name

def get_relevant_ec(ec_name,level):  # extract ec number at hierarchical level
    row=ec_name.split('.')
    if level==1:
        return row[0]
    elif level==2:
        return row[0]+'.'+row[1]
    elif level==3:
        return row[0]+'.'+row[1]+'.'+row[2]
    elif level==4:
        return row[0]+'.'+row[1]+'.'+row[2]+'.'+row[3]


def main():
    fourth_ds_ec={}
    first_ds_ec={}
    second_ds_ec={}
    third_ds_ec={}
    f=open(args.input_filename,'r')
    dom_1=[]  # list to store different level ec number
    dom_2=[]
    dom_3=[]
    dom_4=[]
    for line in f:  # put ec into 
        row=line.rstrip().split('\t')
        domain=list_str_trans(row[1:])
        ec=row[0]
        if len(ec.split('-'))==1:   # when it has no '-', in other words, like 'EC=x.x.x.x'
            if domain not in dom_4:
                fourth_ds_ec[domain]=[get_relevant_ec(ec,4)]
                dom_4.append(domain)
            else:
                fourth_ds_ec[domain].append(get_relevant_ec(ec,4))
            if domain not in dom_3:
                third_ds_ec[domain]=[get_relevant_ec(ec,3)]
                dom_3.append(domain)
            else:
                third_ds_ec[domain].append(get_relevant_ec(ec,3))
            if domain not in dom_2:
                second_ds_ec[domain]=[get_relevant_ec(ec,2)]
                dom_2.append(domain)
            else:
                second_ds_ec[domain].append(get_relevant_ec(ec,2))
            if domain not in dom_1:
                first_ds_ec[domain]=[get_relevant_ec(ec,1)]
                dom_1.append(domain)
            else:
                first_ds_ec[domain].append(get_relevant_ec(ec,1))
        elif len(ec.split('-'))==4:     # the lowest level for this ec is only 1st
            if domain not in dom_1:
                first_ds_ec[domain]=[get_relevant_ec(ec,1)]
                dom_1.append(domain)
            else:
                first_ds_ec[domain].append(get_relevant_ec(ec,1))
        elif len(ec.split('-'))==3:     # the lowest level for this ec is only 2nd
            if domain not in dom_2:
                second_ds_ec[domain]=[get_relevant_ec(ec,2)]
                dom_2.append(domain)
            else:
                second_ds_ec[domain].append(get_relevant_ec(ec,2))
            if domain not in dom_1:
                first_ds_ec[domain]=[get_relevant_ec(ec,1)]
                dom_1.append(domain)
            else:
                first_ds_ec[domain].append(get_relevant_ec(ec,1))
        elif len(row[0].split('-'))==2:   # the lowest level for this ec is only 3rd
            if domain not in dom_3:
                third_ds_ec[domain]=[get_relevant_ec(ec,3)]
                dom_3.append(domain)
            else:
                third_ds_ec[domain].append(get_relevant_ec(ec,3))
            if domain not in dom_2:
                second_ds_ec[domain]=[get_relevant_ec(ec,2)]
                dom_2.append(domain)
            else:
                second_ds_ec[domain].append(get_relevant_ec(ec,2))
            if domain not in dom_1:
                first_ds_ec[domain]=[get_relevant_ec(ec,1)]
                dom_1.append(domain)
            else:
                first_ds_ec[domain].append(get_relevant_ec(ec,1))
    f.close()
    
    pickle.dump(first_ds_ec,open(args.output_directry+'/ec_domain_1st_pickle_'+args.session_id,'wb'))
    pickle.dump(second_ds_ec,open(args.output_directry+'/ec_domain_2nd_pickle_'+args.session_id,'wb'))
    pickle.dump(third_ds_ec,open(args.output_directry+'/ec_domain_3rd_pickle_'+args.session_id,'wb'))
    pickle.dump(fourth_ds_ec,open(args.output_directry+'/ec_domain_4th_pickle_'+args.session_id,'wb'))


if __name__ == '__main__':
    main()
