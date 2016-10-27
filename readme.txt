# /////////////////////////////////////////////////////////
# What is this?
# The script package is a machine learning tool termed with "DomSign". (about
# algorithm, see )
# To narmally run this tool in your own machine, we hypothesize that you are
# in a normal linux environment and python 2.8+ is also well installed.
# The basic function of this tool is to hierarchically predict the EC number
# of enzymes through the machine learning approach based on Pfam-A domain
# signatures
# Considering about the expansion, this script is designed to be generalized
# to other machine learning input labels. In this case, other protein
# signatues can be also involved here.  However, only Pfam-A domain signature
# based training dataset is provided here in package. In all other cases, the
# users need to prepare their own training dataset according to the  basic
# data format requirement as shown below. Thus, theoretically, if the input
# labels are in an unified system (in our work, Pfam-A domain signatures) in
# both query and reference  (training) dataset, they can be used to predict
# the EC numbers by the script in this package.
# Hence, here we define an unified protein signature system consisted of k
# signatures (Sign-i, i=1~k). This protein signature system is used for
# prediction in machine learning. In our work, we utilize Pfam-A domain
# signatures as a specific signature system. This system extract Pfam-A
# (version 26.0) domain signatures for every protein, which means Pfam-A
# domain architecture without considering domain order or recurrence.


# /////////////////////////////////////////////////////////
# This machine learning model consist of two steps. 

# ////////////////////////////////////////
# The first step is to differentiate between non-enzymes and enzymes. In this
# step, one file called "specific enzyme signature" is in need. This dataset
# should be organized in   a format like this:

# Sign-iSign-jSign-l\n
# Sign-iSign-l\n
# ...
 
# All of the signatures above is personally defined by users to represent
# enzymes rather than non-enzymes. And each signature should be sorted
# according to the default python list sort command (according to the alphabet
# seqeunces of the charactors). About the construction method for this dataset
# in Pfam-A domain signatures, please check   .
 
# /////////////////////////////////////////
# The second step is machine learning approach to predict the EC number
# hierarchically. In this step, one file called "training dataset" is in need.
# This dataset should be organized in a format like this:

# proteinID\tEC1,EC2\tSign-i,Sign-j,Sign-l\n
# proteinID\tEC1\tSign-i\n
# proteinID\tEC2\tSign-i,Sign-j\n
# ...

# Here, each EC number should be organized as the complete four-digit
# (EC=x.x.x.x) or incomplete (EC=x.x.-.-) or "Non-enzyme" format. The protein
# signature system should be the same  as that used in the first step.

# /////////////////////////////////////////////////////////////
# This package has two main functions: prediction and cross-validation

# ///////////////////////////////////////////
# For prediction 
# You should provide three files, query, "specific enzyme signature" as
# described in the first step and "training dataset" as described in the
# second step.
# All these three files should use one unified protein signature system.
# Meanwhile, for Pfam-A protein signature system, we have provide one
# "training dataset" called "    " under the directory of
# working_direcotry/reference/ of this package.
# Likewise, we also provide one "specific enzyme domain signature" called "
# " under the directory of working_direcotry/reference/ of this package. 
# For query data, it should be organized in this format:
# proteinID\tSign-i,Sign-j,Sign-l\n
# proteinID\tSign-j\n
# proteinID\tSign-l\n
# ...

# For this function, we need to type in a command like.
# dir/DomSing.tool/DomSign.prediction.sh -i dir/query -r dir/"traning_dataset"
# -e "specific_enzyme_signature" -s (specificity threshold, a number between
# 0.5   to 1.0, default 0.8. About details, see     ) -o dir/output_file

# The output file will be also located in the query directory with data format
# proteinID\tEC1\n
# proteinID\tEC2\n
# ...
# Here also we have the complete four-digit (EC=x.x.x.x) or incomplete
# (EC=x.x.-.-) or "Non-enzyme" format for every EC shown above.


# ////////////////////////////////////////////
# For cross-validation
# Perhaps you are interested in developing another kind of protein signature
# system to predict enzyme function, or you just want to simply reproduce some
# of the results in our paper. In both cases, you'd better have some
# cross-validation on a reliable dataset.
# This function is a little bit different from prediction. First of all, you
# need to prepare two basic files and two additional files.
# Two basic files include the "training dataset"  and "specific enzyme
# signature" which have all the same format with that in prediction module. 
# If you want to have the test in a so-called "homolog unavailable" scenario,
# which means to remove some query homolog from the reference in every fold of
# cross-validation to simula  te the situation where simple blast doesn't work
# well, you need to prepare another two additional files: the "training
# dataset blast all against all" file (-outfmt 6) and "trainin  g
# dataset.fasta" file. For the former one, the format should be derived from
# standard blast or blast+ package -outfmt 6 format. For the second one, this
# fasta file should be in ei  ther nucleotide or amino acid format according
# to the format used in "training dataset blast all against all" file. 

# For this function, we need to type in a command like.
# dir/DomSing.tool/DomSign.crossVal.sh -r dir/"traning_dataset" -e
# "specific_enzyme_signature" -s (specificity threshold, a num  ber between
# 0.5 to 1.0, default 0.8. About details, see     ) -o output_file_name -f
# (fold of cross-validation) -m (number of fold conducted, for example, you
# set 1000-fold cross   validation, then you can choose here to only conduct
# 100 of them)
# Then, the program will ask you whether test in "homolog unavailable"
# scenario or not. If so, we need to provide the two additioanl files and
# their absolute path from keyboard. 
# Subsequently, the threshold (query coverage and identity) of balst based
# reference purification will also be asked to type in from keyboard. 

# Finally, one txt file will be processed to the query directory, providing
# all the performance information in this cross-validation test. The
# evaluation is based on a statistical hierarchical metric system designed in   
# . This system is designed to provide high-resolution result evaluation for 
# hierarchical labels such as EC number.


# /////////////////////////////////////////////
# For any content question, please contact
# For any technique question, please contact wtm0217@gmail.com
# This tool is developed by Kurokawa&Nakashima&Yamada lab in Tokyo Institute
# of Technology and released as additional file in publication ""
# All rights reserved
