from mariadb import connect


def _get_connection():
    try:
        conn = connect(
            user='root',
            password='2210',
            host='localhost',
            port=3306,
            database='forum_system_schema'
        )
        print("Connected to the database!")

        return conn
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
