# use specific_enzyme_ds_in_string.list to purify
# and, output has at least one EC digit

import argparse

parser = argparse.ArgumentParser(
        prog='purify_reference.py'
        )
parser.add_argument('-o', dest='output', required=True)
parser.add_argument('-r', dest='reference_data', required=True)
parser.add_argument('-e', dest='specific_enzyme', required=True)
args = parser.parse_args()


def lst_trans_str(lst):
    lst.sort()
    ds_in_str=''
    for item in lst:
        ds_in_str+=item
    return ds_in_str


def main():
    g=open(args.output,'w')

    specific_enzyme=[]
    for line in open(args.specific_enzyme, 'r'):
        specific_enzyme.append(line.strip())
    
    for line in open(args.reference_data, 'r'):
        row=line.rstrip().split('\t')
        ec=row[1]
        if ec=='EC=-.-.-.-' or ec=='Non-enzyme':
            continue
        ds_lst=row[2].split(',')
        ds_str=lst_trans_str(ds_lst)
        if ds_str in specific_enzyme:
            g.write(row[1]+'\t'+'\t'.join(ds_lst)+'\n')
    
    g.close()


if __name__ == '__main__':
    main()
