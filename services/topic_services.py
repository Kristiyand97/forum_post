from mariadb import IntegrityError

from data.database_queries import insert_query, read_query, update_query
from data.models import Topic
from data.schemas import TopicCreate, ViewTopic, ViewReply


def get_all_topics(search: str = None, sort: str = None, pagination: int = None):
    topics_data = read_query('select id,topic_name,category_id,created_at from topic')

    if search:
        topics_data = read_query('select id,topic_name,category_id,created_at from topic where topic_name = ?',
                                 sql_params=(search,))
        if not topics_data:
            return 'wrong search parameter'

    if sort:
        if 'asc' in sort or 'desc' in sort:
            reverse = 'desc' in sort
            topics_data = sorted(topics_data, key=lambda t: t[3], reverse=reverse)
        else:  # if sort parameter value is wrong -> return 'wrong sort parameter'
            return 'wrong sort parameter'

    return (ViewTopic(id=id, topic_name=topic_name, category_id=category_id, created_at=created_at) for
            id, topic_name, category_id, created_at in topics_data)


def get_topic_by_id(id: int):
    topic_data = read_query('select id,topic_name,category_id,created_at,user_id from topic where id=?',
                            sql_params=(id,))

    if not topic_data:
        return 'wrong topic id'

    topic_user_creator_data = read_query('select username from user where id=?', sql_params=(topic_data[0][4],))
    topic_user_creator = str(topic_user_creator_data[0][0])

    reply_data = read_query('select id, content, created_at from reply where topic_id = ?', sql_params=(id,))
    replies = (ViewReply(id=id, content=content, created_at=created_at) for id, content, created_at in reply_data)

    if not reply_data:  # check if the current topic has replies, if not, return 'no replies' as result in JSON response
        replies = 'no replies'

    topics = {
        "id": topic_data[0][0],
        "topic_name": topic_data[0][1],
        "category_id": topic_data[0][2],
        "created_at": topic_data[0][3],
        "creator": topic_user_creator,
        "creator_id": topic_data[0][4],
        "replies": replies
    }

    return topics


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
        return Topic(id=generated_id, topic_name=topic_name, category_id=category_id, user_id=user_id,
                     best_reply_id=None)

    except IntegrityError as e:
        print(f"An error occurred: {e}")
        return None


def update_best_reply(topic_id: int, reply_id: int, owner_id: int):
    reply_data = update_query('update topic set best_reply_id=? where id = ? and user_id = ?',
                              (reply_id, topic_id, owner_id))

    return reply_data
