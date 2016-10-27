# this script is the main script to construct necessary file for cross_validation

# Basic method: 
# 1. According to the requirement collected, construct a dir under query_dir called "cross_validation", with subdir called sample0/ sample1/ ... according to the number of fold for this cross validation;
# 2. Then, under each subdir, construct the query.dat and reference.dat for one fold of cross-validation
# 3. Then, if "homolog unavailable" scenario is asked, get the source data blast all against all set, use the defined threshold to filter it. Based on it, we can remove some homologs from every references under subdir of "cross_validation" depending on their relevant query sequences.

# 1st step, construct the basic cross validation files
echo "$training_dataset_dir"
echo "$validation_number"
mkdir "$training_dataset_dir""/cross_validation/"
# shuffle the training dataset
cat "$training_dataset" | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' > "$training_dataset".shuffle
python "$SCRIPTPATH"/cross_validation_file_processing/foldVal_dataset_construction.py "$training_dataset".shuffle
rm "$training_dataset".shuffle

# if asked, go on to purify the reference based on blast result
if [ "$homolog_unavailable" = "True" ] ; then
    # 2nd step, purify the source data blast all against all result_hit.py
    echo "$training_dataset_fasta_file"
    python "$SCRIPTPATH"/cross_validation_file_processing/blast_based_ref_filter/blast_filter.py "$training_dataset_fasta_file" "$training_dataset_blastall_file"
    echo "blast file filter finalized !!!"
    cut -f 1,2 "$training_dataset_blastall_file".trim.iden*.queCo* > "$training_dataset_dir"/temp.dat
    # the trimed file resulted from the second step will be used to further purify every reference
    python "$SCRIPTPATH"/cross_validation_file_processing/blast_based_ref_filter/reference_filter.py "$training_dataset_dir"/cross_validation/ "$training_dataset_dir"/temp.dat "$validation_fold" "$validation_number" 
    rm "$training_dataset_dir"/temp.dat "$training_dataset_blastall_file".trim.iden*.queCo*
fi

# start to construct the script for each fold of cross-validation and result evaluation
python "$SCRIPTPATH"/cross_validation_file_processing/parallel_annotation_script_construction.py "$training_dataset_dir"/cross_validation/

# conduct the parallel annotation based on the multiple fold cross validation
bash "$training_dataset_dir"/parallel_annotation.sh
# calculate the average of cross validation
python "$SCRIPTPATH"/cross_validation_file_processing/data_integration_and_average.py "$training_dataset_dir"/result_store/ crossVal_result_evaluation_"$specificity_threshold"_ "$validation_fold" "$validation_number"
mv "$training_dataset_dir"/result_store/result_of_crossVal.txt "$training_dataset_dir"/
