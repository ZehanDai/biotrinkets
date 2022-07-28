#!/usr/bin/python3

import os 
from fasta_tools.subset import *

def get_flank(indict, id_reg_file, flank, exclude=False):
    # process the original region file first, then use "subset" to get fasta
    # Note: the param 'exclude' has not yet been finished yet
    with open(id_reg_file,'r') as inf:
        id_reg_lst = inf.readlines()
    id_reg_lst = [ line.split('\t') for line in id_reg_lst ]
    olst = []
    for line in id_reg_lst:
        ID,sta,end = line[0],int(line[1]),int(line[2])
        if (sta <= end):
            sta = sta - flank
            end = end + flank
        elif (end < sta):
            end = end - flank
            sta = sta + flank
        olst.append('\t'.join([ ID, str(sta), str(end) ]))
        
    with open('tmp_reg.tsv','w') as tbl:
        tbl.write('\n'.join(olst))

    odict = subset(indict,'tmp_reg.tsv')
    os.remove('tmp_reg.tsv')
    return odict



