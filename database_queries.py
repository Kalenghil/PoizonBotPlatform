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
        key INT AUTO_INCREMENT PRIMARY KEY,
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
    UPDATE users SET state = '%s' WHERE id = %s
"""

get_admins = """
    SELECT (tg_id, level, state) FROM users WHERE level = 'admin'
"""

add_order = """
    INSERT INTO orders (data, is_confirmed, user_id) VALUES (%s, %s, %s)
"""

confirm_order = "UPDATE orders SET is_confirmed = TRUE WHERE key = %s"

get_order = """
    SELECT key, data, is_confirmed, user_id FROM orders WHERE key = %s
"""

delete_order = """
    DELETE FROM orders WHERE key = %s
"""

get_all_orders = """
    SELECT (key, data, user_id) FROM users
"""

get_confirmed_orders = """
    SELECT (key, data, user_id) FROM users WHERE is_confirmed = TRUE
"""