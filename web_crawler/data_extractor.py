import re
from nltk.stem import PorterStemmer



helping_words = {
    "a", "an", "the", "is", "are", "was", "were",
    "of", "to", "in", "on", "at", "for", "by",
    "and", "or", "but", "if", "then", "this", "that"
}




class processedDocs:
    def __init__(self, url , title , word_freq , body_text):
        self.url = url
        self.title = title
        self.word_freq = word_freq
        self.body_text = body_text 




def extract_data(current_url , current_page):
    for tag in current_page.find_all(["script", "style"]):
        tag.decompose()
    current_title = current_page.title.string if current_page.title else ""
    body = current_page.body
    body_text = ""
    if body:
         body_text = body.get_text(separator = " " , strip = True)
    doc = processedDocs(current_url , current_title , calc_wordFreq(body_text) , body_text )
    return doc




def calc_wordFreq(body_text):
    word_arr = re.findall(r"\b[a-zA-Z]+\b", body_text)
    stemmer = PorterStemmer()
    word_freq = {}
    for word in word_arr:
        word = word.lower()
        word = stemmer.stem(word)
        if word not in helping_words:
            if word not in word_freq:
                word_freq[word] = 0
            word_freq[word] += 1
    return word_freq

