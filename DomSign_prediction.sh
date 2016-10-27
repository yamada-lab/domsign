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
# ./DomSign.prediction.sh -i ~/domsign/example_prediction/query.dat -r ~/domsign/example_prediction/reference.dat -e ~/domsign/example_prediction/specific_enzyme_ds_in_string.list -s 0.95 -o ~/domsign/example_prediction/nimei95

# /////////////////////////////////
# /////////////////////////////////

# get the absolute path of DomSign tool without the last '/'
SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd -P )  
export SCRIPTPATH

# -i input data in a defined absolute directory
# -r the reference used
# -e specific enzyme signature
# -s specificity threshold used in this annotation
# -o output file

while getopts "i:r:e:s:o:" arg
do
        case $arg in
             i)
                printf "input data in a defined absolute directory, about the format, see readme.txt:  "
                echo $OPTARG
                query_file=$OPTARG
                echo $query_file
                export query_file
                ;;
             r)
                printf "reference data in a defined absolute directory, about the format, see readme.txt:  "
                echo $OPTARG
                reference_file=$OPTARG
                echo $reference_file
                export reference_file
                ;;
             e)
                echo "specific enzyme signature a defined absolute directory, about the format, see readme.txt:  "
                echo $OPTARG
                specific_enzyme_signature_file=$OPTARG
                echo $specific_enzyme_signature_file
                export specific_enzyme_signature_file
                ;;
             s)
                printf "specificity threshold used in this annotation, which should be >=0.5 and <=1.0:  "
                echo $OPTARG
                specificity_threshold=$OPTARG
                echo $specificity_threshold
                export specificity_threshold
                ;;
             o)
                printf "output file:   "
                echo $OPTARG
                output_file=$OPTARG
                echo $output_file
                export output_file
                ;;
        esac
done

# copy the query to the working directory
cp "$query_file" "$SCRIPTPATH""/working_directory/query.dat"

# cd to the working directory and ready to go
cd "$SCRIPTPATH""/working_directory/"


# now 1.0 part starts:
cp "$reference_file" ../annotation_reference_file_construction/reference.dat
cp "$specific_enzyme_signature_file" ../annotation_reference_file_construction/purify_reference/specific_enzyme_ds_in_string.list
cd ../annotation_reference_file_construction/
bash main.sh
cd ../
cp working_directory/query.dat annotation_pipeline/

# /////////////////////////////////
# now 2.0 part starts:
cd annotation_pipeline/
bash main.sh
cd ../
