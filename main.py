from EmojiCaptcha import EmojiCaptcha
from envs import *
from database_mongo import *

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
from datetime import datetime
import minio
import requests
import secrets
import shutil
import uuid
import html
import json
import re
import io
from pydantic import BaseModel


base_url = "https://api.telegram.org/bot"

url=f"{base_url}{token}/sendMessage"
url_image=f"{base_url}{token}/sendPhoto"

def create_buckets(client: minio.Minio) -> None:
    if not client.bucket_exists(user_bucket):
        client.make_bucket(user_bucket)

app = FastAPI()
security = HTTPBasic()
minio_client = minio.Minio(
    'minio:9000',
    access_key=minio_access_key,
    secret_key=minio_secret_key,
    secure=False,
)
user_bucket = 'users'
config_bucket = 'config'
print('trying to create tables')
create_tables()
print('trying to create buckets')
create_buckets(minio_client)

emojis = ['🃏', '🎤', '🎥', '🎨', '🎩', '🎬', '🎭', '🎮', '🎯', '🎱', '🎲', '🎷', '🎸', '🎹', '🎾', '🏀', '🏆', '🏈', '🏉', '🏐', '🏓', '💠', '💡', '💣', '💨', '💸', '💻', '💾', '💿', '📈', '📉', '📊', '📌', '📍', '📎', '📏', '📐', '📞', '📟', '📠', '📡', '📢', '📣', '📦', '📹', '📺', '📻', '📼', '📽', '🖥', '🖨', '🖲', '🗂', '🗃', '🗄', '🗜', '🗝', '🗡', '🚧', '🚨', '🛒', '🛠', '🛢', '🧀', '🌭', '🌮', '🌯', '🌺', '🌻', '🌼', '🌽', '🌾', '🌿', '🍊', '🍋', '🍌', '🍍', '🍎', '🍏', '🍚', '🍛', '🍜', '🍝', '🍞', '🍟', '🍪', '🍫', '🍬', '🍭', '🍮', '🍯', '🍺', '🍻', '🍼', '🍽', '🍾', '🍿', '🎊', '🎋', '🎍', '🎏', '🎚', '🎛', '🎞', '🐌', '🐍', '🐎', '🐚', '🐛', '🐝', '🐞', '🐟', '🐬', '🐭', '🐮', '🐯', '🐻', '🐼', '🐿', '👛', '👜', '👝', '👞', '👟', '💊', '💋', '💍', '💎', '🔋', '🔌', '🔪', '🔫', '🔬', '🔭', '🔮', '🕯', '🖊', '🖋', '🖌', '🖍', '🥚', '🥛', '🥜', '🥝', '🥞', '🦊', '🦋', '🦌', '🦍', '🦎', '🦏', '🌀', '🌂', '🌑', '🌕', '🌡', '🌤', '⛅️', '🌦', '🌧', '🌨', '🌩', '🌰', '🌱', '🌲', '🌳', '🌴', '🌵', '🌶', '🌷', '🌸', '🌹', '🍀', '🍁', '🍂', '🍃', '🍄', '🍅', '🍆', '🍇', '🍈', '🍉', '🍐', '🍑', '🍒', '🍓', '🍔', '🍕', '🍖', '🍗', '🍘', '🍙', '🍠', '🍡', '🍢', '🍣', '🍤', '🍥', '🍦', '🍧', '🍨', '🍩', '🍰', '🍱', '🍲', '🍴', '🍵', '🍶', '🍷', '🍸', '🍹', '🎀', '🎁', '🎂', '🎃', '🎄', '🎈', '🎉', '🎒', '🎓', '🎙', '🐀', '🐁', '🐂', '🐃', '🐄', '🐅', '🐆', '🐇', '🐕', '🐉', '🐓', '🐖', '🐗', '🐘', '🐙', '🐠', '🐡', '🐢', '🐣', '🐤', '🐥', '🐦', '🐧', '🐨', '🐩', '🐰', '🐱', '🐴', '🐵', '🐶', '🐷', '🐸', '🐹', '👁\u200d🗨', '👑', '👒', '👠', '👡', '👢', '💄', '💈', '🔗', '🔥', '🔦', '🔧', '🔨', '🔩', '🔰', '🔱', '🕰', '🕶', '🕹', '🖇', '🚀', '🤖', '🥀', '🥁', '🥂', '🥃', '🥐', '🥑', '🥒', '🥓', '🥔', '🥕', '🥖', '🥗', '🥘', '🥙', '🦀', '🦁', '🦂', '🦃', '🦄', '🦅', '🦆', '🦇', '🦈', '🦉', '🦐', '🦑', '⭐️', '⏰', '⏲', '⚠️', '⚡️', '⚰️', '⚽️', '⚾️', '⛄️', '⛅️', '⛈', '⛏', '⛓', '⌚️', '☎️', '⚜️', '✏️', '⌨️', '☁️', '☃️', '☄️', '☕️', '☘️', '☠️', '♨️', '⚒', '⚔️', '⚙️', '✈️', '✉️', '✒️']

reply_keyboard_buttons = {
  "Произвести расчет 🧑🏻‍💻": "/calculator",
  "Оформить заказ ✅": "/order",
  "Каталог товаров 🗳": "/items",
  "О нас ⚠️" : "/about",
  "Чат и отзывы 💬": "/contact",
  "FAQ 🛡": "/faq"
}

class sendMessage(BaseModel):
    update_id: int
    message: Optional[dict] = None
    callback_query: Optional[dict] = None

