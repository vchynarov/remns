import pytest
import time # sleep for approx timestamp comparison
from fixtures import session, post_service, tag_service, tagging_service
from datetime import datetime


def find(items, key, value):
    return filter(lambda item: getattr(item, key) == value, items)[0]

def extract(items, key):
    return map(lambda item: getattr(item, key), items)


post_service = post_service(session())
last_year_id = post_service.create({
    "title": "Old Post",
    "content": "Initial content",
    "mode": "published"
})
this_year_id = post_service.create({
    "title": "This year post",
    "content": "Other content",
    "mode": "draft"
})
this_year_diff_month_id = post_service.create({
    "title": "newer post",
    "content": "Newer content",
    "mode": "published"
})
last_year = post_service.find(last_year_id)
this_year = post_service.find(this_year_id)
this_year_diff_month = post_service.find(this_year_diff_month_id)
last_year.created = datetime(2013, 03, 01)
this_year.created = datetime(2015, 01, 01)
this_year_diff_month.created = datetime(2015, 03, 01)


def test_year_query():
    this_year_posts = post_service.get_posts_by_date(2015)
    assert sorted([post.id for post in this_year_posts]) == sorted([this_year.id, this_year_diff_month.id])

def test_month_query():
    this_month_posts = post_service.get_posts_by_date(2015, 03, 01)
    assert len(this_month_posts) == 1
    assert this_month_posts[0].id == this_year_diff_month_id

def test_specific_post():
    pass