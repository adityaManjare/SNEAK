





class processedDocs:
    def __init__(self, url , title , body_text):
        self.url = url
        self.title = title
        # self.word_freq = word_freq
        self.body_text = body_text 




def extract_data(current_url , current_page):
    for tag in current_page.find_all(["script", "style"]):
        tag.decompose()
    current_title = current_page.title.string if current_page.title else ""
    body = current_page.body
    body_text = ""
    if body:
         body_text = body.get_text(separator = " " , strip = True)
    doc = processedDocs(current_url , current_title , body_text )
    return doc






