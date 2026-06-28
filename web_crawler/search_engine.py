
import json
from web_crawler.bool_search import bool_search
from web_crawler.phrase_search import phrase_search
from web_crawler.ranking import tf_idf




with open("index.json") as f:
    index = json.load(f)


with open("doc_lenghts.json") as f:
    doc_lengths = json.load(f)

doc_lengths = {int(k): v for k, v in doc_lengths.items()}

total_docs = len(doc_lengths)


   




BOOLEAN_OPERATORS = {"AND", "OR", "NOT"}


def is_boolean_query(query):
    return any(token.upper() in BOOLEAN_OPERATORS
               for token in query.split())


def is_phrase_query(query):
    return '"' in query


def search(query):
    query = query.strip()

    if not query:
        return []


    if is_boolean_query(query):
        print("boolean search \n")
        return bool_search(query, index)

    if is_phrase_query(query):
        print("phrase search \n")
        phrase = query.replace('"', '')
        return phrase_search(phrase, index)
    

    return tf_idf(query, index, doc_lengths, total_docs)


print(search("hello world"))
print(search('"love you"'))
print(search("hello OR world"))


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