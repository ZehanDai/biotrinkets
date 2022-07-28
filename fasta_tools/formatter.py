#!/usr/bin/python3 

def formatter(indict, w):
    # w: width of fasta sequence
    odict = {}
    key_lst = list(indict.keys())
    for key in key_lst:
        seq = indict[key].replace('\n','')
        size = len(seq)
        nseq = []
        for sta_pos in range(1, size, w):
            sta_idx = sta_pos - 1
            end_idx = sta_idx + (w)
            end_pos = sta_pos + (w-1)
            if (end_idx + 1 > size ):
                end_idx = size - 1
                end_pos = size
            nseq.append( seq[sta_idx:end_idx].replace('\n','') )
        nseq = '\n'.join( nseq )
        odict[key] = nseq
    return odict
