# this file is used to utilize specific_enzyme_ds to purify the reference.dat
# in this case, specific_enzyme_ds_in_string.list is used. it was derived from part1and2 approach with totally 31121 domain signatures

# ////////////////////////
# first of all, trasfter reference.dat into string style
# a processing file temp.dat is retrieved with data structure like:
# proteinID ds1ds2
# proteinID ds1ds3
# ...
python trasfer_ds_to_str.py

# //////////////////////////
# secondly, use specific_enzyme_ds_in_string.list to purify
# purified_protein.list is obtained to further retrieve reference.dat
fgrep -wf specific_enzyme_ds_in_string.list temp.dat |cut -f 1 > purified_protein.list
rm specific_enzyme_ds_in_string.list

# lastly, ok! get the purified_reference.dat 
# in this step, only sequences with specific domain signatures and has at least one EC digit are involved in the purified reference
fgrep -wf purified_protein.list reference.dat |egrep -wv 'EC=-.-.-.-|Non-enzyme' > purified_reference.dat
rm purified_protein.list temp.dat

