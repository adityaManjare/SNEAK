import math
from collections import defaultdict
from sneak.index_builder import tokenize
from sneak.postings_reader import read_postings
from sneak.postings_reader import doc_freq




def rank_tfidf(query, candidate_docs , index , doc_lengths , total_docs):
    if candidate_docs is not None:
        candidate_docs = set(candidate_docs)
    terms = set(tokenize(query))
    scores = defaultdict(float)
    for term in terms:
        if term in index:
            df = doc_freq(term,index)
            idf = math.log((total_docs + 1) / (df + 1)) + 1
            postings = read_postings(term,index)
            for posting in postings:
                if candidate_docs is not None and posting.doc_id not in candidate_docs:
                    continue
                # print("Posting doc_id: ", posting.doc_id)
                # print("doc_lengths: ", doc_lengths)
                tf = posting.term_freq / doc_lengths[posting.doc_id]
                scores[posting.doc_id] += tf * idf
    return scores

# print(tf_idf("hello my"))




