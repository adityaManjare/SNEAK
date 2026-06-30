from fastapi import FastAPI, Depends
from Schemas import crawler_req
from sneak.spider import spider
from sneak.search_engine import search
from sqlalchemy.orm import  Session
from sneak.search_engine import cache
import time
import Models
import database



app = FastAPI()




Models.Base.metadata.create_all(bind=database.engine)

from sqlalchemy import inspect

Models.Base.metadata.create_all(bind=database.engine)

inspector = inspect(database.engine)
print("Tables:", inspector.get_table_names())


@app.post('/dev/crawler')

def get_crawler(request : crawler_req , db : Session = Depends(database.get_db)):
    spider(request.url , request.depth , db)
    return ("hogya print")


@app.get("/search")
def searchx(query: str):
    results = search(query)

    return {
        "query": query,
        "results": [
            {"doc_id": doc_id, "score": score}
            for doc_id, score in results
        ]
    }


@app.get("/cache/stats")
def cache_stats():
    return cache.stats()


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

