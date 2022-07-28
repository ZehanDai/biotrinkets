#!/usr/bin/python3

""" extract regions from long fasta sequences """

def corr_reg(line):
    ID,sta, end = line[0],int(line[1]),int(line[2])
    m = min(sta, end)
    M = max(sta, end)
    return [ID,m,M]

def subset(indict,id_reg_file):
    # id_reg_file: tsv with region for subsetting
    #     format: id\tsta\tend
    with open(id_reg_file,'r') as inf:
        id_reg_lst = inf.readlines()

    # check format
    top1 = id_reg_lst[0].split('\t')
    if len(top1) != 3:
        raise Exception('format error; expected format:\n  id\tsta\tend')
    id_reg_lst = [ line.replace('\n','') for line in id_reg_lst ]
    id_reg_lst = list(set(id_reg_lst))   # deduplicate regions
    id_reg_lst = [ line.split('\t') for line in id_reg_lst ]

    # correct the order of sta and end
    id_reg_lst = [ corr_reg(line) for line in id_reg_lst ]

    keys = list(indict.keys())
    odict = {}
    for line in id_reg_lst:
        ID,sta,end = line[0],line[1],line[2]
        
        # match ID in indict, extract and subset sequence
        hit_keys = [ k for k in keys if ID == k ]
        if len(hit_keys) != 1:
            raise Exception('len(hit_keys) != 1')
        key = hit_keys[0]
        
        # check if sta/end is out bound and correct
        seq = indict[key].replace('\n','')
        seq_size = len(seq)
        if sta <= 0:
            sta = 1
        if end > seq_size:
            end = seq_size
            
        subseq = seq[sta-1:end] # subset the sequence
        key = key +'_' + str(sta) + '-' + str(end)
        odict[key] = subseq
        
    return odict