user_json_model = {
    "order": {
        "type": None,
        "link": None,
        "size": None,
        "price": None,
        "fio": None,
        "adress": None,
        "number": None,
        "captcha_answer": None,
    },
    "calc": {
        "type": None,
        "price": None
    }
}

item_weight = {
    "sneaker": 2000,
    "boot": 3000,
    "winterJacket": 1750,
    "jacket": 1350,
    "cotton": 450,
    "laptop": 3250,
    "smartphone": 300,
    "accessory": 250
}

item_size_type = {
    "sneaker": "number",
    "boot": "number",
    "winterJacket": "size",
    "jacket": "size",
    "cotton": "size",
    "laptop": None,
    "smartphone": None,
    "accessory": None
}



def check_regex(regex, string):
  pattern = re.compile(regex)
  if pattern.fullmatch(string):
    return True
  else:
    return False

price_config_path = 'price_conf.json'


def read_config_data() -> str:
    if not os.path.exists(price_config_path):
        default_price_config = {
            "kg_cost": 750.0,
            "change": 11.5,
            "commission": 700,
        }
        raw_json = json.dumps(default_price_config)
        with open(price_config_path, 'w') as config_file:
            config_file.write(raw_json)

    with open(price_config_path, 'r') as config_file:
        raw_json = config_file.read()
        return raw_json


def store_config_data(raw_json: str) -> None:
    with open(price_config_path, 'w') as config_file:
        config_file.write(raw_json)


def get_price_var(key: str) -> float | None:
    price_config = json.loads(read_config_data())
    if key in price_config:
        return price_config[key]
    else:
        return None


def get_price_vars(*keys: str) -> tuple | None:
    price_config = json.loads(read_config_data())
    if any(key not in price_config for key in keys):
        return None
    return tuple(price_config[key] for key in keys)


def set_price_var(key: str, value: float):
    price_config = json.loads(read_config_data())
    if key not in price_config:
        raise KeyError
    price_config[key] = value
    store_config_data(json.dumps(price_config))


def order_formula(type, price):
    price_vars = get_price_vars('commission', 'kg_cost', 'change')
    if price_vars is None:
        raise KeyError
    commission, kg_cost, change = price_vars
    if use_extended_formula:
        final_price = commission+((item_weight[type]/1000)*kg_cost)+(price*change)
    else:
        final_price = price * change + commission
    return final_price

def copy_file(current_path, new_path):
    shutil.copyfile(f"{str(current_path)}", f"{str(new_path)}")


