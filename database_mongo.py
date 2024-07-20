from envs import mongo_uri, mongo_db, mongo_password, mongo_username

from typing import Any
import json
import pymongo
import requests


requests.get

mc = pymongo.MongoClient(mongo_uri)
mongo_database = mc[mongo_db]

def _wrap_cursor_(cursor: pymongo.CursorType) -> pymongo.CursorType | None:
    return cursor if cursor.alive else None

def create_tables():
    existing_collections = mongo_database.list_collection_names()

    # Create collections if they don't alredy exist
    if 'users' not in existing_collections:
        mongo_database.create_collection('users')
    if 'allorders' not in existing_collections:
        mongo_database.create_collection('allorders')

    print('MongoDB tables created:')
    print(*mongo_database.list_collection_names())
    

def db_add_user(user: dict[str, str]):
    users = mongo_database.users
    users.replace_one({'_id': user['_id']}, user, upsert=True)
    
def db_get_user(id: str):
    db = mongo_database
    users = db.users
    
    user = users.find_one({'_id': id})
    return user

def db_change_user_state(id: str, state: str):
    users = mongo_database.users
    print(f"changing state of: {id} to {state}")
    user = users.update_one({'_id': id}, {'$set' : {'state' : state}})
    print(user)

def db_promote_user(id: str):
    users = mongo_database.users
    users.update_one({'_id': id}, {'$set' : {'lvl': 'admin'}})

def db_ban_user(id: str):
    users = mongo_database.users
    users.update_one({'_id': id}, {'$set' : {'lvl': 'banned'}})

def db_unban_user(id: str):
    users = mongo_database.users
    users.update_one({'_id': id}, {'$set' : {'lvl': 'user'}})

def db_add_order(order: dict[str: Any]):
    orders = mongo_database.allorders
    orders.replace_one({'_id': order['_id']}, order, upsert=True)
    return order
    
def db_get_order(id: str):
    orders = mongo_database.allorders
    order = orders.find_one({'_id': id})
    return order


def db_confirm_order(id: str):
    allorders = mongo_database.allorders
    
    order_to_conf = allorders.find_one({'_id': id})
    if order_to_conf is None:
        raise KeyError
    allorders.update_one({'_id': order_to_conf['_id']}, {'$set': {'confirmed': True}})


def db_delete_order(id: str):
    orders = mongo_database.allorders
    orders.delete_one({'_id': id})


def db_get_admin_users():
    users = mongo_database.users
    resp = users.find({'lvl': 'admin'})
    resp = _wrap_cursor_(resp)
    if resp is None:
        return None
    
    return (user for user in resp)

def db_get_all_users(user_id: str | None = None):
    users = mongo_database.users
    if user_id == None:
        resp = users.find()
    else:
        resp = users.find({'_id': user_id})
    resp = _wrap_cursor_(resp)
    if resp is None:
        return None
    
    return (user for user in resp)


def db_get_all_orders(user_id: str | None = None):
    allorders = mongo_database.allorders
    if user_id == None:
        resp = allorders.find({'confirmed': False})
    else:
        resp = allorders.find({'user_id': user_id, 'confirmed': False})
    resp = _wrap_cursor_(resp)
    if resp is None:
        return None
    
    return (order for order in resp)


def db_get_confirmed_orders(user_id: str | None = None):
    allorders = mongo_database.allorders
    if user_id == None:
        resp = allorders.find({'confirmed': True})
    else:
        resp = allorders.find({'user_id': user_id, 'confirmed': True})
    resp = _wrap_cursor_(resp)
    if resp is None:
        return None
    
    return (order for order in resp)
