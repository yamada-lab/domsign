#////////////////////////////////
# this script is used to conduct cross validation on a given source dataset
# input: a source dataset with data structure like
# proteinID\tEC1\tDomain1,Domain2
# EC can be "EC=x.x.x.x" or "Non-enzyme"
# Domain should be Pfam-A domain or any other unified signatures (e.g InterProt signatures)

# Steps:
# 1. we construct the samples for cross-validation under the directory of query directory
# 2. If the user ask for a "homolog unavailable" scenario based test, we ask for two additional files, source data balst all agaisnt all (-outfmt 6) and source.fasta file to remove #    homolog of queries from reference for each fold of cross-validation
# 3. further, DomSign.prediction.sh is called for relevant times to conduct cross-validation
# 4. the result will be averaged and the standard error and standard deriative will also be given

# the source data set should be organized as 
# proteinID\tEC1,EC2\tDomain1,Domain2
# EC can be "EC=x.x.x.x" or "Non-enzyme"
# Domain should be Pfam-A domain or any other unified signatures (e.g InterProt signatures)

# the source data blast all against all data should be in the format of -outfmt 6
# the fasta file should be protein or dna fasta file according to the file used in blast

# Example:
# ./DomSign.crossVal.sh -t ~/domsign/example_crossVal/sprot_noenz_oneec_with_domain.dat -e ~/domsign/example_prediction/specific_enzyme_ds_in_string.list -s 0.95 -f 10 -m 10

# /////////////////////////////////
# /////////////////////////////////

# get the absolute path of DomSign tool without the last '/'
SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd -P )  
export SCRIPTPATH

# -t training dataset in a defined absolute directory
# -e specific enzyme signature a defined absolute directory
# -s specificity threshold used in this annotation
# -f fold of cross validation
# -m number of actually conducted validation

while getopts "t:e:s:f:m:" arg
do
        case $arg in
             t)
                echo "training dataset in a defined absolute directory, about the format, see readme.txt:  "
                echo $OPTARG
                training_dataset=$OPTARG
                export training_dataset
                ;;
             e)
                echo "specific enzyme signature a defined absolute directory, about the format, see readme.txt:  "
                echo $OPTARG
                specific_enzyme_signature_file=$OPTARG
                export specific_enzyme_signature_file
                ;;
             s)
                echo "specificity threshold used in this annotation, which should be >=0.5 and <=1.0:  "
                echo $OPTARG
                specificity_threshold=$OPTARG
                export specificity_threshold
                ;;
             f)
                echo "fold of cross validation:   "
                echo $OPTARG
                validation_fold=$OPTARG
                export validation_fold
                ;;
             m)
                echo "number of actually conducted validation:   "
                echo $OPTARG
                validation_number=$OPTARG
                export validation_number
                ;;
        esac
done

# the absolute directory of the training dataset will be also specified there
training_dataset_dir=${training_dataset%/*}
export training_dataset_dir

# ask the user whether to use the "homolog unavailable" scenario or not
echo "Please type in whether you'd like to conduct this test in a homolog unavailable scenario (yes or no)"
printf "Please type in (yes or no):    "
read flag 
homolog_unavailable="blank"
if [ "$flag" = "yes" ] ; then
    homolog_unavailable="True"
    echo "Now we need two additional files for homolog unavailable cross validation"
    echo "Please type in the path access to the training data blast all against all file in outfmt 6"
    printf "Please type in: "
    read training_dataset_blastall_file 
    export training_dataset_blastall_file 
    echo "Please type in the path access to the training data fasta file"
    printf "Please type in: "
    read training_dataset_fasta_file
    export training_dataset_fasta_file
elif [ "$flag" = "no" ] ; then
    homolog_unavailable="False"
else
    echo "incorrect input!!"
fi
export homolog_unavailable

# conduct the cross-validation
if [ "$homolog_unavailable" != "blank" ] ; then
    bash "$SCRIPTPATH"/cross_validation_file_processing/main.sh
fi
