import os

import pytest
from fastapi.testclient import TestClient
from loguru import logger

from definitions import ROOT_DIR
from tests.assets import AUTHORS, POSTS, TOPICS


@pytest.fixture(scope='session')
def init_sqlite_database():
    path = ROOT_DIR / 'test.db'
    path.unlink(missing_ok=True)
    path.touch(exist_ok=True)

    yield path

    path.unlink()


@pytest.fixture(scope='session')
def client(init_sqlite_database):
    path = init_sqlite_database
    os.environ[
        'DATABASE_URL'
    ] = f'sqlite:///{path.name}?check_same_thread=False'
    os.environ['ENVIRONMENT'] = 'TEST'
    os.environ['PAGE_SIZE'] = '5'
    logger.info(os.environ.get('DATABASE_URL'))

    from app.config import config
    from app.main import app

    logger.info(config.PAGE_SIZE)

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='module')
def client_with_data(client):
    from app.core.engine import get_session

    session = next(get_session())
    for init_data in [AUTHORS, TOPICS, POSTS]:
        session.add_all(init_data)

    session.commit()

    yield client

    from sqlalchemy.orm import close_all_sessions

    close_all_sessions()


@pytest.fixture(scope='module')
def session():
    from app.core.engine import get_session

    s = next(get_session())

    yield s
