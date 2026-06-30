from urllib.parse import urljoin
from urllib.parse import urlparse



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
                if current_domain in clean_link :
                    urls.add(clean_link)
    return urls




# ParseResult(
#     scheme='https',
#     netloc='example.com',
#     path='/about',
#     params='',
#     query='',
#     fragment=''
# )