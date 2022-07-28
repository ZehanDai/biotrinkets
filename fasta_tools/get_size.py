#!/usr/bin/python3

"""calculate size of fasta records"""

def get_size(indict):
    # takes fasta dict as input, returns a 3-column dataframe
    odict = {}
    odict['seqid'] = 'size'
    for hder,seq in indict.items():
        hder = hder.replace('\n','')
        seq = seq.replace('\n','')
        size = str(len(seq))
        odict[hder] = size
    return odict
