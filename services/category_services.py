from data.database_queries import insert_query, update_query, read_query
from data.schemas import CreateCategory, CategoryOut


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
