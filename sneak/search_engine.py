
import json
from sneak.bool_search import bool_search
from sneak.phrase_search import phrase_search
from sneak.tfidf import rank_tfidf
from sneak.cache import LRUCache
from sneak.index_builder import tokenize
from sneak.autocomplete import autocomplete
from sqlalchemy.orm import Session
import Models
cache = LRUCache(1000)





BOOLEAN_OPERATORS = {"AND", "OR", "NOT"}


def is_boolean_query(query):
    return any(token.upper() in BOOLEAN_OPERATORS
               for token in query.split())


def is_phrase_query(query):
    return '"' in query



autocomp = autocomplete(4)

def search(query , db : Session):
    with open("index.json") as f:
        index = json.load(f)

    with open("metadata.json") as f:
        metadata = json.load(f)

    doc_lengths = {int(k): v["length"] for k, v in metadata.items()}
    page_ranks = {int(k) :v["pagerank"] for k , v in metadata.items()}

    max_pr = max(page_ranks.values())

    total_docs = len(doc_lengths)

    query = query.strip()
    # for autocomplete
    try:
        with open("query_history.json","r") as file:
            query_history = json.load(file)
    except:
        query_history = {}
    if query in query_history:
        query_history[query] += 1
    else:
        query_history[query] = 1
    with open("query_history.json","w") as file:
        json.dump(query_history,file)
    autocomp.insert(query,query_history)
    #

    cached = cache.get(query)
    
    if cached is not None:
        return cached
    
    alpha = 0.8 
    beta = 0.2

    if not query:
        return []

    if is_phrase_query(query):
        phrase = query.replace('"', '')
        docs = phrase_search(phrase, index)
        scores =  rank_tfidf(phrase , docs ,index ,doc_lengths , total_docs)
    
    elif is_boolean_query(query):
        docs = bool_search(query, index)
        query = (
        query.replace("AND", " ").replace("OR", " ").replace("NOT", " "))
        scores = rank_tfidf(query , docs , index , doc_lengths , total_docs)


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
    final_res = []
    for doc_id , score in results:
        doc = db.get(Models.webPage , doc_id)
        final_res.append({
            "document id " : doc_id,
            "title " : doc.title,
            "url " : doc.url,
            "score " : score,
            "body " : doc.body
        })
    return final_res
    

