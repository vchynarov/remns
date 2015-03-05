from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import markdown2

Base = declarative_base()

Post_Tags = Table('post_tags', Base.metadata,
     Column('id', Integer, primary_key = True),
     Column('post_id', Integer, ForeignKey('posts.id')),
     Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Post(Base):
    MAX_TOKENS = 6

    __tablename__ = 'posts'
    id = Column(Integer, primary_key = True)
    title = Column(String, unique=True, nullable=False)
    web_title = Column(String, unique=True, nullable=False)
    raw_content = Column(Text, nullable=False)
    display_content = Column(Text, nullable=False)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    published = Column(Boolean, nullable=False)
    tags = relationship('Tag', secondary=Post_Tags, backref='posts')

    def __init__(self, post_dict):
        # Need to do filtering.
        self.title = post_dict['title']
        self.raw_content = post_dict['content']
        modes = {'published': True, 'draft': False}
        self.published = modes[post_dict['mode']]
        self.display_content = self.get_rendered_content(self.raw_content)
        self.web_title = self.get_web_title(self.title)
        self.created = datetime.now()
        self.updated = datetime.now()

    def get_rendered_content(self, raw_content):
        return markdown2.markdown(raw_content, extras=["fenced-code-blocks"])

    def get_web_title(self, web_title):
        replacers = ["\"", "'", "\'", "?", ",", "#", "&", "!"]
        escaped = reduce(lambda rest, x: rest.replace(x, ""), replacers, web_title)
        # In case of double spaces.
        tokens = filter(lambda token: token, escaped.lower().split(" ")[:self.MAX_TOKENS])
        timestamp = datetime.now().strftime("%y-%m-%d-")
        return timestamp + "-".join(tokens)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key = True)
    name = Column(String, unique = True, nullable=False)

class ModelService(object):
    def __init__(self, model, session_maker):
        self.model = model
        self.session_maker = session_maker
        self._current_session = None

    def find(self, id):
        session = session_maker()
        return session.query(self.model).get(id)

    def update(self, id, *args):
        session = self.session_maker()

    def delete(self, id):
        session = self.session_maker()

    def _get_session(self):
        if not self._current_session:
            self._current_session = self.session_maker()
        return self._current_session

    def get_all(self):
        session = self._get_session()
        models = session.query(self.model).order_by('id DESC').all()
        return models
        

    def create(self, args_dict):
        session = self.session_maker()
        new_model = self.model(args_dict)
        session.add(new_model)
        session.commit()
        new_id = new_model.id # Cannot access after session closed.
        session.close()
        return new_id


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

