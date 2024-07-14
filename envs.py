import os


def proceed_bool_env(env):
    if env.lower() in ['true', '1']: return True
    elif env.lower() in ['false', '0']: return False
    else: return None

envs = os.environ
def proceed_env(env_name: str, default_value=''):
    if env_name not in envs:
        return default_value
    return envs[env_name]

redis_password = proceed_env('REDIS_PASSWORD', 'mysecretpassword')

mongo_uri = proceed_env('MONGODB_URI')
mongo_db = proceed_env('MONGO_INITDB_DATABASE')
mongo_username = proceed_env('MONGODB_USER')
mongo_password = proceed_env('MONGODB_PASSWORD')


minio_access_key = proceed_env('MINIO_ACCESS_KEY', 'minioadmin')
minio_secret_key = proceed_env('MINIO_SECRET_KEY', 'minioadmin')

mysql_root_password = proceed_env('MYSQL_ROOT_PASSWORD', 'rootpassw')
mysql_database_name = proceed_env('MYSQL_DATABASE', 'monvisium_db')

token = envs['TOKEN'] if 'TOKEN' in envs else None
about_text = envs['ABOUT'] if 'ABOUT' in envs else "О нас ⚠️"
info_text = envs['INFO'] if 'INFO' in envs else "Чат и отзывы 💬"
items_text = envs['ITEMS'] if 'ITEMS' in envs else "items are here - https://google.com"
mainmenu_text = envs['MAINMENU'] if 'MAINMENU' in envs else "Проект poizonbot"
adminpanel_username = envs['USERNAME'] if 'USERNAME' in envs else "admin"
adminpanel_password = envs['PASSWORD'] if 'PASSWORD' in envs else "@poizonbotthebest))1234"
mainimage_url = envs['MAINIMG'] if 'MAINIMG' in envs else None
aboutimage_url = envs['ABOUTIMG'] if 'ABOUTIMG' in envs else None
tg_link = envs['TGLINK'] if 'TGLINK' in envs else "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # установить ссылку на репозиторий бота
review_link = envs['REVIEWLINK'] if 'REVIEWLINK' in envs else "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
chat_link = envs['CHATLINK'] if 'CHATLINK' in envs else "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
admin_id = envs['ADMINID'] if 'ADMINID' in envs else None
use_extended_formula = proceed_bool_env(envs['EXTFORMULA']) if 'EXTFORMULA' in envs and proceed_bool_env(envs['EXTFORMULA']) is not None else True