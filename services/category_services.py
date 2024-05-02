from data.database_queries import insert_query, update_query, read_query
from data.schemas import CreateCategory, CategoryOut, ViewCategory, ViewTopicsInCategory, ChangeCategoryVisibility


def view_all_categories():
    category_data = read_query('select id,name,created_at from category')
    return (ViewCategory(id=id, name=name, created_at=created_at) for id, name, created_at in category_data)


def view_topics_in_category(category_id: int, search: str = None, sort: str = None, pagination: int = None):
    category_data = read_query('select id,is_private from category where id=?',
                               sql_params=(category_id,))
    # category_users_data = read_query('select user_id from category_has_user where category_id=?', (category_id,))
    # category_users = [u for u in category_users_data]

    topics = read_query('select id,topic_name,category_id,created_at from topic where category_id=?',
                        sql_params=(category_id,))

    is_private = category_data[0][1]

    # check if category_data with this id exists
    if not category_data:
        return f'Category with id: {category_id} does not exist!'

    # check if category_data is empty(without topics)
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


def create(name: str, is_private: bool, is_locked: bool, current_user: int):
    admin_data = read_query('select is_admin from user where id=?', (current_user,))
    is_admin = admin_data[0][0]

    if not is_admin:
        return 'not admin'

    generated_id = insert_query(
        'INSERT INTO category(name, is_private, is_locked) VALUES(?, ?, ?)',
        (name, is_private, is_locked))
    created_at_result = read_query('SELECT created_at FROM category WHERE id = ?', (generated_id,))
    created_at = created_at_result[0][0].strftime("%Y-%m-%d %H:%M:%S")

    return CategoryOut(id=generated_id, name=name, is_private=is_private, is_locked=is_locked, created_at=created_at)


def update_category(category_id: int, is_private: bool, is_locked: bool) -> bool:
    category_data = update_query(
        'UPDATE category SET is_private = ?, is_locked = ? WHERE id = ?',
        (is_private, is_locked, category_id))

    if category_data:
        return True
    else:
        return False


def change_visibility(category_id: int, is_private: bool, is_locked: bool, current_user: int):
    admin_data = read_query('select is_admin from user where id=?', (current_user,))
    is_admin = admin_data[0][0]
    if not is_admin:
        return 'not admin'
    old_category_data = read_query('SELECT is_private, is_locked FROM category WHERE id = ?', (category_id,))
    if not old_category_data:
        return None
    old_is_private, old_is_locked = old_category_data[0]
    category_visibility = update_category(category_id, is_private, is_locked)  # return True or False

    return {
        'visibility_changed': old_is_private != is_private,
        'lock_status_changed': old_is_locked != is_locked,
        'update_successful': category_visibility
    }
