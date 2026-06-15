import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import json


# print("Script is starting...")
internal_links = set()
external_links = set()
seed_url = "https://books.toscrape.com/"
depth = 1



class Document:
    def __init__(self , url , title , body, page_num):
        self.url = url
        self.title = title
        self.body = body
        self.page_num = page_num 
    


def get_links(current_url , current_page):
    urls = set()
    current_domain = urlparse(current_url).netloc # will get the domain name from this
    for anchor_tag in current_page.find_all("a"): # all the anchor tags
        href = anchor_tag.attrs.get("href")
        if(href != "" and href != None):
            orginal_link = urljoin(current_url , href)
            orginal_link_parsed = urlparse(orginal_link)
            clean_link = orginal_link_parsed.scheme
            clean_link += "://"
            clean_link += orginal_link_parsed.netloc
            clean_link += orginal_link_parsed.path
            clean_link_parsed = urlparse(clean_link)
            is_valid = bool(clean_link_parsed.scheme) and bool(clean_link_parsed.netloc)
            if(is_valid) :
                if current_domain not in clean_link :
                    print(f"external link {clean_link}")
                    external_links.add(clean_link)
                if current_domain in clean_link :
                    print(f"internal link {clean_link}")
                    internal_links.add(clean_link)
                urls.add(clean_link)
    return urls

def extract_data(current_url , current_page, page_num):
    for tag in current_page.find_all(["script", "style"]):
        tag.decompose()
    current_title = current_page.title.string if current_page.title else ""
    body = current_page.body
    body_text = ""
    if body:
         body_text = body.get_text(separator = " " , strip = True)
    doc = Document(current_url , current_title , body_text , page_num)
    return doc


def spider(seed_url , depth):
    queue = []
    docs = []
    page_num = 0
    queue.append(seed_url)
    for i in range(depth):
            for _ in range(len(queue)): # level order traversal
                current_url = queue.pop(0)
                page_num += 1
                current_page =  BeautifulSoup(requests.get(current_url).content , "lxml") 
                urls = get_links(current_url, current_page)
                doc = extract_data(current_url,current_page,page_num)
                print(f"page num {page_num}")
                docs.append(doc)
                for url in urls:
                    queue.append(url)
    for doc in docs:
        print(f"title {doc.title}")


spider(seed_url,2)



# ParseResult(
#     scheme='https',
#     netloc='example.com',
#     path='/about',
#     params='',
#     query='',
#     fragment=''
# )