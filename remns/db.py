from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Post, Tag, Post_Tags, Base
import config

def get_session_maker():
    Session = sessionmaker()
    engine = create_engine(config.DB_CONN_STRING)
    Session.configure(bind=engine)
    return Session

def reset():
    engine = create_engine(config.DB_CONN_STRING)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine, checkfirst=True)

if __name__ == "__main__":
    reset()
