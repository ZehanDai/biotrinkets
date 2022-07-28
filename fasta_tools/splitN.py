#!/usr/bin/python3 
"""split fasta by N """


def get_substr_idx(string, substr):
    idx = 0
    pos = []
    
    while True:
        idx = string.find(substr, idx)
        if (idx == -1):
            return pos # idx will be -1 only after the last hits, thus finalize pos
        pos.append(idx)
        idx += len(substr)
    

def cac_region(pos, threshold, Filter=True):
    slst = [] # store temperary variables 
    olst = [] # store output results
    len_pos = len(pos)
    last_pos_idx = len_pos - 1
    for idx in pos:
        if pos.index(idx) == 0:
            slst.append(idx)
        elif pos.index(idx) >= 1:
            old_idx = slst[len(slst)-1]
            if (old_idx == (idx - 1)):
                slst.append(idx)
            elif (old_idx != (idx-1)):
                olst.append(slst)
                slst = []
                slst.append(idx)
            if pos.index(idx) == last_pos_idx:
                olst.append(slst)

    olst2 = []
    for reg in olst:
        sta = reg[0]
        end = reg[len(reg)-1]
        
        if (end - sta >= threshold) and (Filter == True) :
            olst2.append([sta,end])
        if Filter == False:
            olst2.append([sta,end])
    return olst2

def create_comple_lst(string, regions):
    # create complementary regions for given regions
    #   implementation:
    #       given a seuqence, sort regions, add 0 and the end of the full sequence size, a form a list (the total number must be even)
    #   create regions pair by pair
    sta0 = 0
    end0 = len(string)
    olst = []
    for reg in regions:
        slst = list( range(reg[0], reg[1]+1 ))
        olst = olst + slst
    olst2 = [ i for i in list(range(sta0,end0)) if i not in olst ]
    olst2 = cac_region(olst2,threshold=5, Filter=False) # 这里不是过滤特定长度的Ns
    return olst2


def ext_substr_lst(string, idx_lst):
    # accept a seq
    olst = []
    for reg in idx_lst:
        sta = reg[0]
        try:
            end = reg[1]+1
            substr = string[sta:end]
        except :
            substr = string[sta]
        olst.append(substr)
    return olst


def splitN(indict,num_cut=5,size_cut=200):
    # num_cut: minimum total N threshold to split
    # size_cut: minimum size of sequence to keep after split
    odict = {}
    key_lst = list(indict.keys())
    for key in key_lst:
        seq = indict[key].replace('\n','')
        
        pos1 = get_substr_idx(seq,'N')
        pos2 = get_substr_idx(seq,'n')
        pos = pos1 + pos2
        
        regions = cac_region(pos,5)
        regions = create_comple_lst(seq, regions)
        
        olst = ext_substr_lst(seq,regions)
        
        hder_idx = 0
        for subset in olst:
            if len(subset) >= size_cut:
                hder_idx += 1
                nkey = key + '_splitN' + str(hder_idx)
                odict[nkey] = subset 
    return odict
