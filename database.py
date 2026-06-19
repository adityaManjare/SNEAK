from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



sqlalchemy_database_url = "sqlite:///./app.db"


engine = create_engine(sqlalchemy_database_url, connect_args={'check_same_thread': False}) # an engine is the the main interface of the database im # sqlalchemy, it is used to connect to the database and execute queries
# the connect_args={'check_same_thread': False} is used to allow multiple threads to access the database at the same time, which is necessary for FastAPI to work properly with SQLite.
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#This creates a session factory that will generate database sessions.bind=engine: Sessions created by this factory will use the specified engine
Base = declarative_base()


# is pure get db ka yahi kaam tha bas ki yeh ek session banake use db ko pakda de ya inject karde
def get_db():
    db = session_local() # here db is a session object that is used to interact with the database

    try:
        yield db #Yields the session: yield db provides the session to whoever calls this function

    finally:
        db.close()



# session is a connection to the database, it is used to execute queries and transactions
# session_local is a session factory that will generate database sessions
# engine is the main interface of the database in SQLAlchemy, it is used to connect to the database and execute queries (and as such hame sessions iss engine database ke liye chahiye we bind the session to engine)
# Base is the declarative base class that is used to define the database models
# It provides a way to define the database schema using Python classes and SQLAlchemy's ORM capabilities.

