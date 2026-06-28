import math
from collections import defaultdict
from web_crawler.index_builder import tokenize
from web_crawler.postings_reader import read_postings
from web_crawler.postings_reader import doc_freq




def tf_idf(query, index , doc_lengths , total_docs):
    terms = set(tokenize(query))
    scores = defaultdict(float)
    for term in terms:
        if term in index:
            df = doc_freq(term,index)
            idf = math.log((total_docs + 1) / (df + 1)) + 1
            postings = read_postings(term,index)
            for posting in postings:
                tf = posting.term_freq / doc_lengths[posting.doc_id]
                scores[posting.doc_id] += tf * idf
    results = sorted( scores.items(), key=lambda x: x[1], reverse=True ) # scores.items() returns (doc_id, score) tuples 
    return results

# print(tf_idf("hello my"))




