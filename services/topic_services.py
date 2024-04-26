from mariadb import IntegrityError

from data.database_queries import insert_query
from data.models import Topic
from data.schemas import TopicCreate


def create(name: str, category_id: int, user_id: int) -> Topic | None:
    try:
        generated_id = insert_query(
            'INSERT INTO topic(topic_name, category_id, user_id) VALUES (?, ?, ?)',
            (name, category_id, user_id))
        return Topic(id=generated_id, name=name, category_id=category_id, user_id=user_id)

    except IntegrityError as e:
        # Here you could log the error message
        print(f"An error occurred: {e}")
        return None
