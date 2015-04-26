from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import markdown2

Base = declarative_base()

Post_Tags = Table('post_tags', Base.metadata,
     Column('id', Integer, primary_key=True),
     Column('post_id', Integer, ForeignKey('posts.id')),
     Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Post(Base):
    MAX_TOKENS = 6

    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    web_title = Column(String, unique=True, nullable=False)
    raw_content = Column(Text, nullable=False)
    display_content = Column(Text, nullable=False)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    published = Column(Boolean, nullable=False)
    tags = relationship('Tag', secondary=Post_Tags, backref='posts')
    ViewModes = {'published': True, 'draft': False}

    def __init__(self, post_dict):
        self._write(post_dict)
        self.created = datetime.now()
        self.web_title = self.get_web_title(self.title)

    def get_rendered_content(self, raw_content):
        return markdown2.markdown(raw_content, extras=["fenced-code-blocks"])

    def get_web_title(self, web_title):
        replacers = ["\"", "'", "\'", "?", ",", "#", "&", "!"]
        escaped = reduce(lambda rest, x: rest.replace(x, ""), replacers, web_title)
        # In case of double spaces.
        tokens = filter(lambda token: token, escaped.lower().split(" ")[:self.MAX_TOKENS])
        timestamp = datetime.now().strftime("%y-%m-%d-")
        return timestamp + "-".join(tokens)

    def _write(self, input_dict):
        self.title = input_dict['title']
        self.raw_content = input_dict['content']
        self.display_content = self.get_rendered_content(self.raw_content)
        self.published = self.ViewModes[input_dict['mode']]
        self.updated = datetime.now()

    def update(self, put_dict):
        self._write(put_dict)

    def api_representation(self):
        pass

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)

    def __init__(self, post_dict):
        self._write(post_dict)
        self.created = datetime.now()

    def update(self, put_dict):
        self._write(put_dict)

    def _write(self, input_dict):
        self.name = input_dict["name"]
        self.updated = datetime.now()

    def api_representation(self):
        return {
                "id": self.id,
                "name": self.name
        }
        
class ModelService(object):
    def __init__(self, model, session_maker):
        self.model = model
        self.session_maker = session_maker
        self._current_session = None

    def find(self, id):
        # need to add connection pool kind of thing.
        session = self._get_session()
        return session.query(self.model).get(id)

    def update(self, id, args_dict):
        session = self._get_session()
        existing_model = self.find(id)
        existing_model.update(args_dict)
        session.add(existing_model)
        session.commit()

    def _get_session(self):
        pool = None
        if not self._current_session:
            self._current_session = self.session_maker()

        return self._current_session

    def delete(self, id):
        session = self._get_session()
        session.delete(self.find(id))
        session.commit()

    def get_all(self):
        session = self._get_session()
        models = session.query(self.model).order_by('id DESC').all()
        return models
        
    def create(self, args_dict):
        session = self._get_session()
        new_model = self.model(args_dict)
        session.add(new_model)
        session.commit()
        new_id = new_model.id # Cannot access after session closed.
        return new_id

    def find_multiple(self, args_dict):
        session = self._get_session()
        models = session.query(self.model).filter(self.model.in_(ids))
        return models


class TaggingService(ModelService):
    def __init__(self, session_maker):
        super(TaggingService, self).__init__(None, session_maker)

    def set_tags(self, post_id, tag_ids):
        session = self._get_session()
        insert_values = [{"post_id": int(post_id), "tag_id": int(tag_id)} for tag_id in tag_ids]
        # More performant and way simpler to just wrap a delete all and create all in a transaction.
        try:
            delete_operation = Post_Tags.delete().where(Post_Tags.c.post_id == post_id)
            insert_operation = Post_Tags.insert().values(insert_values)
            session.execute(delete_operation)
            session.execute(insert_operation)
            session.commit()
        except:
            session.rollback()
            raise

class PostService(ModelService):
    def __init__(self, session_maker):
        super(PostService, self).__init__(Post, session_maker)

    def get_posts_by_date(self, year, month=None, day=None, *tags):
        pass

    def get_post_tags(self, post_id):
        session = self._get_session()
        post = session.query(Post).get(post_id)
        return post.tags

        
class TagService(ModelService):
    def __init__(self, session_maker):
        super(TagService, self).__init__(Tag, session_maker)

    def initialize_tags(self, submitted_tags):
        """
            Returns an array of integers of newly created tags!
        """
        new_tags = filter(lambda tag: tag["status"] == "created", submitted_tags)
        existing_ids = [int(tag["value"]) for tag in  filter(lambda tag: tag["status"] == "existing", submitted_tags)]
        new_ids = [self.create({"name": new_tag["value"]}) for new_tag in new_tags]
        return new_ids + existing_ids
