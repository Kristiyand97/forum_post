from mariadb import IntegrityError

from data.database_queries import insert_query, read_query
from data.schemas import Message, ViewConversation
from datetime import datetime


def create_message(content: str, receiver_id: int, sender_id: int):
    try:
        generated_id = insert_query('insert into messages (content,receiver_id,sender_id) values (?,?,?)',
                                    (content, receiver_id, sender_id))
        time = datetime.now()

        return Message(id=generated_id, created_at=time, content=content, receiver_id=receiver_id, sender_id=sender_id)

    except IntegrityError as e:
        print(f"An error occurred: {e}")
        return None


def get_conversations(current_user: int):
    messages = read_query('SELECT * FROM messages WHERE sender_id = ? OR receiver_id = ?', (current_user, current_user))

    return (ViewConversation.from_query_result(*message) for message in messages)


def get_conversation_with_user(current_user: int):
    messages = read_query('SELECT * FROM messages WHERE sender_id = ?', (current_user,))
    return (ViewConversation.from_query_result(*message) for message in messages)
