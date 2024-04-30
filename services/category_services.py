from data.database_queries import insert_query, update_query, read_query
from data.schemas import CreateCategory, CategoryOut, ViewCategory, ViewTopicsInCategory


def view_all_categories():
    category_data = read_query('select id,name,created_at from category')
    return (ViewCategory(id=id, name=name, created_at=created_at) for id, name, created_at in category_data)


def view_topics_in_category(category_id: int, search: str = None, sort: str = None, pagination: int = None):
    category = read_query('select id from category where id=?',
                          sql_params=(category_id,))

    topics = read_query('select id,topic_name,category_id,created_at from topic where category_id=?',
                        sql_params=(category_id,))

    # check if category with this id exists
    if not category:
        return f'Category with id: {category_id} does not exist!'

    # check if category is empty(without topics)
    if not topics:
        return f'Category with id: {category_id} is empty!'

    if search:
        topics = read_query(
            'select id,topic_name,category_id,created_at from topic where category_id=? and topic_name = ?',
            sql_params=(category_id, search,))  # if search parameter value is wrong -> return empty list
        if not topics:  # if list is empty -> return 'wrong search parameter'
            return 'wrong search parameter'

    if sort:
        if 'asc' in sort or 'desc' in sort:
            reverse = 'desc' in sort
            topics = sorted(topics, key=lambda t: t[3], reverse=reverse)
        else:  # if sort parameter value is wrong -> return 'wrong sort parameter'
            return 'wrong sort parameter'

    return (ViewTopicsInCategory(topic_id=id, topic_name=topic_name, category_id=category_id, created_at=created_at) for
            id, topic_name, category_id, created_at in topics)


def create(name: str, is_private: bool, is_locked: bool):
    generated_id = insert_query(
        'INSERT INTO category(name, is_private, is_locked) VALUES(?, ?, ?)',
        (name, is_private, is_locked))
    created_at_result = read_query('SELECT created_at FROM category WHERE id = ?', (generated_id,))
    created_at = created_at_result[0][0].strftime("%Y-%m-%d %H:%M:%S")

    return CategoryOut(id=generated_id, name=name, is_private=is_private, is_locked=is_locked, created_at=created_at)


def update_category(category_id: int, is_private: bool, is_locked: bool):
    update_query(
        'UPDATE category SET is_private = ?, is_locked = ? WHERE id = ?',
        (is_private, is_locked, category_id))
