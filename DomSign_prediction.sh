# ////////////////////////////////
# this file is for DomSign engine to annotate enzyme EC number from Pfam-A domain signature by machine learning
# it is divided into two parts
# 1.0 the construction of machine learning model: 
#     Input: "reference.dat" 
#     Output: Four annotation files on four-digit EC number level as the reference for the annotation. "domain_signature_ec_dic_uniprot_1st_pickle", "domain_signature_ec_dic_uniprot
#             _2nd_pickle", "domain_signature_ec_dic_uniprot_3rd_pickle", "domain_signature_ec_dic_uniprot_4th_pickle"

# 2.0 the annotation pipeline and the following results show:
#     Input: the output of 1.0 and 2.0 will be used to do annotation

# Directory of files:
# under the main directory of this pipeline (domain_signature_based_enzyme_annotation_pipeline), we have three directories:

# 1.0 annotation_referrence_file_construction
#     Usage: for the conduction of program from part 1.0

# 2.0 annotation_pipeline
#     Usage: for the conduction of program from part 3.0

# 3.0 working directory
#     Usage: many processing will be conducted under this directory

# data structure requirement:

# query dataset
# proteinID\tDomain1
# proteinID\tDomain1,Domain2
# Domain here can be any unified protein signatures, not limiting to Pfam-A domains

# reference dataset
# proteinID\tEC1,EC2\tDomain1
# proteinID\tEC1\tDomain1,Domain2
# EC should be as EC=x.x.x.x (complete) or EC=x.x.-.- (incomplete) or "Non-enzyme"
# Domain should be the same as the query file
# you can also use the Swiss-Prot enzyme reference provided under the directory working_directoty/reference/

# Example
# ./DomSign_prediction.sh -i ~/domsign/example_prediction/query.dat -r ~/domsign/example_prediction/reference.dat -e ~/domsign/example_prediction/specific_enzyme_ds_in_string.list -t 0.95 -o ~/domsign/example_prediction/nimei95 -s 1

# /////////////////////////////////
# /////////////////////////////////

# get the absolute path of DomSign tool without the last '/'
cd `dirname $0`
DOMSIGN_ROOT=`pwd -P`

# -i input data in a defined absolute directory
# -r the reference used
# -e specific enzyme signature
# -s specificity threshold used in this annotation
# -o output file

while getopts "i:r:e:t:o:s:" arg
do
        case ${arg} in
             i)
                printf "input data in a defined absolute directory, about the format, see readme.txt:  "
                echo ${OPTARG}
                query_file=${OPTARG}
                ;;
             r)
                printf "reference data in a defined absolute directory, about the format, see readme.txt:  "
                echo ${OPTARG}
                reference_file=${OPTARG}
                ;;
             e)
                echo "specific enzyme signature a defined absolute directory, about the format, see readme.txt:  "
                echo $OPTARG
                specific_enzyme_signature_file=${OPTARG}
                ;;
             t)
                printf "specificity threshold used in this annotation, which should be >=0.5 and <=1.0:  "
                echo ${OPTARG}
                specificity_threshold=${OPTARG}
                ;;
             o)
                printf "output file:   "
                echo ${OPTARG}
                output_file=${OPTARG}
                ;;
             s)
                printf "session ID manage multiple jobs:  "
                echo ${OPTARG}
                session_id=${OPTARG}
                ;;
        esac
done


############## now 1.0 part starts:
# it is devide into several parts
# the input file name is reference.dat with data structure like:
# proteinID ec ds1 ds2 ds3 ...

# Part0: purify reference.dat by specific_enzyme_ds (remove Non-enzyme, EC=-.-.-.- and those beyond the specific enzyme domain signatures)
# Part1: convert to reference.dat.formated
# ec1\td1\td2
# ec2\td1
# Among them, the proteins with multiple EC numbers are divided into several sub EC group here.
python ${DOMSIGN_ROOT}/src/python/purify_reference.py -o ${DOMSIGN_ROOT}/tmp/reference_${session_id}.dat -r ${reference_file} -e ${specific_enzyme_signature_file}

# Part2: construct basic ec-domain signature dictionary and move them to corresponding directory
python ${DOMSIGN_ROOT}/src/python/associate_domain_ec.py -i ${DOMSIGN_ROOT}/tmp/reference_${session_id}.dat -o ${DOMSIGN_ROOT}/tmp -s ${session_id}

# Part3: construct annotation reference and stack them into one directory called annotation_reference
python ${DOMSIGN_ROOT}/src/python/machine_learning_model.py -d ${DOMSIGN_ROOT}/tmp -l 1st -s ${session_id}
python ${DOMSIGN_ROOT}/src/python/machine_learning_model.py -d ${DOMSIGN_ROOT}/tmp -l 2nd -s ${session_id}
python ${DOMSIGN_ROOT}/src/python/machine_learning_model.py -d ${DOMSIGN_ROOT}/tmp -l 3rd -s ${session_id}
python ${DOMSIGN_ROOT}/src/python/machine_learning_model.py -d ${DOMSIGN_ROOT}/tmp -l 4th -s ${session_id}



################ now 2.0 part starts:
# two files are needed

# First one: query.dat
# Description: query data, with data structure in every line like:
# proteinID EC ds1 ds2 ds3 ...
# the domain signature of this query don't have need to be filtered by ds in reference

# Second one: four reference pickle file in one directory called annotation_reference

# The ds not in reference will be annotated as EC:-.-.-.-

# Specificity of 1.0, 0.99, 0.97, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65 will be used to do annotation, respectively
# All the results will be stored in one txt file called 'final_result.txt'
python ${DOMSIGN_ROOT}/src/python/ds_based_enzyme_anno_protocol.py -q ${query_file} -d ${DOMSIGN_ROOT}/tmp -t ${specificity_threshold} -s ${session_id} -o ${output_file}


################ Remove temporally files
rm ${DOMSIGN_ROOT}/tmp/reference_${session_id}.dat
rm ${DOMSIGN_ROOT}/tmp/ec_domain_*_pickle_${session_id}
rm ${DOMSIGN_ROOT}/tmp/domain_signature_ec_dic_*_pickle_${session_id}
