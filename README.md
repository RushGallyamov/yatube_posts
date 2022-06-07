# yatube_post

## Описание:

Прототип социальной сети-блога. Реализована система подписок.



## Установка:

1. Клонировать репозиторий:
```
git clone git@github.com:RushGallyamov/yatube_posts.git
```
2. Перейти в папку с файлом docker-compose.yaml:
```
cd foodgra-project-react/infra/
```

3. Собрать и запустить контейнеры:
```
docker-compose up -d --build
```


4. Выполнить миграции, создать суперпользователя, собрать статику:
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
```

5. Админка доступна:
```
http://localhost/admin/
```

6. Документация API на странице http://localhost/redoc/
```
http://localhost/redoc/
```

Развернутый проект можно посмотреть на странице:
http://51.250.96.39

Админка:
логин: admin
пароль: 12345678


## management-команда для загрузки ингридиентов в базу

```
docker-compose exec web python manage.py load_ingredients
```


С уважением,
Рашит Галлямов

Контакты:
rashitgalliamov@yandex.ru
https://github.com/RushGallyamov
