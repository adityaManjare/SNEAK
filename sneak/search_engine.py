
import json
from sneak.bool_search import bool_search
from sneak.phrase_search import phrase_search
from sneak.tfidf import rank_tfidf
from sneak.cache import LRUCache

cache = LRUCache(1000)

with open("index.json") as f:
    index = json.load(f)


with open("metadata.json") as f:
    metadata = json.load(f)

doc_lengths = {int(k): v["length"] for k, v in metadata.items()}
page_ranks = {int(k) :v["pagerank"] for k , v in metadata.items()}


max_pr = max(page_ranks.values())


total_docs = len(doc_lengths)




BOOLEAN_OPERATORS = {"AND", "OR", "NOT"}


def is_boolean_query(query):
    return any(token.upper() in BOOLEAN_OPERATORS
               for token in query.split())


def is_phrase_query(query):
    return '"' in query


def search(query):
    query = query.strip()

    cached = cache.get(query)
    
    if cached is not None:
        return cached
    
    alpha = 0.8 
    beta = 0.2

    if not query:
        return []


    if is_boolean_query(query):
        # print("boolean search \n")
        docs = bool_search(query, index)
        query = (
        query.replace("AND", " ").replace("OR", " ").replace("NOT", " "))
        scores = rank_tfidf(query , docs , index , doc_lengths , total_docs)

    elif is_phrase_query(query):
        # print("phrase search \n")
        phrase = query.replace('"', '')
        docs = phrase_search(phrase, index)
        scores =  rank_tfidf(phrase , docs ,index ,doc_lengths , total_docs)
    
    else :
        scores = rank_tfidf(query, None ,index, doc_lengths, total_docs)
    
    if not scores:
        return []
    
    max_score = max(scores.values())

    if max_score == 0:
        max_score = 1

    for doc_id in scores:
        scores[doc_id] = (alpha * (scores[doc_id]/max_score) + beta * (page_ranks[doc_id]/max_pr) )


    results = sorted( scores.items(), key=lambda x: x[1], reverse=True ) # scores.items() returns (doc_id, score) tuples 
    cache.put(query, results)
    return results
    

# print(len(index))

# print(search("love you"))
# print(search("love OR you"))


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
# print(phrase_search("love you"))