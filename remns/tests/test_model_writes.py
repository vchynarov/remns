import pytest
import time # sleep for approx timestamp comparison
from fixtures import session, post_service, tag_service, tagging_service
from datetime import datetime


def approx_same(time1, time2):
    """
    When checking for update, make sure that time differences are in fact,
    different.

    :param time1:
    :param time2:
    :return: bool
    """
    return abs((time2-time1).total_seconds()) < 0.01


def find(items, key, value):
    return filter(lambda item: getattr(item, key) == value, items)[0]

def extract(items, key):
    return map(lambda item: getattr(item, key), items)

class TestPostServiceWrites(object):
    # uses Global to test updates
    def test_create_basic_draft(self, post_service):
        test_post = {
            "title": "My first test post.",
            "content": "Here is some content",
            "mode": "draft"
        }
        model = post_service.create(test_post)
        retrieved = post_service.find(model.id)
        self.created_draft_id = model.id

        assert retrieved.title == "My first test post."
        assert approx_same(retrieved.created, retrieved.updated) 
        assert "my-first-test-post" in retrieved.web_title
        assert retrieved.raw_content == test_post['content']
        assert retrieved.display_content == '<p>Here is some content</p>\n' 
        assert retrieved.id == model.id
        assert not retrieved.published

    # uses Global to test updates
    def test_create_basic_published(self, post_service):
        test_post = {
            "title": "My second test post.",
            "content": "Some more content",
            "mode": "published"
        }

        model = post_service.create(test_post)
        retrieved = post_service.find(model.id)
        assert approx_same(retrieved.created, retrieved.updated)
        assert retrieved.title == test_post['title']
        assert "my-second-test-post" in retrieved.web_title
        assert retrieved.raw_content == test_post['content']
        assert retrieved.display_content == '<p>Some more content</p>\n' 
        assert retrieved.id == model.id
        assert retrieved.published
    
    # secondary test
    def test_update_basic_draft(self, post_service):
        test_post = {
            "title": "To be updated post",
            "content": "Initial content",
            "mode": "draft"
        }
        updates = {
            "title": "Updated title",
            "content": "Updated content",
            "mode": "published"
        }

        model = post_service.create(test_post)
        # time for updates
        time.sleep(0.1)
        post_service.update(model.id, updates)
        retrieved = post_service.find(model.id)
        assert retrieved.id == model.id
        # web title should not change!
        assert "to-be-updated-post" in retrieved.web_title
        assert retrieved.title == "Updated title"
        assert not approx_same(retrieved.created, retrieved.updated)
        assert retrieved.raw_content == updates['content']
        assert retrieved.display_content == '<p>Updated content</p>\n' 
        assert retrieved.published

    def test_delete_post(self, post_service):
        test_post = {
            "title": "Post to be deleted",
            "content": "Some more content",
            "mode": "published"
        }
        model = post_service.create(test_post)
        post_service.delete(model.id)
        deleted_post = post_service.find(model.id)
        assert deleted_post is None

class TestTagService(object):
    def test_create_new_tags(self, tag_service):
        api_tags = [
            {"status": "created", "value": "python"},
            {"status": "created", "value": "tooling"},
            {"status": "created", "value": "gulp"},
            {"status": "created", "value": "sinatra"}
        ]
        resulting_ids = tag_service.initialize_tags(api_tags)
        all_tags = tag_service.get_all()
        assert sorted(resulting_ids) == sorted([tag.id for tag in all_tags])

    def test_create_some_new_tags(self, tag_service):
        initial_api_tags = [
            {"status": "created", "value": "tooling"},
            {"status": "created", "value": "gulp"}
        ]
        tag_service.initialize_tags(initial_api_tags)
        all_tags = tag_service.get_all()
        tooling = find(all_tags, "name", "tooling")
        gulp = find(all_tags, "name", "gulp")
        new_api_tags = [
            {"status": "existing", "value": tooling.id},
            {"status": "existing", "value": gulp.id},
            {"status": "created", "value": "python"},
            {"status": "created", "value": "django"}
        ]
        tag_service.initialize_tags(new_api_tags)
        updated_all_tags = tag_service.get_all()
        assert len(updated_all_tags) > len(all_tags)
        assert find(updated_all_tags, "name", "python")
        assert find(updated_all_tags, "name", "django")


    def test_create_tag(self, tag_service):
        test_tag = {
            "name": "First Tag"
        }
        model = tag_service.create(test_tag)
        retrieved = tag_service.find(model.id)
        self.created_id = model.id
        assert retrieved.name == test_tag["name"]
        assert approx_same(retrieved.created, retrieved.updated)

    def test_delete_tag(self, tag_service):
        test_tag = {
            "name": "to be deleted"
        }
        model = tag_service.create(test_tag)
        tag_service.delete(model.id)
        deleted_tag = tag_service.find(model.id)
        assert deleted_tag is None

class TestTaggingService(object):
    def test_create_post_new_tags(self, post_service, tag_service, tagging_service):
        test_post = {
            "title": "To be updated post",
            "content": "Initial content",
            "mode": "draft"
        }
        api_tags = [
            {"status": "created", "value": "python"},
            {"status": "created", "value": "tooling"},
            {"status": "created", "value": "gulp"},
            {"status": "created", "value": "sinatra"}
        ]
        tag_service.initialize_tags(api_tags)
        new_post = post_service.create(test_post)
        all_tags = tag_service.get_all()
        sinatra = find(all_tags, "name", "sinatra")
        python = find(all_tags, "name", "python")
        tagging_service.set_tags(new_post.id, [sinatra.id, python.id])
        updated_post = post_service.find(new_post.id)
        assert sorted(extract([sinatra, python], "name")) == sorted(extract(updated_post.tags, "name"))

    def test_update_post_new_tags(self, post_service, tag_service, tagging_service):
        test_post = {
            "title": "To be updated post",
            "content": "Initial content",
            "mode": "draft"
        }
        api_tags = [
            {"status": "created", "value": "python"},
            {"status": "created", "value": "tooling"},
            {"status": "created", "value": "gulp"},
            {"status": "created", "value": "sinatra"}
        ]
        tag_service.initialize_tags(api_tags)
        new_post = post_service.create(test_post)
        all_tags = tag_service.get_all()
        # Set two tags at first
        tagging_service.set_tags(new_post.id, [tag.id for tag in all_tags])
        sinatra = find(all_tags, "name", "sinatra")
        python = find(all_tags, "name", "python")
        tagging_service.set_tags(new_post.id, [sinatra.id, python.id])
        updated_post = post_service.find(new_post.id)
        assert sorted(extract([sinatra, python], "name")) == sorted(extract(updated_post.tags, "name"))