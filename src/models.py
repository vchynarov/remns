from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Table, ForeignKey, Column, Integer, String, Time, Text, Boolean
from sqlalchemy.orm import relationship, backref
from datetime import time

Base = declarative_base()

Post_Tags = Table('post_tags', Base.metadata,
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
    tags = relationship('Tag', secondary=Post_Tags, backref='posts')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key = True)
    name = Column(String, unique = True, nullable=False)



class ModelService(object):
    def __init__(self, model, session_maker):
        self.model = model
        self.session_maker = session_maker

    def find(self, id):
        session = session_maker()
        session.query(model).find(id)

    def update(self, id, *args):
        session = session_maker()

    def delete(self, id):
        session = session_maker()

    def create(self, *args):
        session = session_maker()


class PostService(ModelService):
    def __init__(self, session_maker):
        super(PostService, self).__init__(Post, session_maker)

    def get_posts_by_date(self, year, month, day, *tags):
        pass

    def add_tags_to_post(self, id, tag_ids ):
        pass

    def remove_tags_from_post(self, id, tag_ids):
        pass
        
        
class TagService(ModelService):
    def __init__(self, session_maker):
        super(TagService, self).__init__(Tag, session_maker)

