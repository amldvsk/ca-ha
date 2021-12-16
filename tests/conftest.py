import pytest

from todoapp import create_app
from todoapp import DbConnector
import os
with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    with app.app_context():
        DbConnector.getInstance().init_db()
        DbConnector.getInstance().get_db().executescript(_data_sql)
    yield app



@pytest.fixture
def client(app):
    return app.test_client()