def download_image(url, filename):
    try:
        response = requests.get(url, stream=True)
        with open(f'/tmp/{filename}.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    except Exception as e:
        copy_file(f"./{filename}.png", f"/tmp/{filename}.png")

if mainimage_url is not None:
    download_image(mainimage_url, "main")
else:
    copy_file("./main.png", "/tmp/main.png")

if aboutimage_url is not None:
    download_image(aboutimage_url, "about")
else:
    copy_file("./about.png", "/tmp/about.png")

if admin_id is not None:
    db_promote_user(admin_id)
# ------------------------------- MINIO FILE CONTROL FUNCTIONS -------------------------

def minio_get_userfile(filename: str):
    try:
        resp = minio_client.get_object(user_bucket, filename)
        byte_json = resp.read()
        raw_json = byte_json.decode('utf-8')
    except Exception as e:
        print('Error loading file from minio')
    else:
        print(f"Userfile {filename} got from minio")
        resp.close(); resp.release_conn()
        return raw_json
        


def minio_put_userfile(filename: str, contents: str):
    print('Minio adding userfile')
    raw_bytes = contents.encode('utf-8')
    print('Raw bytes')
    byte_buffer = io.BytesIO(raw_bytes)
    print('Buffer created')
    try:
        print('trying to add userfile')
        resp = minio_client.put_object(
            user_bucket,
            filename,
            data=byte_buffer,
            content_type='application/json',
            length=len(raw_bytes)
        )
        print('userfile created')
        print(f"Minio write result: {str(resp.http_headers)}")
    except Exception as e:
        print(f"Error writing userfile to minio: {e}")


# ------------------------------- DATA CONTROL FUNCTIONS -------------------------------

def create_userfile(id):
    filename = str(id)+'.json'
    print('Trying to put userfile')
    return minio_put_userfile(filename=filename, contents=json.dumps(user_json_model))

# ~USER FUNCTIONS~
def modify_userfile(id, val, field, category=None):
    filename = str(id)+'.json'
    user_data = json.loads(minio_get_userfile(filename))
    if category is None:
        user_data[field]=val
    else:
        user_data[category][field]=val
    return minio_put_userfile(filename=filename, contents=json.dumps(user_data))

def get_userfile(id):
    filename = str(id)+'.json'
    file = json.loads(minio_get_userfile(filename))
    return file

def add_user(id):
    user = db_add_user({
        "_id": str(id),
        "state": "MAIN_MENU",
        "lvl": "user"
    })
    print('creating userfile')
    create_userfile(id)
    return user

def add_admin(id):
    user = db_add_user({
        "_id": str(id),
        "state": "MAIN_MENU",
        "lvl": "admin"
    })
    create_userfile(id)
    return user

def get_user(id):
    user = db_get_user(str(id))
    return user if user else None

def change_user_state(id, state):
    print("Changing user state")
    user_old = get_user(id)
    user = db_change_user_state(str(id), state)

    return user

def get_admins():
    admins = db_get_admin_users()
    return admins if admins else None

def add_order(user_id, type, link, size, price, fio, adress, number):
    order = db_add_order({
        "_id": str(uuid.uuid4()),
        "user_id": user_id,
        "confirmed": False,
        "date": int(datetime.now().timestamp()),
        "data": {
            "product_type": type,
            "product_link": link,
            "product_size": size,
            "price": price,
            "fio": fio,
            "ship_to": adress,
            "phone_number": number
        }
    })
    return order

def get_order(key):
    order = db_get_order(str(key))
    return order if order else None

def confirm_order(id, key):
    order_from_all_orders = get_order(key)
    confirmed_order = None
    if order_from_all_orders is not None:
        send_confirm_prompt(order_from_all_orders["user_id"], order_from_all_orders)
        send_text(id, f"Заказ номер `{key}` подтверждён. Спасибо!")
        db_confirm_order(key)
    else:
        send_text(id, f"Заказ номер `{key}` уже обработан либо не найден.")
    return confirmed_order

def decline_order(id, key):
    parsed_order = get_order(key)
    deleted_order = None
    if parsed_order is not None:
        send_decline_prompt(parsed_order["user_id"], parsed_order)
        deleted_order = db_delete_order(key)
    content = send_text(id, f"Заказ номер `{key}` отклонён. Спасибо!")
    return content, deleted_order

def delete_order(id, order_id, cause: str | None =None):
    order = get_order(order_id)
    if order is None:
        resp = send_text(id, 'Заказ по данному id не найден')
        return resp
    else:
        db_delete_order(order_id)
    
    if cause is not None:
        send_text(order['user_id'], f"Ваш заказ был отменён по причине: {cause}")
    send_text(id, f'Заказ {order_id} был удалён')
    
    
def fetch_all_users():
    users = db_get_all_users()
    return users if users else None

def fetch_orders(user_id: str = None):
    orders = db_get_all_orders(user_id)
    return orders if orders else None

def fetch_confirmed_orders(user_id: str = None):
    confirm_orders = db_get_confirmed_orders(user_id)
    return confirm_orders if confirm_orders else None

# ------------------------------- MESSAGE FUNCTIONS -------------------------------
def init_user(id):
    print(f"User init: {id}")
    user_id = get_user(id)
    print(f"User id found: {user_id}")
    if user_id is None:
        print('New user')
        if admin_id is not None:
            if str(id) == admin_id:
                print('Adding admin')
                add_admin(id)
            else:
                print('Adding user')
                add_user(id)
    else:
        print('Old user')
        change_user_state(id, "MAIN_MENU")
    print('Trying to display menu')
    return display_menu(id)

def display_menu(id):
    print('Display menu', id)
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'Произвести расчет 🧑🏻‍💻', 'callback_data': 'calculator'}],
            [{'text': 'Оформить заказ ✅', 'callback_data': 'makeorder'}],
            [{'text': 'О нас ⚠️', 'callback_data': 'about'}],
            [{'text': 'FAQ 🛡', 'callback_data': 'howtoorder'}]
        ],
        'keyboard': [[{"text": k, "callback_data": v} for k, v in list(reply_keyboard_buttons.items())[i:i+2]] for i in range(0, len(reply_keyboard_buttons), 2)],
        "is_persistent": True,
        "resize_keyboard": True
    })
    mes_params = {
        "chat_id": id,
        "caption": str(mainmenu_text),
        "parse_mode": "markdown",
        "reply_markup": reply
    }
    print(f'Trying to make reuqest\n URL:{url_image} \nParams: {mes_params}')
    resp = requests.post(url_image, files={'photo': open("/tmp/main.png", 'rb')}, params=mes_params)
    print(f'start menu tg api response:{resp.content, resp.headers}')
    return resp.content


def send_ordertype_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'Кроссовки', 'callback_data': 'sneaker'}, {'text': 'Обувь', 'callback_data': 'boot'}],
            [{'text': 'Пуховик', 'callback_data': 'winterJacket'}, {'text': 'Верхняя одежда', 'callback_data': 'jacket'}],
            [{'text': 'Одежда', 'callback_data': 'cotton'}, {'text': 'Ноутбук', 'callback_data': 'laptop'}],
            [{'text': 'Смартфон', 'callback_data': 'smartphone'}, {'text': 'Аксессуар/Парфюмерия', 'callback_data': 'accessory'}],
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "👀 Выберите категорию товара:",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_orderprice_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'ℹ️ Как узнать цену своего размера?', 'callback_data': 'instruction'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "🏷️ Введите цену товара в юанях:",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def main_send_orderprice_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '❌ Отменить заказ', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "🏷️ Введите цену товара в юанях:",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_ordercost_prompt(id, price):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '↩️ Главное меню', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": f"Итоговая стоимость в рублях: `{int(price)}₽`\n Цена без учета доставки по РФ.",
    "parse_mode": "markdown",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def escape_special_chars(text):
   text = html.escape(text)
   return text

