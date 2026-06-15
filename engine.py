import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse



# print("Script is starting...")
internal_links = set()
external_links = set()
seed_url = "https://books.toscrape.com/"
depth = 1


def get_links(seed_url):
    urls = set()
    current_domain = urlparse(seed_url).netloc # will get the domain name from this
    current_page = BeautifulSoup(requests.get(seed_url).content , "lxml") # content and lxml 
    for anchor_tag in current_page.find_all("a"): # all the anchor tags
        href = anchor_tag.attrs.get("href")
        if(href != "" and href != None):
            orginal_link = urljoin(seed_url , href)
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


def spider(seed_url , depth):
    queue = []
    queue.append(seed_url)
    for i in range(depth):
            print(f"depth { depth }")
            for _ in range(len(queue)): # level order traversal
                urls = get_links(queue.pop(0))
                for url in urls:
                    queue.append(url)

spider(seed_url,2)

# ParseResult(
#     scheme='https',
#     netloc='example.com',
#     path='/about',
#     params='',
#     query='',
#     fragment=''
# )