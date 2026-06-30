
import struct
from sneak.index_builder import Posting


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


def doc_freq(term , index):
    offset = index[term]
    with open("postings.bin", "rb") as postings:
        postings.seek(offset)
        df = struct.unpack("I",postings.read(4))[0]
    return df