def send_text(id, text="Test"):
    mes_params = {
    "chat_id": id,
    "parse_mode": "HTML",
    "text": escape_special_chars(text)
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_captcha_prompt(id):
    try:
        captcha = EmojiCaptcha(file_name=f"captcha{id}", background="./background.png")
        generated_captcha = captcha.generate()
    except Exception as e:
        resp = str(e)

    reply = json.dumps({'inline_keyboard': [
            [{'text': str(i), 'callback_data': str(i)} for i in generated_captcha.variants]
        ]
    })
    mes_params = {
        "chat_id": id,
        "caption": "🤖 Подтвердите свою человечность!\nНажмите на эмодзи, соответствующий изображению.",
        "reply_markup": reply
    }
    resp = requests.post(url_image, files={'photo': open(f"/tmp/captcha{id}.png", 'rb')}, params=mes_params).content
    generated_captcha.remove()
    modify_userfile(id, generated_captcha.answer, "captcha_answer", "order")
    return resp

def send_ordersize_prompt(id):
    type = get_userfile(id)["order"]["type"]
    text = ""
    if item_size_type[type] == "number":
        text = "📏 Введите размер (от 16 до 63)"
    elif item_size_type[type] == "size":
        text = "📏 Введите размер (от XXXS до XXXL)"
    elif item_size_type[type] == None:
        text = "📏 Введите модель товара. Если у товара нет модели — введите слово \"Нет\""
    else:
        text = "Неверный тип товара."
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'ℹ️ Как узнать цену своего размера?', 'url': 'https://telegra.ph/Kak-oformit-zakaz-s-DEWU-Poizon-01-10#%D0%9A%D0%B0%D0%BA-%D1%83%D0%B7%D0%BD%D0%B0%D1%82%D1%8C-%D1%81%D1%82%D0%BE%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C-%D0%BD%D1%83%D0%B6%D0%BD%D0%BE%D0%B3%D0%BE-%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%80%D0%B0-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%B0'}],
            [{'text': '❌ Отменить заказ', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": text,
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_orderfio_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '❌ Отменить заказ', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "👤 Введите Ваше ФИО",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_orderadress_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'ℹ️ Подобрать пункт выдачи', 'url': 'http://www.cdek.ru/ru/offices'}],
            [{'text': '❌ Отменить заказ', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "🚚 Введите адрес доставки — пункта *«СДЕК»*",
    "parse_mode": "markdown",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_ordernumber_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '❌ Отменить заказ', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "📞 Введите номер телефона получателя",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_orderlink_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'Как скопировать ссылку на товар?', 'url': 'https://telegra.ph/Kak-oformit-zakaz-s-DEWU-Poizon-01-10#%D0%9A%D0%B0%D0%BA-%D0%BF%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%D1%82%D1%8C%D1%81%D1%8F-%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%BE%D0%B9-%D0%BD%D0%B0-%D1%82%D0%BE%D0%B2%D0%B0%D1%80'}],
            [{'text': '❌ Отменить заказ', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "Введите ссылку на товар",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_help(id: str):
    text = f"Краткая справка по командам для администрации бота:\n"
    text += f"/help: Выводит справку\n"
    text += f"/allorders [=user_id]: Выводит все неподтверждённые заказы,\n если предоставлен id профиля - все неподтверждённые заказы от этого человека.\n"
    text += f"/confirmedorders [=user_id]: Выводит все подтверждённые заказы,\n если предоставлен id профиля - все подтверждённые заказы от этого человека.\n"
    text += f"/listusers: Выводит краткую информацию о каждом профиле, зарегистрированом в боте.\n"
    text += f"/userinfo <user_id>: Выводит информацию о конкретном профиле, а также id всех его заказов\n"
    text += f"/orderinfo <order_id>: Выводит информацию о конкретном заказе.\n"
    text += f"/deleteorder <order_id>: Удаляет заказ из системы.\n"
    text += f"/setcomission <значение>: Задаёт значение фиксированной комиссии.\n"
    text += f"/setexchange <значение>: Задаёт значение рассчётного коэффиwиента.\n"
    text += f"/ban <user_id>: Банит пользователя.\n"
    text += f"/unban <user_id>: Разбанивает пользователя, также может понизить пользователя с уровня админа.\n"
    text += f"/promote <user_id>: Делает пользователя админом.\n"
    text += f"\n"
    text += f"Формулы расчёта стоимости:\n"
    text += f"Простая: ИТОГ = <цена> * <рассч. коэфф.> + <комиссия>\n"
    text += f"Сложная: ИТОГ = ((<типовой вес> / 1000) * <цена за кг.>) + (<цена> * <рассч. коэфф.>) + <комиссия>"
    text += f"Выбранная формула: {'Сложная' if use_extended_formula else 'Простая'}"
    send_text(id, text)

def generate_order_info(order: dict[str, Any]) -> str:
    text = f"Время заказа: {datetime.fromtimestamp(float(order['date']))}\n"
    text += f"*Тип заказа:* {order['data']['product_type']}\n"
    text += f"*Ссылка на товар:* {str(order['data']['product_link'])}\n"
    text += f"*Размер товара:* {order['data']['product_size']}\n"
    text += f"*Стоимость заказа (в юанях):* {order['data']['price']}¥\n"
    text += f"*ФИО клиента:* {order['data']['fio']}\n"
    text += f"*Номер телефона:* {order['data']['phone_number']}\n"
    text += f"*Пункт СДЕК:* {order['data']['ship_to']}\n"
    return text

def send_admin_prompt(id, order):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '✔️ Подтвердить', 'callback_data': f"confirm{order['_id']}"}, {'text': '❌ Отменить', 'callback_data': f"decline{order['_id']}"}],
            [{'text': '👤 Cвязь с клиентом', 'url': f"tg://user?id={order['user_id']}"}]
        ]
    })
    text = f"У Вас новая заявка!\nДетали заказа номер `{order['_id']}`:\n"
    text += generate_order_info(order)
    mes_params = {
        "chat_id": id,
        "text": text,
        "parse_mode": "markdown",
        "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    if not resp.ok:
        text += f'В связи с настройками приватности пользователя, сгенерировать ссылку на его профиль невозможно\n'
        reply = json.dumps({'inline_keyboard': [
                [{'text': '✔️ Подтвердить', 'callback_data': f"confirm{order['_id']}"}, {'text': '❌ Отменить', 'callback_data': f"decline{order['_id']}"}],
            ]
        })
        mes_params = {
        "chat_id": id,
        "text": text,
        "parse_mode": "markdown",
        "reply_markup": reply
        }
        resp = requests.post(url, params=mes_params)
    
    return resp

def send_decline_prompt(id, order):
    text = f"❌ Ваш заказ номер `{order['_id']}` был отклонен. Детали заказа:\n"
    text += generate_order_info(order)
    mes_params = {
        "chat_id": id,
        "text": text,
        "parse_mode": "markdown"
    }
    resp = requests.post(url, params=mes_params)

def send_confirm_prompt(id, order):
    text = f"✔️ Ваш заказ номер `{order['_id']}` был подтвержден.\n В ближайшее время с Вами свяжется администратор. Детали заказа:\n"
    text += generate_order_info(order)
    mes_params = {
        "chat_id": id,
        "text": text,
        "parse_mode": "markdown"
    }
    resp = requests.post(url, params=mes_params)

def send_orderconfirm_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '✔️ Оформить', 'callback_data': 'acceptorder'}, {'text': '❌ Отменить', 'callback_data': 'cancelorder'}],
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "Подтвердите оформление заказа",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def price_calc(id):
    change_user_state(id, "CALC_ORDERTYPE")
    return send_ordertype_prompt(id)

