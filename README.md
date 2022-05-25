![workflow status](https://github.com/OlegPletnev/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master&event=push)
# Курсовой проект "Продуктовый помощник"
___

> На разработанном сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
Проект на удаленном сервере - http://51.250.100.250/recipes
___
### Технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

### Суперпользователь
```
email:       admin@fake.ru
password:    123
```

### Шаблон наполнения env-файла
```
DB_ENGINE=
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
SECRET_KEY=
```
> Настройки по-умолчанию можно посмотреть в дефолтах из файла settings
### Последовательность действий для запуска проекта в dev-режиме
- Клонируйте репозиторий:  
`git clone https://github.com/OlegPletnev/foodgram-project-react.git`
- В папке **infra** выполните команду `docker-compose up` - запустится сервис **frontend**
- Выполните миграции
`docker-compose exec backend python manage.py migrate`
- Создайте суперпользователя
`docker-compose exec backend python manage.py createsuperuser`
- Соберите статику
`docker-compose exec backend python manage.py collectstatic --no-input`
- Восстановите базу данных
`docker-compose exec backend python manage.py loaddata data/db_users.json`
`docker-compose exec backend python manage.py loaddata data/db_recipes.json`  
или можно восстановить только справочную часть: ингредиенты **(db_ingredients.json)** и теги времени приема пищи **(db_tags.json)**
- Теперь можно зайти на http://localhost/admin/ и создать новые записи или же прочитать документацию на  http://localhost/api/docs/. Основной сайт доступен по адресу http://localhost/recipes.

## Для работы с удаленным сервером (Ubuntu):
- Установите docker на сервер: `sudo apt install docker.io` 
- Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
- Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP
- Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
- Cоздайте .env файл, заполните его аналогично описанному в разделе Dev-сервера
- Для работы с Workflow добавьте на Гитхабе в Settings/Secrets/Actions секреты окружения
    ```
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=db
    DB_PORT=5432
    SECRET_KEY=<секретный ключ проекта django>
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>
    

    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

    TELEGRAM_TO=<ID чата, в который придет сообщение>
    TELEGRAM_TOKEN=<токен вашего бота>
    ```
    Workflow состоит из четырех шагов:
     - Проверка кода на соответствие PEP8
     - Сборка и публикация образа бекенда и фронтенда на DockerHub.
     - Автоматический деплой на удаленный сервер.
     - Отправка уведомления в телеграм-чат.  
  
  
_Проект нужно запустить в трёх контейнерах (nginx, PostgreSQL и Django) (контейнер frontend используется лишь для подготовки файлов) через docker-compose на вашем сервере_
- На сервере соберите docker-compose:
`sudo docker-compose up -d --build`

- Миграции, создание суперпользователя, сбор статики и восстановление базы проводится аналогично описанному в разделе установки на dev-сервер
    
### Автор

Плетнёв Олег

Проект сделан в рамках учебного процеса по специализации Python-разработчик расширенный (back-end) Яндекс.Практикум.
