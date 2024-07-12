create_user_table = """
    CREATE TABLE IF NOT EXISTS users (
        tg_id INT,
        level VARCHAR(32),
        state VARCHAR(100),
        PRIMARY KEY(tg_id)
    );
"""

create_order_table = """
    CREATE TABLE IF NOT EXISTS orders (
        id VARCHAR(32),
        data JSON,
        is_confirmed BOOL,
        FOREIGN KEY(user_id) REFERENCES users(tg_id) 
    );
"""


add_user = """
    INSERT INTO users (tg_id, level, state) VALUES (%s, %s, %s) 
"""

get_user = """
    SELECT tg_id, level, state FROM users WHERE tg_id = %s
"""

modify_user_state = """
    UPDATE users SET state = %s WHERE id = %s
"""

get_admins = """
    SELECT (tg_id, level, state) FROM users WHERE level = "admin"
"""

add_order = """
    INSERT INTO orders (id, data, is_confirmed, user_id) VALUES (%s, %s, %s, %s)
"""

confirm_order = "UPDATE orders SET is_confirmed = TRUE WHERE id = %s"

get_order = """
    SELECT
"""