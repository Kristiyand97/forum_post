from mariadb import IntegrityError

from data.database_queries import insert_query, read_query
from data.schemas import ReplyCreate, UserReply


def create(content: str, topic_id: int, user_id: int) -> ReplyCreate | None:
    try:
        generated_id = insert_query(
            'INSERT INTO reply(content, topic_id) VALUES (?, ?)',
            (content, topic_id))

        insert_query(
            'INSERT INTO votes(user_id, reply_id) VALUES (?, ?)', (user_id, generated_id))

        return ReplyCreate(id=generated_id, content=content, topic_id=topic_id)

    except (IntegrityError, Exception) as e:

        print(f"An error occurred: {e}")
        return None


