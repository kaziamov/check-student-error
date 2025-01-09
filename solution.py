import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect('postgresql://tirion:secret@localhost:5432/tirion')


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
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT
                p.*,
                c.id as comment_id,
                c.author_id as comment_author_id,
                c.content as comment_content,
                c.created_at as comment_created_at
            FROM posts p
            LEFT JOIN comments c ON p.id = c.post_id
            WHERE p.id IN (
                SELECT id FROM posts
                ORDER BY created_at DESC
                LIMIT %s
            )
        """, (n,))

        rows = cur.fetchall()

        posts_dict = {}
        for row in rows:
            post_id = row['id']
            if not posts_dict.get(post_id):
                posts_dict[post_id] = {
                    'id': row['id'],
                    'title': row['title'],
                    'content': row['content'],
                    'author_id': row['author_id'],
                    'created_at': row['created_at'],
                    'comments': []
                }

            if row.get('comment_id'):
                posts_dict[post_id]['comments'].append({
                    'id': row['comment_id'],
                    'author_id': row['comment_author_id'],
                    'content': row['comment_content'],
                    'created_at': row['comment_created_at']
                })

        return list(posts_dict.values())

# END