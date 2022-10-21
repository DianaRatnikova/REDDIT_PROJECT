<<<<<<< HEAD
# DATA REDDIT
DATA REDDIT - это скрипт? собирающий на ресурсе reddit.com наиболее популярные посты и комментарии к ним, 
=======
# REDDIT_PROJECT

REDDIT_PROJECT - это скрипт собирающий на ресурсе reddit.com наиболее популярные посты и комментарии к ним, 
>>>>>>> 33836dbb348b6e0a47d0b99718b7869a6508c010
сохраняющий данные в базу данных и csv-файлы.  
Пользователь вводит число постов и получает 2 csv-файла в директории /result_data:
```
top_subreddits.csv
comments.csv
```

Затем происходит создание и заполнение таблиц top_subreddits и comments в соответствии со схемой:
```
https://lucid.app/lucidchart/ea2ff8ec-6936-4357-ac32-3fa4c80c5b78/edit?viewport_loc=423%2C109%2C1480%2C563%2C0_0&invitationId=inv_7d9034a6-0c23-41ef-855f-70e2a6b7eab4
```

Проект разработан на Flask, используется база данных SQLAlchemy.

## Необходимое ПО и авторизации:

Установка Valentina Studio:
```
https://www.valentina-db.com/ru/
```

Аккаунт на elephantsql.com.
Необходимо создать базу данных под своим аккаунтом и открыть её в Valentine Studio
```
https://customer.elephantsql.com/instance
```

Аккаунт на reddit.com
```
reddit.com.com
```

## Сборка репозитория и локальный запуск
Выполните в консоли:
```
git clone https://github.com/DianaRatnikova/REDDIT_PROJECT.git
pip install -r requirments.txt
```
 
### Настройка
Создайте файл webapp/config_auth.py и добавьте туда следующие настройки:
```
CLIENT_ID="ИД, который Вы получили на Рэддит"
SECRET_TOKEN="Токен, привязанный к Вашему аккаунту"
user_name = ЛОГИН
password = ПАРОЛЬ

HEADERS_INFO = {'User-Agent': 'Reddit_Explore/0.0.1'}
URL_ACCESS_TOKEN = 'https://www.reddit.com/api/v1/access_token'

CONST_URL='https://oauth.reddit.com'
FOLDER_NAME = "result_data"
```


### Запуск
Скрипт запускается из корня. Выполните в консоли:
```
python get_top_subreddits.py
```
