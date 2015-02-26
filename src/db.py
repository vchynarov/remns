from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Post, Tag, Post_Tags, Base
import config

def get_session_maker():
    Session = sessionmaker()
    engine = create_engine(config.DB_CONN_STRING)
    Session.configure(bind=engine)
    return Session

if __name__ == "__main__":
    engine = create_engine(config.DB_CONN_STRING)
    Base.metadata.create_all(engine, checkfirst=True)
