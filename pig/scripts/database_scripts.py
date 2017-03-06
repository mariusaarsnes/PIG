__author__ = 'owner_000'
from pig.db.models import *
from pig.views import database

def test_query():
    return database.get_session().query(User).filter(True).first()