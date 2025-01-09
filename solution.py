import psycopg2
from psycopg2.extras import RealDictCursor

from settings import TEST_DB_URL

conn = psycopg2.connect(TEST_DB_URL)


# BEGIN (write your solution here)
def create_post(conn, post):
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        query = """INSERT INTO posts (title, content, author_id) 
        VALUES (%s, %s, %s) RETURNING id;"""
        curs.execute(query, (post['title'], post['content'], post['author_id']))
        post_id = curs.fetchone()['id']
    conn.commit()
    return post_id


def add_comment(conn, comment):
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        query = """INSERT INTO comments (post_id, author_id, content)
        VALUES (%s, %s, %s) RETURNING id;"""
        curs.execute(query, (comment['post_id'], comment['author_id'], comment['content']))
        comment_id = curs.fetchone()['id']
    conn.commit()
    return comment_id


def get_latest_posts(conn, n):
    query = """
        SELECT 
            posts.id AS post_id, 
            posts.title, 
            posts.content, 
            posts.author_id AS post_author_id, 
            posts.created_at AS post_created_at,
            comments.id AS comment_id,
            comments.author_id AS comment_author_id,
            comments.content AS comment_content,
            comments.created_at AS comment_created_at
        FROM posts
        LEFT JOIN comments ON posts.id = comments.post_id
        ORDER BY posts.created_at DESC, comments.created_at ASC
        LIMIT %s;
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, (n,))
        rows = cursor.fetchall()

    posts = {}
    for row in rows:
        post_id = row['post_id']
        if post_id not in posts:
            posts[post_id] = {
                'id': post_id,
                'title': row['title'],
                'content': row['content'],
                'author_id': row['post_author_id'],
                'created_at': row['post_created_at'],
                'comments': []
            }
        if row['comment_id']:
            posts[post_id]['comments'].append({
                'id': row['comment_id'],
                'author_id': row['comment_author_id'],
                'content': row['comment_content'],
                'created_at': row['comment_created_at']
            })
    return list(posts.values())
# END