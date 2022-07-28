#!/bin/bash


test_dir=/mnt/e/Scripts/python/biotrinkets/biotrinkets/fasta_tools/test_files
test_oud=$test_dir/output
mkdir -p $test_oud 

# calculate sequence size 
#infile=$test_dir/test_TADB2-typeI_AT.fna
infile=$test_dir/test.splitN.fa
outfile=$test_oud/test_size.tsv
python3 -m fasta_tools -m get_size -i $infile -o $outfile
echo 

exit 


# extract sequence
infile=$test_dir/test.splitN.fa 
outfile=$test_oud/test_extract.fa
echo seq1 seq2 seq3 seq4 seq5 | tr ' ' $'\n' > seqid.lst # sequence id list
python3 -m fasta_tools -m extract -i $infile -o $outfile -l seqid.lst
echo
  

# subset sequence
# create a subset table for subseting 
outfile=$test_oud/test_subset.fa
echo seq1 seq2 seq3 seq4 seq5 | tr ' ' $'\n' > tmp1
echo 1 1 1 1 1 | tr ' ' $'\n' > tmp2
echo 10 10 10 10 10 | tr ' ' $'\n' > tmp3
paste tmp1 tmp2 tmp3 > seq_reg.tsv # region of query sequence to subset
python3 -m fasta_tools -m subset -i $infile -o $outfile -t seq_reg.tsv 
rm tmp1 tmp2 tmp3
echo 


# get flank, extent version of subset, output include flanks of the regions you want to extract
regfile=seq_reg.tsv
infile=$test_dir/test.splitN.fa
outfile=$test_oud/test_subset-flank.fa
python3 -m fasta_tools -m get_flank -i $infile -o $outfile -t seq_reg.tsv -f 10
echo 


# formatter 
infile=$test_dir/test_TADB2-typeI_AT.fna # the width of the sequence is 60
outfile=$test_oud/test_formatted.tsv 
python3 -m fasta_tools -m formatter -i $infile -o $outfile -w 100
echo 

 
# splitN 
infile=$test_dir/test.splitN.fa 
outfile=$test_oud/test_split.fa
python3 -m fasta_tools -m splitN -i $infile -o $outfile -n 10 -S 100
# -n num_cut: minimum total N threshold to split
# -S size_cut: minimum size of sequence to keep
echo 

