#!/usr/bin/python3

def match_lst(qlst,slst):
    # compare qlst and slst, get items from slst matching qlst
    olst = []
    for q in qlst:
        hit = [ s for s in slst if s == q ] # absolute match
        if len(hit) == 1:
            olst.append(hit[0])
        else:
            hits = [ s for s in slst if q in s ] # substring match
            if len(hits) > 1:
                raise Exception('more than 1 hit found')
            elif len(hits) == 0:
                raise Exception('no hits found')
    return olst

def extract(indict,id_lst_file):
    # extract by id
    with open(id_lst_file,'r') as l:
        id_lst = l.readlines()
        id_lst = [ i.replace('\n','') for i in id_lst]
        
        keys = list(indict.keys())
        id_lst2 = match_lst(id_lst, keys)
        
        odict={}
        total = len(id_lst2)
        i = 0
        for ID in id_lst2:
            i = i + 1
            #print(str(i)+'/'+str(total))
            value = indict[ID].replace('\n','')
            odict[ID] = value
    return odict