def make_order(id):
    change_user_state(id, "ORDER_CAPTCHA")
    return send_captcha_prompt(id)

def order_type(id):
    change_user_state(id, "ORDER_ORDER_TYPE")
    return send_ordertype_prompt(id)

def send_faq(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'ℹ️ Как заказать товар с Poizon', 'url': 'https://telegra.ph/Kak-oformit-zakaz-s-DEWU-Poizon-01-10'}],
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "Инструкции по работе с каждой площадкой:",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_about(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': "👉🏼 Наша группа в TG", 'url': str(tg_link)}],
        ]
    })
    mes_params = {
        "chat_id": id,
        "caption": str(about_text),
        "reply_markup": reply
    }
    resp = requests.post(url_image, files={'photo': open("/tmp/about.png", 'rb')}, params=mes_params)
    return resp.content


def send_user_info(id: str, lookup_id: str):
    user = get_user(str(lookup_id))
    if user is None:
        send_text(id, "Пользователь с таким id не найден")
    text = f"Информация о пользователе:\n"
    text += f"Id пользователя: {user['_id']}\n"
    text += f"Уровень пользователя: {user['lvl']}\n"
    text += f"Статус пользователя в системе: {user['state']}\n"
    text += f"Подтверждённые заказы:\n"
    user_orders = fetch_confirmed_orders(user['_id'])
    for order in user_orders:
        text += f"{order['_id']}\n"
    text += f"Заказы в модерации:\n"
    user_orders = fetch_orders(user['_id'])
    for order in user_orders:
        text += f"{order['_id']}\n"
    
    send_text(id, text)

def send_contact(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': "👉🏼 Наш чат", 'url': str(chat_link)}],
            [{'text': "👉🏼 Отзывы", 'url': str(review_link)}],
        ]
    })
    mes_params = {
        "caption": str(info_text),
        "reply_markup": reply
    }
    resp = requests.post(url_image+(f"?chat_id={id}"), files={'photo': open("/tmp/about.png", 'rb')}, params=mes_params)
    return resp.content

