from envs import redis_password

from typing import Any
import redis
import json

rc = redis.Redis(
        host="redis-server",
        port=6379,
        password=redis_password,
        decode_responses=True,
)

def db_add_user(user: dict[str, str]):
    resp = rc.set(user['key'], json.dumps(user))


def db_get_user(id: str) -> dict[str, Any] | None:
    resp = json.loads(rc.get(id))
    return resp


def db_promote_user(id: str):
    resp = json.loads(rc.get(id))
    resp['lvl'] = 'admin'
    db_add_user(resp)

def db_add_order(order_data: dict[str, Any]):
    