#!/usr/bin/python3


"""
Description: simplify long and complicated fasta headers
version: v0.3.1
Update: 2022-6-22 
        move "try mapFile" test from main() to initial test 

"""

import os
import sys
import getopt

from fasta_tools.formatter import * 
from fasta_tools.__main__ import parse,headd


# parse arguments
def usage():
    print('Usage:\n  python3 fasta_encoder.py [-m mode] [-i infile.fa] [-e encode_map.tsv] [-p seq ] [ -f 10 ] [ -F 1 ]')
    print('  python3 fasta_encoder.py -m encode -i $inf -e encode_map -p "sequence"')
    print('  python3 fasta_encoder.py -m decode -i $inf -e encode_map -f 10\n')
    print('\n'.join([ 
        "Main parameters\n",
        "    -i input fasta\n",
        "    -o output fasta\n",
        "    -m mode ['encode' or 'decode']\n"
        "        encode mode simplify the headers and decode reconvert the simplifier to the originals\n",
        "        encode mode writes encode map file to tmp_dir/encode.tsv by default\n",
        "        decode mode reads encode map file encode.tsv in tmp_dir, or accepts a map file in customized path\n",
        "    -e encode map file\n",
        "        encode map format:\n",
        "            #original\tsimplified\n",
        "           long_header\tshort_header\n",
        "    Header format\n",
        "        -p header format, 'seq1, seq2, seq3'\n",
        "        -f using the first N letters as header, conclict with -p,\n",
        "        -F using the first word as header (space as delimitter) (default)"]))
    print(''.join([
        'Modes:\n'
        '  encode: simplify long header\n',
        '  decode: reconvert simplifier headers to the originals \n']))


opts,argv = getopt.getopt(sys.argv[1:],'-i:-o:-m:-e:-p:-f:-F:-h')
mode_lst = ['encode','decode']

for opt_n,opt_v in opts:
    if opt_n in ('-h'):
        usage()
        exit()
        
i = 0
#print('opts',opts)
 
for opt_n,opt_v in opts:
    if opt_n == '-i':
        infile = opt_v
    elif opt_n == '-o':
        outfile = opt_v            
    elif opt_n == '-m':
        mode = opt_v             
        if mode not in mode_lst:
            print(mode_lst)
            raise Exception('Mode given is not in predefined list')
    elif opt_n == '-e':
        global mapFile
        mapFile = opt_v
    elif opt_n == '-p':
        i += 1
        prefix = opt_v
        hder_format= 'prefix' 
    elif opt_n == '-f':
        i += 1
        firstNletter = opt_v
        hder_format = 'letter'    
    elif opt_n == '-F':
        i += 1
        firstNword = opt_v
        hder_format = 'word'

#print('mapFile',mapFile)
try:
    mapFile
except:
    #raise ValueError()
    mapFile = 'tmp_dir/encode.tsv'
    if os.path.exists('tmp_dir') is False:
        os.makedirs('tmp_dir')


if (i > 1):
    raise Exception('More than 1 header formater parameters have been given')

try:
    hder_format
    if hder_format == 'word':
        value = firstNword
    elif hder_format == 'letter':
        value = firstNletter
    elif hder_format == 'prefix':
        value = prefix
except:
    hder_format = 'word' # set as default if not given
    value = 1 # use the first word as simplified header
    print('  header format was not given, specify as "word" ')

#############################################

def tofile(odict='', maplist='', outfile='', mapFile='', wmode='wmode' ):
    # wmode: writting mode, [ 'encode', 'decode' ]
    #   encode: write a fasta file AND a map file 
    #   decode: write a fasta file
    if  wmode == 'encode' :
        olst = [ '>'+key+'\n'+val for key,val in odict.items() ]
        with open(outfile,'w') as ouf:
            ouf.write( '\n'.join(olst))

        with open(mapFile,'w') as ouf:
            ouf.write( '\n'.join(maplist) )
        print('output written to file:', outfile)
        print('encode tsv written to file:', mapFile)
    elif wmode == 'decode':
        olst = [ '>'+key+'\n'+val for key,val in odict.items() ]
        with open(outfile,'w') as ouf:
            ouf.write( '\n'.join(olst))
        print('output written to file:', outfile)


def simplify(indict, hder_format, value):
    """
    Header format
        -p header format, "seq1, seq2, seq3"
        -f using the first N letters as header, conclict with -p
        -F using the first word as header (space as delimitter) (default)
    format should be one of [ 'word', 'letter', 'prefix' ]
    value: value of the format, 
           must be numeric for word and letter mode, 
           must be string for prefix 
    """
    key_lst = list(indict.keys())
    odict = {} 
    map_lst = []
    if hder_format == 'word':
        for key in key_lst:
            seq = indict[key].replace('\n','')
            nkey = str(key).split(' ')[0: int(value)]
            nkey = ' '.join(nkey)
            odict[nkey] = seq 
            map_lst.append('\t'.join([key,nkey]))
    elif hder_format == 'letter':
        for key in key_lst:
            seq = indict[key].replace('\n','')
            nkey = str(key)[0: int(value)]
            odict[nkey] = seq
            map_lst.append('\t'.join([key,nkey]))
    elif hder_format == 'prefix':
        i = 0 
        for key in key_lst:
            i += 1
            seq = indict[key].replace('\n','')
            nkey = str(value) + str(i)
            odict[nkey] = seq
            map_lst.append('\t'.join([key,nkey]))
    return odict,map_lst 

def decode(indict, mapFile):

    with open(mapFile,'r') as mapF:
        map_tsv = mapF.readlines()
    mdict = {}
    for line in map_tsv:
        line = line.split('\t')
        mdict[ line[1].replace('\n','')] = line[0]
    
    odict = {}
    key_lst = list(indict.keys())
    for key in key_lst:
        seq = indict[key].replace('\n','')
        ori_hder = mdict[key]
        odict[ori_hder] = seq 
    return odict

def main():
    fa_dict =  parse(infile)

    if (mode == 'encode'):
        odict, map_lst = simplify(fa_dict, hder_format, value)   
        odict = formatter(odict,60)
        tofile(odict=odict, maplist=map_lst, 
                outfile=outfile, mapFile=mapFile, wmode = 'encode' )
    elif (mode == 'decode'):
        odict = decode(fa_dict, mapFile)
        odict = formatter(odict,60)         
        tofile(odict = odict, outfile = outfile, wmode = 'decode')

########################

if __name__ == '__main__':
    main()

