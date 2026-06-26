import struct
from web_crawler.index_builder import Posting
import json

with open("index.json") as f:
    index = json.load(f)


def read_postings(term : str , index ):
    if term not in index:
        return []
    offset = index[term]
    docs = []
    with open("postings.bin","rb") as postings:
        postings.seek(offset)
        doc_freq = struct.unpack("I",postings.read(4))[0]
        for _ in range(doc_freq):
            doc_id = struct.unpack("I",postings.read(4))[0]
            term_freq = struct.unpack("I",postings.read(4))[0]
            positions = []
            for _ in range(term_freq):
                positions.append(struct.unpack("I",postings.read(4))[0])
            docs.append(Posting(doc_id , positions , term_freq))
    return docs




def bool_and(a ,b ): # here i a and b are listsb
    ans = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            ans.append(a[i])
            i += 1 
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return ans

def bool_or(a,b):
    ans = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            ans.append(a[i])
            i += 1 
            j += 1
        elif a[i] < b[j]:
            ans.append(a[i])
            i += 1
        else:
            ans.append(b[j])
            j += 1
    while i < len(a) :
        ans.append(a[i])
        i += 1
    while j < len(b) :
        ans.append(b[j])
        j += 1
    return ans


def bool_not(a , b):
    ans = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1 
            j += 1
        elif a[i] < b[j]:
            ans.append(a[i])
            i += 1
        else:
            j += 1
    while i < len(a) :
        ans.append(a[i])
        i += 1
    return ans




def search(query:str):
    tokens = query.split()
    if not tokens:
        return []
    docs = []
    if len(tokens) == 1:
        docs = [x.doc_id for x in read_postings(query,index)]
    else:
        a = [x.doc_id for x in read_postings(tokens[0],index)]
        b = [x.doc_id for x in read_postings(tokens[2],index)]
        if tokens[1] == "AND":
            docs = bool_and(a,b)
        elif tokens[1] == "OR":
            docs = bool_or(a,b)
        else:
            docs = bool_not(a,b)
    return docs

query = "dress" 
print(search(query))