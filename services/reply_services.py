from datetime import datetime

from mariadb import IntegrityError

from data.database_queries import insert_query, read_query, update_query
from data.schemas import UserReply, ReplyOut


def create(content: str, topic_id: int, user_id: int, category_id):
    check_user_access = read_query('SELECT access_type from category_has_user WHERE user_id = ? AND category_id = ?', (user_id, category_id))
    user_access = check_user_access[0][0]

    if user_access == 'read access':
        return f"user with id {user_id} has read only access"

    generated_id = insert_query(
        'INSERT INTO reply(content, topic_id) VALUES (?, ?)',
        (content, topic_id))

    insert_query(
        'INSERT INTO votes(user_id, reply_id) VALUES (?, ?)', (user_id, generated_id))

    created_at_result = read_query('SELECT created_at FROM reply WHERE id = ?', (generated_id,))
    created_at = created_at_result[0][0].strftime("%Y-%m-%d %H:%M:%S")

    return ReplyOut(id=generated_id, content=content, topic_id=topic_id, created_at=created_at)


def change_vote_status(reply_id, vote_status, current_user_id):
    vote_data = update_query('update votes set status = ? where reply_id = ? and user_id = ? ',
                             (vote_status, reply_id, current_user_id))

    # return True if update query was successful
    return vote_data
