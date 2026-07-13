from fastapi import FastAPI, Depends
from Schemas import crawler_req
from sneak.handler import call_everything
from sneak.search_engine import search
from sqlalchemy.orm import  Session
from sneak.search_engine import cache , autocomp # literally imported a object
from sneak.handler import bk
import time
import Models
import database


app = FastAPI()


Models.Base.metadata.create_all(bind=database.engine)


@app.post('/dev/crawler')

def get_crawler(request : crawler_req , db : Session = Depends(database.get_db)):
    call_everything(request.url , request.depth , db)
    return ("Successful")


@app.get("/search")
def searchx(query: str , db : Session = Depends(database.get_db)):
    results = search(query , db)
    # return {
    #     "query": query,
    #     "results": [
    #         {"doc_id": doc_id, "score": score}
    #         for doc_id, score in results
    #     ]
    # }
    return results


@app.get("/cache/stats")
def cache_stats():
    return cache.stats()


@app.get("/autocomplete")
def func(query : str):
    return autocomp.search(query)

@app.get("/spellcorrect")
def func(query : str):
    return bk.search(query , 4)


@app.get("/benchmark")
def benchmark(query:str):

    start = time.perf_counter()
    search(query)
    first = time.perf_counter()-start

    start = time.perf_counter()
    search(query)
    second = time.perf_counter()-start

    return {
        "without_cache_ms": first*1000,
        "with_cache_ms": second*1000
    }


# seed_url = "https://books.toscrape.com/"
# depth = 1

