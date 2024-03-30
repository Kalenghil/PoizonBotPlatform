# PoizonBotPlatform
Serverless Telegram-платформа с открытым исходным кодом для тех, для тех, кто занимается доставкой товаров с маркетплейсов Китая.

[![Deploy](https://button.deta.dev/1/svg)](https://deta.space/discovery/r/bf9ny8ugvvfhnx76)  

[![Buy me a coffee](https://github.com/nnagibator228/PoizonBotPlatform/blob/main/da_button.png)](https://www.donationalerts.com/r/plzdontcry)

# Быстрый запуск
## Создание Telegram-Бота
Прежде всего необходимо создать профиль бота, который будет использоваться для приема и обработки всех заявок
- Обратитесь к [BotFather](https://t.me/BotFather)
- Создайте TG-бота и сохраните его token
- Персонализируйте бота, укажите описание, установите аватар
- Создайте меню команд, указав текст ниже
    ```
    start - Инициализация бота
    menu - Открыть меню
    calculator - Рассчитать стоимость заказа
    order - Оформить заказ
    items - Товары в наличии
    about - Информация о компании
    contact - Ссылки на отзывы и чат
    faq - Инструкции по выбору товара и оформлении заказа
    ```
- Отключите возможность добавлять бота в группы
- **Готово!** Теперь можете переходить к следующему шагу

## Запуск сервиса
Теперь необходимо запустить сервис бота. Для этого нужно нажать на розовую кнопку. На открывшейся странице нажать **"Install on Space"**, авторизироваться и заполнить поля в открывшейся странице.
> ⚠️  **Учтите, неправильное заполнение полей может привести к ошибкам в работе бота или вовсе вывести его из строя!** ⚠️ 

URL, указываемые для изображений, должны напрямую вести к файлу картинки, например:
[`https://imgix.ranker.com/user_node_img/4269/85370951/original/85370951-photo-u75088731?auto=format&q=60&fit=crop&fm=pjpg&dpr=2&w=375`](https://imgix.ranker.com/user_node_img/4269/85370951/original/85370951-photo-u75088731?auto=format&q=60&fit=crop&fm=pjpg&dpr=2&w=375)
  
## Привязка вебхука
Как только сервис успешно запустится, перейдите по указанной ссылке. 
Если появилось сообщение об успешном запуске, перейдите на `<текущая ссылка сервиса>/setwhook?link=<текущая ссылка сервиса>`, например `https://rgyfqf.deta.dev/swhook?link=https://rgyfqf.deta.dev`
Авторизируйтесь с данными, заданными при запуске сервиса. Данные по умолчанию:
| Ключ | Значение |
| ------ | ------ |
| login | *admin*  |
|password | *@poizonbotthebest))1234*  |
> ⚠️ **Настоятельно рекомендуем изменить значения данных авторизации, тк стандартная пара находится в открытом доступе!** ⚠️   

При выводе сообщения о успешной привязке вебхука можно приступать к использованию бота.

# Функционал бота
К большинству функций доступ осуществляется как через команды, так и через inline-кнопки в чате. Все этапы взаимодействия с ботом снабжены фильтрацией вводимых данных.
## Команды бота
- `/start` - команда для инициализации
- `/menu` - главное меню бота

![Меню](https://github.com/nnagibator228/PoizonBotPlatform/blob/main/menu_img.png)
- `/about` - информация о компании

![Раздел Онас](https://github.com/nnagibator228/PoizonBotPlatform/blob/main/about_img.png)
- `/faq` - инструкции по работе с площадками
- `/info` - ссылки на отзывы по проекту и на чат проекта
- `/items` - посмотреть товары, доступные в наличии
- `/calculator` - рассчет стоимости товара

![Калькулятор стоимости](https://github.com/nnagibator228/PoizonBotPlatform/blob/main/calc_img.png)
- `/order` - после прохождения капчи позволяет оформить заказ, проверяя вводимую информацию

![Оформление заказа](https://github.com/nnagibator228/PoizonBotPlatform/blob/main/order_img.png)
  
## Функции администратора
- Модерация заявок

![Функции модерации #1](https://github.com/nnagibator228/PoizonBotPlatform/blob/main/mod_img.png)
![Функции модерации #2](https://github.com/nnagibator228/PoizonBotPlatform/blob/main/mod2_img.png)
- Настройка курса, комиссии, стоимости килограмма доставки

![Изменение переменных рассчета](https://github.com/nnagibator228/PoizonBotPlatform/blob/main/var_img.png)
- Просмотр заявок
`/allorders` - просмотр заявок в модерации
`/confirmedorders` - просмотр принятых заказов

![Просмотр заявок](https://github.com/nnagibator228/PoizonBotPlatform/blob/main/list_img.png)
  
# Техническая информация

## Стэк
 - Python
    - Fastapi
    - Pillow
 - Бесплатное облако deta.sh

## Лицензия
Продуктом можно пользоваться без каких-либо ограничений. Если планируется использование в коммерческих целях (продажа функционала бота etc. третьим лицам), необходимо упомянуть\указать автора.  

⭐ Если вы все-таки решите воспользовоться продуктом или поддержать автора, рекомендовано поставить звездочку проекту, создателя это точно порадует!) ⭐
