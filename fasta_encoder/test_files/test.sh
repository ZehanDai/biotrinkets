### encoder
#test_dir=/mnt/e/Yulab/03TApipeline/biotrinkets/fasta_tools/test_files
test_dir=/mnt/e/Scripts/python/biotrinkets/biotrinkets/fasta_encoder/test_files 
test_oud=$test_dir/output
mkdir -p $test_oud

infile=$test_dir/test_TADB2-typeI_AT.fna
mapfile=$test_oud/test_encode_map.tsv
outfile=$test_oud/test_encode_map.fa
#python3 -m fasta_encoder -h
python3 -m fasta_encoder -m encode -i $infile -o $outfile -e $mapfile -p "sequence" # fasta header changed to sequence1, sequence2, ... sequenceN 
head $outfile -n 3 
echo 
echo 
 

python3 -m fasta_encoder -m encode -i $infile -o $outfile -e $mapfile -f 20 # replace the original headers to the N letters of the old ones
head $outfile -n 3
echo 
echo 

python3 -m fasta_encoder -m encode -i $infile -o $outfile -e $mapfile -F 1 # replace the original headers to the first letter of the old ones
head $outfile -n 3
echo
echo

### decoder
infile=$outfile
outfile=$test_oud/test_decode_map.fa
mapfile=$test_oud/test_encode_map.tsv
python3 -m fasta_encoder -m decode -i $infile -e $mapfile -o $outfile 
head $outfile 
echo
echo 

