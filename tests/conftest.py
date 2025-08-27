# tests/conftest.py
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete

from app.db import Base, get_session
from app.main import app
from app.models import Price

@pytest.fixture(scope="session")
def engine(tmp_path_factory):
    # create a unique temp directory and file for this test session
    db_dir = tmp_path_factory.mktemp("data")
    db_file = db_dir / "test.db"
    url = f"sqlite:///{db_file}"
    engine = create_engine(url, connect_args={"check_same_thread": False})
    # create tables
    Base.metadata.create_all(bind=engine)
    yield engine
    # teardown: dispose engine to release sqlite file lock, then remove file
    engine.dispose()
    try:
        if db_file.exists():
            db_file.unlink()
    except PermissionError:
        # on rare occasions Windows still locks file; ignore and let OS cleanup later
        pass

@pytest.fixture()
def testing_session(engine):
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSessionLocal()
    try:
        # ensure clean table at start of each test
        session.execute(delete(Price))
        session.commit()
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture()
def client(testing_session):
    # make FastAPI use the testing session
    def override_get_session():
        try:
            yield testing_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
