import pytest

from writer import db

@pytest.fixture
def db_conn():
    conn = db.connect(database='aiven',
                      user='aiven',
                      password='aiven',
                      host='test_postgres',
                      port='5432')

    db.prepare_db(conn)

    yield conn

    db.drop_table(conn)

    conn.close()