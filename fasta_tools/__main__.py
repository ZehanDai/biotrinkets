#!/usr/bin/python3

"""
Description: a collection of small utils for fasta file manipulation
Update: 2022-02-18
"""

import os
import sys
import getopt

from fasta_tools.get_size import * 
from fasta_tools.extract import *
from fasta_tools.subset import *
from fasta_tools.formatter import *
from fasta_tools.get_flank import *
from fasta_tools.splitN import *


def parse_params():
    opts,argv = getopt.getopt(sys.argv[1:],'-i:-o:-m:-l:-e:-M:-t:-f:-w:-n:-S:-h')
    mode_lst = ['get_size','extract','subset','get_flank',
            'sim_hder','encoder','formatter','splitSeq',
            'toRNA','reverse','rev_comp','splitN']
    infile,outfile,lst_id,tbl,e,mapfile,fsize,w,mode,num_cut,size_cut = '','','','', '','','','', '','',''

    for opt_n,opt_v in opts:
        if opt_n in ('-h'):
            print('Usage: python3 fasta_toolset.py [-m mode] [-i infile.fa] [-o outfile.fa] [other arguments...]')
            modes = ''.join([
                '\n  get_size: calculate the size, returns a list;\n',
                '    python3 -m fasta_tools -m get_size -i $infile -o $outfile\n',
                '  extract: extract fasta by ID;\n',
                '    python3 -m fasta_tools -m extract -i $infile -o $outfile -l seqid.lst\n',
                '  subset: extract smaller regions from fasta;\n',
                '    python3 -m fasta_tools -m subset -i $infile -o $outfile -t seq_reg.tsv\n',
                '  get_flank: like Subset, but gets the flanks ;\n',
                '    python3 -m fasta_tools -m get_flank -i $infile -o $outfile -t seq_reg.tsv -f 10\n',
                '  formatter: change the width of fasta;\n',
                '    python3 fasta_toolset -m formatter -i $infile -o $outfile -w 100\n',
                '  splitN: split sequence by Ns:\n',
                '    python3 -m fasta_tools -m splitN -i $infile -o $outfile -n 10 -S 100\n',
                ])
            print('modes',modes)
            exit()    
        elif opt_n == '-i':
            infile = opt_v
            #print('infile',infile)
        elif opt_n == '-o':
            outfile = opt_v
            #print('outfile',outfile)
        elif opt_n == '-l':
            lst_id = opt_v
            #print('id list',lst_id)
        elif opt_n == '-t':
            tbl = opt_v
            #print('region table for subseting',tbl)
        elif opt_n == '-e':
            e = opt_v # either True or False
            #print('exclude subset region',e)
        elif opt_n == '-M':
            mapfile = opt_v
            #print('id map file',mapfile)
        elif opt_n == '-f':
            fsize = opt_v
            #print('flank size',flank size)
        elif opt_n == '-w':
            w = int(opt_v)
            #print('seq width',w)
        elif opt_n == '-n':
            num_cut = int(opt_v)
            #print('minimum number of N/n to split',num_cut)
        elif opt_n == '-S':
            size_cut = int(opt_v)
            #print('minimum size of the seuqnece to keep',size_cut)
        elif opt_n == '-m':
            mode = opt_v
            #print('mode',mode)
    try:
        mode
    except :
        print('ERROR: must specify mode')
        print('Usage: python3 fasta_toolset.py [-m mode] [-i infile.fa] [-o outfile.fa] [other arguments...]')
        exit()

    if mode not in mode_lst:
        print(mode_lst)
        raise Exception('Mode given is not in predefined list')
    return infile,outfile,lst_id,tbl,e,mapfile,fsize,w,mode,num_cut,size_cut 

#####################################

def parse(fafile):
    """read fasta file, return a dictionary"""
    with open(fafile) as fa:
        fa = fa.read()
        fa_lst = fa.split('>')
        fa_lst = list(filter(None,fa_lst)) # 去掉开头的空字符串
        
        odict = {}
        for fa in fa_lst:
            hder = fa.split('\n')[0]
            seq = fa.replace(hder+'\n','')
            odict[hder] = seq
    return odict

      
def headd(idict,n=10):
    """print/extract the first n items of the dictionary, only for test stage"""
    odict = {}
    key_lst = list(idict.keys())[0:n]
    for key in key_lst:
        print(key)
        value = idict[key]
        print(value,'\n')
        odict[key] = value
    return odict


def tofile(odict,outfile,wmode):
    """wmode: writting mode, [ 'fasta','tsv', 'csv' ]"""
    print('writting output to file with specifi mode:',wmode)
    if wmode == 'fasta':
        olst = [ '>'+key+'\n'+val for key,val in odict.items() ]
    elif wmode == 'tsv':
        olst = [ key+'\t'+val for key,val in odict.items() ]
        
    with open(outfile,'w') as ouf:
        ouf.write( '\n'.join(olst))
    print('output written to file:',outfile)


######################################################### 

def main():
    
    infile,outfile,lst_id,tbl,e,mapfile,fsize,w,mode,num_cut,size_cut = parse_params() # initial params
    fa_dict =  parse(infile) # read file 
    
    if (mode == 'extract'):
        odict = extract(fa_dict,lst_id)
        tofile(odict,outfile,'fasta') 
    elif (mode == 'get_size'):
        odict = get_size(fa_dict)
        tofile(odict,outfile,'tsv')
    elif (mode == 'subset' ):
        odict = subset(fa_dict,tbl)
        tofile(odict,outfile,'fasta')
    elif (mode == 'formatter' ):
        odict = formatter(fa_dict,int(w))
        tofile(odict,outfile,'fasta')
    elif (mode == 'get_flank' ):
        odict = get_flank(fa_dict,tbl,int(fsize))
        tofile(odict,outfile,'fasta')
    elif (mode == 'splitN'):
        odict = splitN(fa_dict,num_cut = num_cut, size_cut = size_cut)
        tofile(odict,outfile,'fasta')

if __name__ == "__main__":
    main()

