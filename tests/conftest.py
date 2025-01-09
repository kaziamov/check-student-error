import pytest
import psycopg2
import psycopg2.extras

from settings import TEST_DB_URL


@pytest.fixture(scope="session")
def db_connection():
    conn = psycopg2.connect(TEST_DB_URL)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    yield conn
    conn.close()


@pytest.fixture(autouse=True)
def reset_table(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("""
        DROP TABLE IF EXISTS posts;
        DROP TABLE IF EXISTS comments;
        
        CREATE TABLE posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE comments (
            id SERIAL PRIMARY KEY,
            post_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    db_connection.commit()


@pytest.fixture(scope="function")
def db_transaction(db_connection):
    with db_connection:
        with db_connection.cursor() as cur:
            cur.execute("BEGIN")
            yield db_connection
            cur.execute("ROLLBACK")