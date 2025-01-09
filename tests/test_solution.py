from solution import get_latest_posts, add_comment, create_post


def test_solution(db_transaction):
    assert get_latest_posts(db_transaction, 1) == []

    post = {'title': 'My Super Post', 'content': 'text', 'author_id': 42}
    post_id = create_post(db_transaction, post)

    comment_1 = {'post_id': post_id, 'author_id': 42, 'content': 'wow such post'}
    comment_2 = {'post_id': post_id, 'author_id': 24, 'content': 'totally disagree btw i use arch'}
    comment_1_id = add_comment(db_transaction, comment_1)
    comment_2_id = add_comment(db_transaction, comment_2)

    latest_post = get_latest_posts(db_transaction, 1)[0]
    latest_post_comment_1 = next(c for c in latest_post['comments'] if c['id'] == comment_1_id)
    latest_post_comment_2 = next(c for c in latest_post['comments'] if c['id'] == comment_2_id)

    assert latest_post_comment_1['content'] == comment_1['content']
    assert latest_post_comment_2['content'] == comment_2['content']