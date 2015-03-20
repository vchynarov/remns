import pytest
import time # sleep for approx timestamp comparison
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

def approx_same(time1, time2):
    return abs((time2-time1).total_seconds()) < 0.01

# init testing services

class TestPostServiceWrites(object):
    
    def get_post_service(self):
        if '_postservice' in dir(self):
            return self._postservice
        else:
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
        self.created_draft_id = item

        assert retrieved.title == "My first test post."
        assert approx_same(retrieved.created, retrieved.updated) 
        assert "my-first-test-post" in retrieved.web_title
        assert retrieved.raw_content == test_post['content']
        assert retrieved.display_content == '<p>Here is some content</p>\n' 
        assert retrieved.id == item
        assert not retrieved.published

        self.t_update_basic_draft()

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
        assert approx_same(retrieved.created, retrieved.updated)
        assert retrieved.title == test_post['title']
        assert "my-second-test-post" in retrieved.web_title
        assert retrieved.raw_content == test_post['content']
        assert retrieved.display_content == '<p>Some more content</p>\n' 
        assert retrieved.id == item
        assert retrieved.published
    
    # secondary test
    def t_update_basic_draft(self):
        post_service = self.get_post_service()
        test_post = {
            "title": "updated first post",
            "content": "updated first content",
            "mode": "published"
        }

        time.sleep(0.05) # give some time for updates
        post_service.update(self.created_draft_id, test_post)
        retrieved = post_service.find(self.created_draft_id)
        assert retrieved.title == test_post['title']
        # we title should not change!
        assert "my-first-test-post" in retrieved.web_title
        assert not approx_same(retrieved.created, retrieved.updated)
        assert retrieved.raw_content == test_post['content']
        assert retrieved.display_content == '<p>updated first content</p>\n' 
        assert retrieved.id == self.created_draft_id
        assert retrieved.published

    def test_delete_post(self):
        post_service = self.get_post_service()
        test_post = {
            "title": "Post to be deleted",
            "content": "Some more content",
            "mode": "published"
        }
        item = post_service.create(test_post)
        post_service.delete(item)
        deleted_post = post_service.find(item)
        assert deleted_post is None
        pass

class TestTagService(object):

    def get_tag_service(self):
        if '_tagservice' in dir(self):
            return self._tagservice
        else:
            self._tagservce = TagService(session())
            return self._tagservce

    def test_create_tag(self):
        tag_service = self.get_tag_service()
        test_tag = {
            "name": "First Tag"
        }
        item = tag_service.create(test_tag)
        retrieved = tag_service.find(item)
        self.created_id = item
        assert retrieved.name == test_tag["name"]
        assert approx_same(retrieved.created, retrieved.updated)

    def test_rename_tag(self):
        tag_service = self.get_tag_service()
        test_tag = {
            "name": "Unupdated"
        }
        item = tag_service.create(test_tag)
        tag_service.update(item, {"name": "updated_tag"})
        new_item = tag_service.find(item)
        assert new_item.name == "updated_tag"

    def test_delete_tag(self):
        tag_service = self.get_tag_service()
        test_tag = {
            "name": "to be deleted"
        }
        item = tag_service.create(test_tag)
        tag_service.delete(item)
        deleted_tag = tag_service.find(item)
        assert deleted_tag is None

