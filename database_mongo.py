from envs import mongo_uri, mongo_db, mongo_password, mongo_username

from typing import Any
import json
import pymongo
import requests


requests.get

mc = pymongo.MongoClient(mongo_uri)
mongo_database = mc[mongo_db]

def create_tables():
    existing_collections = mongo_database.list_collection_names()

    # Create collections if they don't alredy exist
    if 'users' not in existing_collections:
        mongo_database.create_collection('users')
    if 'allorders' not in existing_collections:
        mongo_database.create_collection('allorders')
    if 'conforders' not in existing_collections:
        mongo_database.create_collection('conforders')

    print('MongoDB tables created:')
    print(*mongo_database.list_collection_names())
    

def db_add_user(user: dict[str, str]):
    users = mongo_database.users
    users.insert_one(user)
    
def db_get_user(id: str):
    db = mongo_database
    users = db.users
    
    user = users.find({'id': id})
    return user

def db_promote_user(id: str):
    users = mongo_database.users
    
    user = users.find_one_and_update({'id': id}, {'$set' : {'lvl' : 'admin'}})


def db_add_order(order: dict[str: Any]):
    orders = mongo_database.allorders
    
    orders.insert_one(order)
    
def db_get_order(id: str):
    orders = mongo_database.allorders
    
    order = orders.find_one({'id': id})
    return order


def db_confirm_order(id: str):
    allorders = mongo_database.allorders
    conforders = mongo_database.conforders
    
    order_to_conf = allorders.find_one({'id': id})
    if order_to_conf is None:
        raise KeyError
    conforders.insert_one(order_to_conf['id'])
    allorders.delete_one({'id': order_to_conf['id']})


def db_delete_order(id: str):
    orders = mongo_database.allorders
    orders.delete_one({'id': id})


def db_get_admin_users():
    users = mongo_database.users
    resp = users.find({'lvl': 'admin'})
    if resp is None:
        return None
    
    return (user for user in resp)


def db_get_all_orders():
    allorders = mongo_database.allorders
    resp = allorders.find()
    if resp is None:
        return None
    
    return (order for order in resp)


def db_get_confirmed_orders():
    conforders = mongo_database.conforders
    resp = conforders.find()
    if resp is None:
        return None
    
    return (order for order in resp)
