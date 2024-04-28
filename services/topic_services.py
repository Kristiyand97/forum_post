from mariadb import IntegrityError

from data.database_queries import insert_query, read_query
from data.models import Topic
from data.schemas import TopicCreate


# def create(name: str) -> Topic | None:
#     try:
#         generated_id = insert_query(
#             'INSERT INTO topic(topic_name) VALUES (?)',
#             (name,))
#         return Topic(id=generated_id, name=name)
#
#     except IntegrityError as e:
#         # Here you could log the error message
#         print(f"An error occurred: {e}")
#         return None


def category_exists(category_id: int) -> bool:
    result = read_query('SELECT id FROM category WHERE id = ?', (category_id,))
    return result is not None


def create(topic_name: str, category_id: int, user_id: int) -> Topic | None:
    if not category_exists(category_id):
        print(f"Category ID {category_id} does not exist.")
        return None

    try:
        generated_id = insert_query(
            'INSERT INTO topic(topic_name, category_id, user_id) VALUES (?, ?, ?)',
            (topic_name, category_id, user_id))
        return Topic(id=generated_id, topic_name=topic_name, category_id=category_id, user_id=user_id, best_reply_id=None)

    except IntegrityError as e:
        print(f"An error occurred: {e}")
        return None
