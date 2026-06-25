from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String , DateTime
from sqlalchemy.sql import func


Base = declarative_base()



class webPage(Base):
    __tablename__ = "WebPages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String,index=True ,nullable=False) # as of now if you have same url it will throw error
    title = Column(String, index=True, nullable=False)
    body = Column(String, nullable=False)
    crawled_at = Column(DateTime(timezone=True), server_default=func.now())