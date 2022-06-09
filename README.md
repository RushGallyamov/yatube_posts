# yatube_post

## Описание:


Прототип социальной сети-блога. Реализована система подписок.



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
