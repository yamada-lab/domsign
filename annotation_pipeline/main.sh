# this file is used to use constructed reference to do annotation based on domain signature infomation

# two files are needed

# First one: query.dat
# Description: query data, with data structure in every line like:
# proteinID EC ds1 ds2 ds3 ...
# the domain signature of this query don't have need to be filtered by ds in reference

# Second one: four reference pickle file in one directory called annotation_reference

# The ds not in reference will be annotated as EC:-.-.-.-

# Specificity of 1.0, 0.99, 0.97, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65 will be used to do annotation, respectively
# All the results will be stored in one txt file called 'final_result.txt'

mv annotation_reference/*pickle ../annotation_pipeline/ # change the location of reference pickle file to be accessed by python program
python ds_based_enzyme_anno_protocol.py
rm *pickle

# if it is prediction, then here is the last step and we mv the predicted file back to the query directory
#cp *.dat "$query_dir"/"$output_file_name"    
specificity_threshold_temp=$(echo "$specificity_threshold * 100" | bc)
specificity_threshold_integer=${specificity_threshold_temp%.*}
mv result_with_specificity_"$specificity_threshold_integer".dat "$output_file"
