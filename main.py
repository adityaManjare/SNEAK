from fastapi import FastAPI, Depends
from Schemas import crawler_req
from web_crawler.spider import spider
from sqlalchemy.orm import  Session
import Models
import database



app = FastAPI()


Models.Base.metadata.create_all(bind=database.engine)


@app.post('/dev/crawler')

def get_crawler(request : crawler_req , db : Session = Depends(database.get_db)):
    spider(request.url , request.depth , db)
    return ("hogya print")



# seed_url = "https://books.toscrape.com/"
# depth = 1

