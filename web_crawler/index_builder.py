import re
from nltk.stem import PorterStemmer

from database import session_local
from sqlalchemy.orm import Session
import Models
import struct
import json


helping_words = {
    "a", "an", "the", "is", "are", "was", "were",
    "of", "to", "in", "on", "at", "for", "by",
    "and", "or", "but", "if", "then", "this", "that"
}


class Posting:
    def __init__(self , doc_id  ,positions = None , term_freq = 0 ):
        self.doc_id = doc_id
        self.term_freq = term_freq
        if(positions is None):
            self.positions = []
        else:
            self.positions = positions
    def __repr__(self):
        return(
            f"Posting( doc_id = {self}, "
            f"term_freq = {self.term_freq} "
            f"positions = {self.positions} )"
        )

def tokenize(text : str):
    tokens = []
    word_arr = re.findall(r"\b[a-zA-Z]+\b", text)
    stemmer = PorterStemmer()
    for word in word_arr:
        word = word.lower()
        if word not in helping_words:
            word = stemmer.stem(word)
            tokens.append(word)
    return tokens
        

def buildIndex(db : Session):
    dictionary = {}
    doc_lengths = {}
    docs = db.query(Models.webPage).all()
    for doc in docs:
        text = doc.title + " " + doc.body
        tokens = tokenize(text)
        doc_lengths[doc.id] = len(tokens)
        for pos , term in enumerate(tokens):
            if term not in dictionary:
                dictionary[term] = []
            postings = dictionary[term]
            if len(postings) == 0 or postings[-1] != doc.id: # you have to create a new post
                new_post = Posting(doc.id )
                postings.append(new_post)
            post = postings[-1]
            post.term_freq += 1
            post.positions.append(pos)

    with open("doc_lenghts.json" , "w") as file:
        json.dump(doc_lengths,file)
    return dictionary





# db = session_local()
# try:
#     dictionary = buildIndex(db)
# finally:
#     db.close()





def store_in_disk(dictionary):
    with open("postings.bin", "wb") as post_file:
        index = {}
        for term in sorted(dictionary.keys()):
            offset = post_file.tell()
            index[term] = offset
            postings = dictionary[term]
            post_file.write(struct.pack("I",len(postings)))
            for post in postings:
                post_file.write(struct.pack("I",post.doc_id))
                post_file.write(struct.pack("I",post.term_freq))
                for pos in post.positions:
                    post_file.write(struct.pack("I",pos))

    with open("index.json","w") as file:
        json.dump(index,file)


# store_in_disk(dictionary)






# def calc_wordFreq(body_text):
#     word_arr = re.findall(r"\b[a-zA-Z]+\b", body_text)
#     stemmer = PorterStemmer()
#     word_freq = {}
#     for word in word_arr:
#         word = word.lower()
#         word = stemmer.stem(word)
#         if word not in helping_words:
#             if word not in word_freq:
#                 word_freq[word] = 0
#             word_freq[word] += 1
#     return word_freq



# crawler -> sql lite -> indexing 
                        # dictionary -> term - offset "location -> as json file "
                        # posting -> binary file which will have our all the postings which we can fecth using offset
                    