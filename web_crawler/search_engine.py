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




def bool_and(a ,b ): # here i a and b are lists 
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




def bool_search(query:str):
    tokens = query.split()
    if not tokens:
        return []
    precedence = {
        "NOT" : 2,
        "AND" : 1,
        "OR" : 0
    }
    oprtr = []
    oprnd = []
    for token in tokens:
        if token in precedence :
            while oprtr and precedence[oprtr[-1]] >= precedence[token]:
                b = oprnd.pop()
                a = oprnd.pop() 
                op = oprtr.pop()
                if op == "AND":
                    c = bool_and(a,b)
                elif op == "OR":
                    c = bool_or(a,b)
                else:
                    c = bool_not(a,b)
                oprnd.append(c)
            oprtr.append(token)
        else:
            a = [x.doc_id for x in read_postings(token,index)]
            oprnd.append(a)
    while oprtr:
        b = oprnd.pop()
        a = oprnd.pop()
        op = oprtr.pop()
        if op == "AND":
            c = bool_and(a,b)
        elif op == "OR":
            c = bool_or(a,b)
        else:
            c = bool_not(a,b)
        oprnd.append(c)
    return oprnd.pop()



def merge_positions(pos1, pos2):
    i = j = 0
    matched = []

    while i < len(pos1) and j < len(pos2):

        if pos2[j] == pos1[i] + 1:
            matched.append(pos2[j])
            i += 1
            j += 1

        elif pos1[i] + 1 < pos2[j]:
            i += 1

        else:
            j += 1

    return matched


def phrase_search(query):
    words = query.split()
    if not words:
        return []

    postings = [read_postings(word, index) for word in words]

    #yup similar to how we do list initialization 
    current = {
        p.doc_id: p.positions
        for p in postings[0]
    }

    for k in range(1, len(words)):
        nxt = {
            p.doc_id: p.positions
            for p in postings[k]
        }
        new_current = {}
        for doc in current:

            if doc not in nxt:
                continue
            matched = merge_positions(current[doc], nxt[doc])
            if matched:
                new_current[doc] = matched

        current = new_current
        if not current:
            return []

    return list(current.keys())




    # if len(tokens) == 1:
    #     docs = [x.doc_id for x in read_postings(query,index)]
    # else:



    #     a = [x.doc_id for x in read_postings(tokens[0],index)]
    #     b = [x.doc_id for x in read_postings(tokens[2],index)]
    #     if tokens[1] == "AND":
    #         docs = bool_and(a,b)
    #     elif tokens[1] == "OR":
    #         docs = bool_or(a,b)
    #     else:
    #         docs = bool_not(a,b)
    # return docs







# print(search("dream NOT butthol OR hello AND boy OR girl NOT hello"))
# print(search("dream NOT butthol OR hello AND boy OR girl"))
# print(search("dream NOT butthol OR hello AND boy"))
# print(search("dream NOT butthol OR hello"))
# print(search("dream NOT butthol "))
# print(search("dream "))
# print(search("boy"))
# print(search("girl"))
# print(search("boy AND girl NOT dream"))
print(phrase_search("love you"))