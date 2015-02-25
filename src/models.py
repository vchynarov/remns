from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Table, ForeignKey, Column, Integer, String, Time, Text, Boolean
from sqlalchemy.orm import sessionmaker, relationship, backref
from datetime import time

Session = sessionmaker()
Base = declarative_base()
engine = create_engine()
Session.configure(bind=engine)

post_tags = Table('post_tags', Base.metadata,
     Column('id', Integer, primary_key = True),
     Column('post_id', Integer, ForeignKey('posts.id')),
     Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key = True)
    title = Column(String, unique=True, nullable=False)
    web_title = Column(String, unique=True, nullable=False)
    content = Column(Text, nullable=False)
    created = Column(Time, nullable=False)
    updated = Column(Time, nullable=False)
    published = Column(Boolean, nullable=False)
    tags = relationship('Tag', secondary=post_tags, backref='posts')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key = True)
    name = Column(String, unique = True, nullable=False)

Base.metadata.create_all(engine, checkfirst=True)


# stuff
if __name__ == '__main__':
    session = Session()
    general_tag = Tag(name='general')
    music_tag = Tag(name='music')
    first_post = Post(title='first post', web_title='yoo', content = 'fasdflkdasjflkdjasf', created=time(), updated = time())
    session.add(general_tag)
    session.add(music_tag)
    session.add(first_post)

    session.commit()
