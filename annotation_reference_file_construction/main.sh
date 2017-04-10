# this file is used to form annotation_referrence_file from an original gene_ID, EC number, domain signature file
# it is devide into several parts
# the input file name is reference.dat with data structure like:
# proteinID ec ds1 ds2 ds3 ...

# Part0: purify reference.dat by specific_enzyme_ds (remove Non-enzyme, EC=-.-.-.- and those beyond the specific enzyme domain signatures)
python purify_reference.py
rm reference.dat specific_enzyme_ds_in_string.list
mv purified_reference.dat reference.dat  # rename new processing file

# //////////////////////////
# Part1: convert to reference.dat.formated
# ec1\td1\td2
# ec2\td1
# Among them, the proteins with multiple EC numbers are divided into several sub EC group here.
python reference_format.py reference.dat
rm reference.dat

# //////////////////////////
# Part2: construct basic ec-domain signature dictionary and move them to corresponding directory
python associate_domain_ec.py reference.dat.formated
rm reference.dat.formated
mv ec_domain_1_pickle first_level/
mv ec_domain_2_pickle second_level/
mv ec_domain_3_pickle third_level/
mv ec_domain_4_pickle fourth_level/

# /////////////////////////
# Part3: construct annotation reference and stack them into one directory called annotation_reference
mkdir annotation_reference
cd first_level/
python machine_learning_model.py
mv domain_signature_ec_dic_1st_pickle ../annotation_reference/
rm *pickle
cd ../second_level/
python machine_learning_model.py
cp domain_signature_ec_dic_2nd_pickle ../annotation_reference/
rm *pickle
cd ../third_level/
python machine_learning_model.py
cp domain_signature_ec_dic_3rd_pickle ../annotation_reference/
rm *pickle
cd ../fourth_level/
python machine_learning_model.py
cp domain_signature_ec_dic_4th_pickle ../annotation_reference/
rm *pickle

cd ../
mv  annotation_reference/ ../annotation_pipeline/
