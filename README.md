![workflow status](https://github.com/OlegPletnev/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master&event=push)
# �������� ������ "����������� ��������"
___

> �� ������������� ������� ������������ ������ ����������� �������, ������������� �� ���������� ������ �������������, ��������� ������������� ������� � ������ ����������, � ����� ������� � ������� ��������� ������� ������ ���������, ����������� ��� ������������� ������ ��� ���������� ��������� ����.
������ �� ��������� ������� - http://51.250.100.250/recipes
___
### ����������
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

### �����������������
```
email:       admin@fake.ru
password:    123
```

### ������ ���������� env-�����
```
DB_ENGINE=
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
SECRET_KEY=
```
> ��������� ��-��������� ����� ���������� � �������� �� ����� settings
### ������������������ �������� ��� ������� ������� � dev-������
- ���������� �����������:  
`git clone https://github.com/OlegPletnev/foodgram-project-react.git`
- � ����� **infra** ��������� ������� `docker-compose up` - ���������� ������ **frontend**
- ��������� ��������
`docker-compose exec backend python manage.py migrate`
- �������� �����������������
`docker-compose exec backend python manage.py createsuperuser`
- �������� �������
`docker-compose exec backend python manage.py collectstatic --no-input`
- ������������ ���� ������
`docker-compose exec backend python manage.py loaddata data/db_users.json`
`docker-compose exec backend python manage.py loaddata data/db_recipes.json`  
��� ����� ������������ ������ ���������� �����: ����������� **(db_ingredients.json)** � ���� ������� ������ ���� **(db_tags.json)**
- ������ ����� ����� �� http://localhost/admin/ � ������� ����� ������ ��� �� ��������� ������������ ��  http://localhost/api/docs/. �������� ���� �������� �� ������ http://localhost/recipes.

## ��� ������ � ��������� �������� (Ubuntu):
- ���������� docker �� ������: `sudo apt install docker.io` 
- ���������� docker-compose �� ������:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
- �������� �������������� ���� infra/nginx.conf � � ������ server_name ������� ���� IP
- ���������� ����� docker-compose.yml � nginx.conf �� ���������� infra �� ������:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
- C������� .env ����, ��������� ��� ���������� ���������� � ������� Dev-�������
- ��� ������ � Workflow �������� �� ������� � Settings/Secrets/Actions ������� ���������
    ```
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    DB_USER=<������������ ��>
    DB_PASSWORD=<������>
    DB_HOST=db
    DB_PORT=5432
    SECRET_KEY=<��������� ���� ������� django>
    
    DOCKER_PASSWORD=<������ �� DockerHub>
    DOCKER_USERNAME=<��� ������������>
    

    USER=<username ��� ����������� � �������>
    HOST=<IP �������>
    PASSPHRASE=<������ ��� �������, ���� �� ����������>
    SSH_KEY=<��� SSH ���� (��� ��������� �������: cat ~/.ssh/id_rsa)>

    TELEGRAM_TO=<ID ����, � ������� ������ ���������>
    TELEGRAM_TOKEN=<����� ������ ����>
    ```
    Workflow ������� �� ������� �����:
     - �������� ���� �� ������������ PEP8
     - ������ � ���������� ������ ������� � ��������� �� DockerHub.
     - �������������� ������ �� ��������� ������.
     - �������� ����������� � ��������-���.  
  
  
_������ ����� ��������� � ��� ����������� (nginx, PostgreSQL � Django) (��������� frontend ������������ ���� ��� ���������� ������) ����� docker-compose �� ����� �������_
- �� ������� �������� docker-compose:
`sudo docker-compose up -d --build`

- ��������, �������� �����������������, ���� ������� � �������������� ���� ���������� ���������� ���������� � ������� ��������� �� dev-������
    
### �����

������ ����

������ ������ � ������ �������� ������� �� ������������� Python-����������� ����������� (back-end) ������.���������.
