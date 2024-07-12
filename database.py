from typing import Generator

import mysql
from mysql.connector.pooling import PooledMySQLConnection
import json

import database_queries
from envs import mysql_database_name, mysql_root_password


def db_get_connection() -> PooledMySQLConnection | None:
    try:
        conn = mysql.connector.connect(
            host='localhost:3306',
            user='root',
            password=mysql_root_password,
            database=mysql_database_name,
        )
    except mysql.connector.Error as err:
        print(f'Error connecting to database; {err}')
        return None
    else:
        return conn


def db_add_user(user: dict[str, str]):
    try:
        conn = db_get_connection()
        cursor = conn.cursor()

        values = (user['id'], user['lvl'], user['state'])
        cursor.execute(database_queries.add_user, values)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error adding user: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def db_get_user(id: str) -> dict[str, any] | None:
    try:
        conn = db_get_connection()
        cursor = conn.cursor()

        cursor.execute(database_queries.get_user, (id,))
        result = cursor.fetchone()
        if result:
            user_data = {
                'id': result[0],
                'lvl': result[1],
                'state': result[2]
            }
            return user_data
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Error retrieving user: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def db_promote_user(id):
    try:
        conn = db_get_connection()
        cursor = conn.cursor()

        cursor.execute(database_queries.modify_user_state, (id,))
        cursor.execute()

    except mysql.connector.Error as err:
        print(f"Error retrieving user: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def db_add_order(order_data: dict[str, any]):
    try:
        conn = db_get_connection()
        cursor = conn.cursor()

        data_json = json.dumps(order_data['data'])
        values = (order_data['id'], data_json, False, order_data['user_id'])
        cursor.execute(database_queries.add_user, values)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error adding user: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def db_confirm_order(order_id):
    try:
        conn = db_get_connection()
        cursor = conn.cursor()

        cursor.execute(database_queries.confirm_order, (order_id,))
        conn.commit()

        print(f"Order with ID {order_id} has been marked as confirmed.")

    except mysql.connector.Error as err:
        print(f"Error confirming order: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def db_get_order(id) -> dict[str, any] | None:
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="your_database"
        )
        cursor = conn.cursor()

        cursor.execute(database_queries.get_order, (id,))
        result = cursor.fetchone()

        if result:
            data = json.loads(result[1])
            order_data = {
                'id': result[0],
                'data': data,
                'is_confirmed': result[2]
            }
            return order_data
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Error retrieving order: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def db_delete_order(id):
    try:
        conn = db_get_connection()
        cursor = conn.cursor()

        cursor.execute(database_queries.delete_order, (id,))
        conn.commit()

        print(f"Order with ID {id} has been deleted.")

    except mysql.connector.Error as err:
        print(f"Error deleting order: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_admin_users() -> Generator[dict[str, str], any, None] | None:
    try:
        conn = db_get_connection()
        cursor = conn.cursor()

        cursor.execute(database_queries.get_admins)
        results = cursor.fetchall()
        if results is None:
            return None
        return ({'tg_id': row[0], 'lvl': row[1], 'state': row[2]} for row in results)

    except mysql.connector.Error as err:
        print(f"Error retrieving admin users: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_tables():
    conn = db_get_connection()
    if conn is None:
        raise IOError
    try:
        cursor = conn.cursor()
        cursor.execute(database_queries.create_user_table)
        conn.commit()
        cursor.execute(database_queries.create_order_table)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def db_get_all_orders() -> Generator[dict[str, any], any, None] | None:
    try:
        conn = db_get_connection()
        cursor = conn.cursor()

        cursor.execute(database_queries.get_all_orders)
        results = cursor.fetchall()
        if results is None:
            return None

        return ({"key": row[0], 'data': json.loads(row[1]), 'id': row[2]} for row in results)

    except mysql.connector.Error as err:
        print(f"Error retrieving admin users: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def db_get_confirmed_orders() -> Generator[dict[str, any], any, None] | None:
    try:
        conn = db_get_connection()
        cursor = conn.cursor()

        cursor.execute(database_queries.get_confirmed_orders)
        results = cursor.fetchall()
        if results is None:
            return None

        return ({"key": row[0], 'data': json.loads(row[1]), 'id': row[2]} for row in results)

    except mysql.connector.Error as err:
        print(f"Error retrieving admin users: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()