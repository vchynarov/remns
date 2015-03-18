import pytest
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
@pytest.fixture
def session():
    TestSession = sessionmaker()
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine, checkfirst=True)
    TestSession.configure(bind=engine)
    return TestSession

# init testing services

class TestPostService(object):
    
    def get_post_service(self):
        print "CALLLLLEDDD!!"
        if '_postservice' in dir(self):
            print "returning old"
            return self._postservice
        else:
            print "returning new"
            self._postservice = PostService(session())
            return self._postservice


    # uses Global to test updates
    def test_create_basic_draft(self):
        post_service = self.get_post_service()
        test_post = {
            "title": "My first test post.",
            "content": "Here is some content",
            "mode": "draft"
        }
        item = post_service.create(test_post)
        retrieved = post_service.find(item)
        assert retrieved.title == "My first test post."
        assert "my-first-test-post" in retrieved.web_title
        assert retrieved.raw_content == test_post['content']
        assert retrieved.display_content == '<p>Here is some content</p>\n' 
        assert retrieved.id == item
        assert not retrieved.published

    # uses Global to test updates
    def test_create_basic_published(self):
        post_service = self.get_post_service()
        test_post = {
            "title": "My second test post.",
            "content": "Some more content",
            "mode": "published"
        }

        item = post_service.create(test_post)
        retrieved = post_service.find(item)
        assert retrieved.title == test_post['title']
        assert "my-second-test-post" in retrieved.web_title
        assert retrieved.raw_content == test_post['content']
        assert retrieved.display_content == '<p>Some more content</p>\n' 
        assert retrieved.id == item
        assert retrieved.published
    
    def test_update_basic_draft(self):
        pass
        

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