def display_order(id, order):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '👤 Cвязь с клиентом', 'url': f"tg://user?id={order['user_id']}"}]
        ]
    })
    text = generate_order_info(order)
    mes_params = {
        "chat_id": id,
        "text": text,
        "parse_mode": "markdown",
        "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    if not resp.ok:
        text += f'В связи с настройками приватности пользователя, сгенерировать ссылку на его профиль невозможно\n'
        resp = send_text(id, text) 
    return resp.content
    

def send_parameterchange_info(id, param):
    mes_params = {
        "chat_id": id,
        "text": f"⏩ Курс ¥/₽ изменён на `{param}`",
        "parse_mode": "markdown"
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_parameterkgcost_info(id, param):
    mes_params = {
        "chat_id": id,
        "text": f"⏩ Цена за кг в ₽ изменена на `{param}`",
        "parse_mode": "markdown"
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_parametercommission_info(id, param):
    mes_params = {
        "chat_id": id,
        "text": f"⏩ Стоимость коммисии изменена на `{param}`",
        "parse_mode": "markdown"
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

@app.get("/")
def read_route():
    return "CHATBOT IS UP!"

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = bytes(adminpanel_username, encoding='utf-8')
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = bytes(adminpanel_password, encoding='utf-8')
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/setwhook")
def read_current_user(link: str = None, username: str = Depends(get_current_username)):
    if link is not None:
        resp = requests.get(url=f"https://api.telegram.org/bot{token}/setWebhook?url={link}")
        return f"Hello, {username}\n{resp.content}"
    else:
        return f"Hello, {username}"

@app.post("/")
def chatbot(in_message: sendMessage):
    print(f"In_message:")
    message = in_message.message
    query = in_message.callback_query
    value = None
    if (message is not None) or (query is not None):
        if query is None:
            user_id = message["from"]["id"]
            user = get_user(user_id)
            if (user is not None):
                if (user['lvl'] == 'banned'):
                    return value
                try:
                    value = handle_message(message)
                except Exception as e:
                    value = e
            else:
                init_user(user_id)
        else:
            user_id = query["from"]["id"]
            user = get_user(query["from"]["id"])
            if (user is not None):
                if (user['lvl'] == 'banned'):
                    return value
                try:
                    value = handle_queries(query)
                except Exception as e:
                    value = e
            else:
                init_user(user_id)
    return value

def handle_message(mess):
    answer = None
    print(f'message: {mess}')
    if "entities" in mess:
        if mess["entities"][0]["type"] == "bot_command":
            answer = handle_command(mess)
        elif mess["entities"][0]["type"] == "phone_number":
            answer = handle_number(mess)
        elif mess["entities"][0]["type"] == "url":
            answer = handle_url(mess)
        else:
            answer = None
    else:
        if mess["text"] in reply_keyboard_buttons.keys():
            answer = handle_replykeyboard(mess)
        else:
            answer = handle_input(mess)
    print('Message answer')
    return answer

def handle_replykeyboard(mess):
    mess["text"] = reply_keyboard_buttons[mess["text"]]
    return handle_command(mess)

def handle_command(mess):
    chat_id = mess["from"]["id"]
    print(f'handling command: {chat_id}')
    user = get_user(chat_id)
    command_answer = None
    if mess["text"] == "/start":
        try:
            command_answer = init_user(chat_id)
        except Exception as e:
            command_answer = send_text(id, str(e))
    elif mess["text"] == "/menu":
        change_user_state(chat_id, "MAIN_MENU")
        command_answer = display_menu(chat_id)
    elif mess["text"] == "/calculator":
        command_answer = price_calc(chat_id)
    elif mess["text"] == "/order":
        command_answer = make_order(chat_id)
    elif mess["text"] == "/about":
        command_answer = send_about(chat_id)
    elif mess["text"] == "/items":
        command_answer = send_text(chat_id, str(items_text))
    elif mess["text"] == "/contact":
        command_answer = send_contact(chat_id)
    elif mess["text"] == "/faq":
        command_answer = send_faq(chat_id)

    if user is not None:
        if user["lvl"] == "admin":
            if mess["text"] == "/help":
                command_answer = send_help(chat_id)
            if mess["text"].startswith('/deleteorder'):
                mess_split = mess["text"].split()
                if len(mess_split) < 2:
                    command_answer = send_text(chat_id, "Ошибка при обработке команды")
                else:    
                    lookup_id = mess_split[1].strip()
                    delete_order(chat_id, lookup_id)
            if mess["text"].startswith('/ban'):
                mess_split = mess["text"].split()
                if len(mess_split) < 2:
                    command_answer = send_text(chat_id, "Ошибка при обработке команды")
                else:
                    lookup_id = mess_split[1].strip()
                    if lookup_id == str(chat_id):
                        command_answer = send_text(chat_id, "Ошибка, нельзя забанить самого себя")
                    else:
                        db_ban_user(lookup_id)
                        send_text(lookup_id, "Вас забанили. Если вас что-то не устраивает, напишите администрации")
                        command_answer = send_text(chat_id, f"Пользователь {lookup_id} забанен")
            if mess["text"].startswith('/unban'):
                mess_split = mess["text"].split()
                if len(mess_split) < 2:
                    command_answer = send_text(chat_id, "Ошибка при обработке команды")
                else:
                    lookup_id = mess_split[1].strip()
                    if lookup_id == str(chat_id):
                        command_answer = send_text(chat_id, "Ошибка, нельзя разбанить самого себя")
                    else:
                        db_ban_user(lookup_id)
                        send_text(lookup_id, "Вас успешно разбанили.")
                        command_answer = send_text(chat_id, f"Пользователь {lookup_id} разбанен")
            if mess["text"].startswith('/userinfo'):
                mess_split = mess["text"].split()
                if len(mess_split) < 2:
                    send_text(chat_id, "Ошибка при обработке команды")
                lookup_id = mess_split[1].strip()
                send_user_info(chat_id, lookup_id)
            if mess["text"].startswith('/promote'):
                mess_split = mess["text"].split()
                if len(mess_split) < 2:
                    command_answer = send_text(chat_id, "Ошибка при обработке команды")
                else:
                    lookup_id = mess_split[1].strip()
                    if lookup_id == chat_id:
                        command_answer = send_text(chat_id, "Ошибка, нельзя разбанить самого себя")
                    else:
                        db_promote_user(lookup_id)
                        send_text(lookup_id, "Вас успешно разбанили.")
                        command_answer = send_text(chat_id, f"Пользователь {lookup_id} забанен")
            if mess["text"].startswith('/orderinfo'):
                mess_split = mess["text"].split()
                if len(mess_split) < 2:
                    send_text(chat_id, "Ошибка при обработке команды")
                lookup_id = mess_split[1].strip()
                display_order(chat_id, lookup_id)
            if mess["text"] == "/listusers":
                ausers = fetch_all_users()
                if ausers is not None:
                    command_answer = send_text(chat_id, "⤵️ Список всех пользователей:")
                    for user in ausers:
                        send_user_info(chat_id, user['_id'])
                else:
                    command_answer = send_text(chat_id, "🙂 В системе нет пользователей")
            if mess["text"].startswith("/allorders"):
                mess_split = mess["text"].strip().split()
                if len(mess_split) == 1:
                    user_id = None
                else:
                    user_id = mess_split[1].strip()
                aorders = fetch_orders(user_id)
                if aorders is not None:
                    command_answer = send_text(chat_id, "⤵️ Список заказов в модерации:")
                    for order in aorders:
                        display_order(chat_id, order)
                else:
                    command_answer = send_text(chat_id, "🙂 Нет заказов в модерации")
            if mess["text"].startswith("/confirmedorders"):
                mess_split = mess["text"].strip().split()
                if len(mess_split) == 1:
                    user_id = None
                else:
                    user_id = mess_split[1].strip()
                corders = fetch_confirmed_orders()
                if corders is not None:
                    command_answer = send_text(chat_id, "⤵️ Список активных заказов:")
                    for order in corders:
                        display_order(chat_id, order)
                else:
                    command_answer = send_text(chat_id, "🙂 Нет активных заказов")
            elif mess["text"].startswith("/setexchange"):
                if check_regex('\/setexchange {1}(\d{1,100})+(\.\d{1,100})?$', mess["text"]):
                    mess_split = mess["text"].split(" ")
                    change = float(mess_split[1])
                    try:
                        set_price_var("change", change)
                    except Exception as e:
                        command_answer = send_text(chat_id, f"Ошибка: {str(e)}")
                    else:
                        command_answer = send_parameterchange_info(chat_id, change)
                else:
                    command_answer = send_text(chat_id, "Ошибка в вызове команды.")
            elif mess["text"].startswith("/setkgcost"):
                if check_regex('\/setkgcost {1}(\d{1,100})+(\.\d{1,100})?$', mess["text"]):
                    mess_split = mess["text"].split(" ")
                    kg_cost = float(mess_split[1])
                    try:
                        set_price_var("commission", kg_cost)
                    except Exception as e:
                        command_answer = send_text(chat_id, f"Ошибка: {str(e)}")
                    else:
                        command_answer = send_parameterkgcost_info(chat_id, kg_cost)
                else:
                    command_answer = send_text(chat_id, "Ошибка в вызове команды.")
            elif mess["text"].startswith("/setcommission"):
                if check_regex('\/setcommission {1}(\d{1,100})+(\.\d{1,100})?$', mess["text"]):
                    mess_split = mess["text"].split(" ")
                    commission = float(mess_split[1])
                    try:
                        set_price_var("commission", commission)
                    except Exception as e:
                        command_answer = send_text(chat_id, f"Ошибка: {str(e)}")
                    else:
                        command_answer = send_parametercommission_info(chat_id, commission)
                else:
                    command_answer = send_text(chat_id, "Ошибка в вызове команды.")
    print(f"probably response from telegram api: {command_answer}")
    return command_answer

def handle_number(mess):
    chat_id = mess["from"]["id"]
    resp = None
    curr_state = get_user(chat_id)["state"]
    userdata = get_userfile(chat_id)
    if curr_state == "ORDER_NUMBER":
        if(check_regex('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "number", "order")
            try:
                final_price = int(order_formula(userdata["order"]["type"], userdata["order"]["price"]))
            except Exception as e:
                resp = (send_text(chat_id, "Ошибка при расчете итоговой стоимости. Попробуйте еще раз"), send_orderprice_prompt(chat_id))
            else:
                send_text(chat_id, f"Итоговая стоимость в рублях: `{final_price}₽`\n  Цена без учета доставки по РФ.")
                resp = send_orderconfirm_prompt(chat_id)
                change_user_state(chat_id, "ORDER_CONFIRM")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз"), send_ordernumber_prompt(chat_id))
    return resp

def handle_url(mess):
    chat_id = mess["from"]["id"]
    resp = None
    curr_state = get_user(chat_id)["state"]
    userdata = get_userfile(chat_id)
    if curr_state == "ORDER_LINK":
        if (True):  # link regexes, leave them for future #if(check_regex('https:\/\/dw4\.co\/t\/A\/[a-zA-Z0-9]{8,10}$', mess["text"]) or check_regex('https:\/\/dwz\.cn\/[a-zA-Z0-9]{8,10}$', mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "link", "order")
            resp = send_ordersize_prompt(chat_id)
            change_user_state(chat_id, "ORDER_SIZE")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_orderlink_prompt(chat_id))
    return resp

def handle_input(mess):
    chat_id = mess["from"]["id"]
    resp = None
    curr_state = get_user(chat_id)["state"]
    userdata = get_userfile(chat_id)
    if curr_state == "CALC_PRICE":
        if(check_regex("([1-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9])", mess["text"])):
            modify_userfile(chat_id, int(mess["text"]), "price", "calc")
            userdata = get_userfile(chat_id)
            try:
                resp = send_ordercost_prompt(chat_id, order_formula(userdata["calc"]["type"], userdata["calc"]["price"]))
            except Exception as e:
                resp = (send_text(chat_id, "Ошибка при расчёте итоговой стоимости. Попробуйте еще раз."), send_orderprice_prompt(chat_id))
            else:
                change_user_state(chat_id, "MAIN_MENU")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_orderprice_prompt(chat_id))
    elif curr_state == "ORDER_SIZE":
        type = userdata["order"]["type"]
        regex_str = "^.{1,4095}$"
        if item_size_type[type] == "number":
            regex_str = "(1[6-9]|[2-5][0-9]|6[0-3])"
        elif item_size_type[type] == "size":
            regex_str = "(\d*(?:M|X{0,3}[SL]))(?:$|\s+.*$)"
        elif item_size_type[type] == None:
            regex_str = "^.{1,4095}$"

        if(check_regex(regex_str, mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "size", "order")
            resp = main_send_orderprice_prompt(chat_id)
            change_user_state(chat_id, "ORDER_PRICE")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_ordersize_prompt(chat_id))
    elif curr_state == "ORDER_PRICE":
        if(check_regex("([1-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9])", mess["text"])):
            modify_userfile(chat_id, int(mess["text"]), "price", "order")
            resp = send_orderfio_prompt(chat_id)
            change_user_state(chat_id, "ORDER_FIO")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), main_send_orderprice_prompt(chat_id))
    elif curr_state == "ORDER_FIO":
        if(check_regex("^.{1,4095}$", mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "fio", "order")
            resp = send_orderadress_prompt(chat_id)
            change_user_state(chat_id, "ORDER_ADRESS")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_orderfio_prompt(chat_id))
    elif curr_state == "ORDER_ADRESS":
        if(check_regex("^.{1,4095}$", mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "adress", "order")
            resp = send_ordernumber_prompt(chat_id)
            change_user_state(chat_id, "ORDER_NUMBER")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_orderadress_prompt(chat_id))
    elif curr_state == "ORDER_NUMBER":
        if(check_regex('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "number", "order")
            try:
                final_price = int(order_formula(userdata["order"]["type"], userdata["order"]["price"]))
            except Exception as e:
                resp = (send_text(chat_id, send_text(chat_id, "Ошибка при расчёте формулы. Попробуйте еще раз")), send_ordernumber_prompt(chat_id))
            else:
                send_text(chat_id, f"Итоговая стоимость c учетом доставки будет: `{final_price}₽`\n Цена не учитывает доставку сдеком от склада в России.")
                resp = send_orderconfirm_prompt(chat_id)
                change_user_state(chat_id, "ORDER_CONFIRM")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_ordernumber_prompt(chat_id))
    elif curr_state == "ORDER_LINK":
        if(check_regex('https:\/\/dw4\.co\/t\/A\/[a-zA-Z0-9]{8,10}$', mess["text"]) or check_regex('https:\/\/dwz\.cn\/[a-zA-Z0-9]{8,10}$', mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "link", "order")
            resp = send_ordersize_prompt(chat_id)
            change_user_state(chat_id,  "ORDER_SIZE")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_orderlink_prompt(chat_id))
    return resp

def handle_queries(quer):
    print('handling query')
    chat_id = quer["from"]["id"]
    resp = None
    user = get_user(chat_id)
    curr_state = user["state"]
    if quer["data"] == "mainmenu":
        resp = display_menu(chat_id)
        change_user_state(chat_id, "MAIN_MENU")
    elif quer["data"] == "calculator":
        resp = price_calc(chat_id)
    elif quer["data"] == "makeorder":
        resp = make_order(chat_id)
    elif quer["data"] == "howtoorder":
        resp = send_faq(chat_id)
    elif quer["data"] == "about":
        resp = send_about(chat_id)
    elif quer["data"] == "contact":
        resp = send_contact(chat_id)
    elif quer["data"] == "items":
        resp = send_text(chat_id, str(items_text))
    elif quer["data"].startswith("confirm"):
        if user["lvl"] == "admin":
            key = quer["data"].replace("confirm", "")
            resp = confirm_order(chat_id, key)
    elif quer["data"].startswith("decline"):
        if user["lvl"] == "admin":
            key = quer["data"].replace("decline", "")
            resp = decline_order(chat_id, key)
    elif curr_state == "CALC_ORDERTYPE":
        if quer["data"] in item_weight:
            modify_userfile(chat_id, quer["data"], "type", "calc")
            resp = send_orderprice_prompt(chat_id)
            change_user_state(chat_id, "CALC_PRICE")
    elif curr_state == "ORDER_CAPTCHA":
        if quer["data"] in emojis:
            if get_userfile(chat_id)["order"]["captcha_answer"] == quer["data"]:
                resp = order_type(chat_id)
            else:
                resp = send_text(chat_id, "😖 Неправильно! Попробуйте еще раз."), send_captcha_prompt(chat_id)
    elif curr_state == "ORDER_ORDER_TYPE":
        if quer["data"] in item_weight:
            modify_userfile(chat_id, str(quer["data"]), "type", "order")
            resp = send_orderlink_prompt(chat_id)
            change_user_state(chat_id, "ORDER_LINK")
    elif curr_state == "ORDER_CONFIRM":
        if quer["data"] == "acceptorder":
            userdata = get_userfile(chat_id)
            order = add_order(str(chat_id),str(userdata["order"]["type"]), str(userdata["order"]["link"]), str(userdata["order"]["size"]), str(userdata["order"]["price"]), str(userdata["order"]["fio"]), str(userdata["order"]["adress"]), str(userdata["order"]["number"]))
            resp = send_text(chat_id, f"😃 Спасибо за Ваш заказ!\n\n Заказ номер `{order['_id']}` зарегестрирован и передан на модерацию")
            admin_list = get_admins()
            if admin_list is not None:
                for admin in admin_list:
                    send_admin_prompt(admin['_id'], order)
            change_user_state(chat_id, "MAIN_MENU")
        elif quer["data"] == "cancelorder":
            resp = send_text(chat_id, "🟢 Заказ успешно отменен"), display_menu(chat_id)
            change_user_state(chat_id, "MAIN_MENU")
    return resp
