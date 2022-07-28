# Biotrinkets: a collection of small utils for bioinformatics

* [Introduction](#introduction)
* [Version](#version)
* [Requirement](#requirement)
* [Installation](#installation)
* [Usage](#usage)

## Introductioon
 
This package implemented some small utils for bioinformatic analysis. In this version of release, only those for fasta file manipulation were included, these include, but no limitted to split long scaffold files to shorted contigs by Ns, simplify long and complicated fasta headers to simple ones, subset regions from a batch of sequences with or without flanks. More functions will be added in the future. 

 
## Version
+ Biotrinkets 0.2 (tested on WSL Ubuntu 18 and Ubuntu 20)


## Requirement
------------
+ Python 3.8.3 / 3.6.9 (should work >= 3.6)
+ pandas 1.3.4 (no tested in other version)


## Installation
Just simply ``pip install .`` or ``pip3 install .`` under the biotrinkets path.


## Usage

calculate sequence size 
`test_dir=/mnt/e/Scripts/python/biotrinkets/biotrinkets/fasta_tools/test_files # input folder
test_oud=$test_dir/output # output folder 
mkdir -p $test_oud

infile=$test_dir/test.splitN.fa # input file
outfile=$test_oud/test_size.tsv # output file 
python3 -m fasta_tools -m get_size -i $infile -o $outfile`


extract sequence
`infile=$test_dir/test.splitN.fa
outfile=$test_oud/test_extract.fa
echo seq1 seq2 seq3 seq4 seq5 | tr ' ' $'\n' > seqid.lst # create a sequence id list for extraction
python3 -m fasta_tools -m extract -i $infile -o $outfile -l seqid.lst`
`


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


# get flank, extent version of subset, output include flanks of the regions you want to extractregfile=seq_reg.tsv
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


