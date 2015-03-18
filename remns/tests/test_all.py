import os
import sys
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from datetime import datetime

# Set up path to import remns things.
sys.path.append(os.path.realpath('./remns'))

# import models
from models import PostService, TagService, Post_Tags, Base


# Set up database
TestSession = sessionmaker()
engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine, checkfirst=True)
TestSession.configure(bind=engine)

# init testing services
post_service = PostService(TestSession)
tag_service = TagService(TestSession)

class TestPostService(object):
    def test_create_basic_draft(self):
        test_post = {
            "title": "My first test post.",
            "content": "Here is some content",
            "mode": "draft"
        }
        post_service.create(test_post)

        retrieved = post_service.find(TEST_ID)
        assert retrieved.title == "My first test post."
        assert "my-first-test-post" in retrieved.web_title
        assert retrieved.raw_content == test_post['content']
        assert retrieved.display_content == '<p>Here is some content</p>\n' 
        assert retrieved.id == 1
        assert not retrieved.published

    def test_create_basic_published(self):
        pass
    
    def test_update(self):
        assert False
        

# class TestTagService(object):
#     def test_create_tag(self):
#         assert False
#
#     def test_rename_tag(self):
#         assert False
#
#     def test_delete_tag(self):
#         assert False
#
# class TestAdminController(object):
#     def test_authentication(self):
#         assert False
#
