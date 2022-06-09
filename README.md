# yatube_post
Стек технологий:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)

## Описание:
Прототип прототип социальной сети "Yatube" с авторизацией на Django, чтением из БД и записью в неё, генерацией индивидуальных страниц пользователей, с системой подписки и комментариев.

## Установка:

1. Клонировать репозиторий:
```
git clone git@github.com:RushGallyamov/yatube_posts.git
```
2. Перейти в папку с файлом manage.py:
```
cd yatube_posts
```
3. Создать виртуальное окружение, активировать его,установить зависимости:
```
python -m venv venv
pip install -r requirements.txt
```

4. Выполнить миграции, создать суперпользователя, собрать статику:
```
 python manage.py migrate
 backend python manage.py createsuperuser
 backend python manage.py collectstatic
```

5. Админка доступна:
```
http://localhost/admin/
```


С уважением,
Рашит Галлямов

Контакты:
rashitgalliamov@yandex.ru
https://github.com/RushGallyamov
