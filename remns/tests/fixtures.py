import pytest
import sys
import os

sys.path.append(os.path.realpath('./remns')) # Test working directory from main remns dir.

# Fixtures
@pytest.fixture
def session():
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    from models import Base
    TestSession = sessionmaker()
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine, checkfirst=True)
    TestSession.configure(bind=engine)
    return TestSession

@pytest.fixture
def post_service(session):
    from models import PostService
    return PostService(session)

@pytest.fixture
def tag_service(session):
    from models import TagService
    return TagService(session)

@pytest.fixture
def tagging_service(session):
    from models import TaggingService
    return TaggingService(session)