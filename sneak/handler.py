from sqlalchemy.orm import Session
from sneak.spider import spider
from sneak.index_builder import buildIndex , store_in_disk
from sneak.pageranker import rankPages
from sneak.BK_tree import BKTree
import json



bk = BKTree()
def call_everything(url , depth , db:Session):
    spider(url , depth , db)
    print("crawled \n")
    yeah_ignr_it = buildIndex(db)
    store_in_disk(yeah_ignr_it)
    print("stored in disks \n")
    serializable = {
        term: [post.to_dict() for post in postings]
        for term, postings in yeah_ignr_it.items()
    }
    with open("test.json","w") as file:
        json.dump(serializable,file,indent=4 )

    # json_size = os.path.getsize("test.json")
    # bin_size = os.path.getsize("postings.bin")
    # print(f"JSON Size   : {json_size / (1024 * 1024):.2f} MB")
    # print(f"Binary Size : {bin_size / (1024 * 1024):.2f} MB")
    print("test.json \n")
    rankPages()
    print("pages ranked \n")
    
    with open("index.json") as f:
        index = json.load(f)
    for value , _ in index.items():
        bk.insert(value)
    print(" bk tree made \n")

