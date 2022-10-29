# Crispy Notes
## Blogging platform powered by django

---

### Project dependencies:
* Django >3.2, <3.3
* Django Rest Framework == 3.14.0  
Check out [requirements.txt](requirements.txt) to see full list of dependencies.

---

### Local run:
* Running docker compose and building the image:
```shell
docker-compose -f <docker-compose.yml> up --build
```
* Preparing demo version data:
```shell
docker container exec -it <crispy_notes_backend> /bin/bash
```
```shell
python manage.py makemigrations && python manage.py migrate
```
```shell
python manage.py createsuperuser
```
```shell
python manage.py add_fake_posts
```
* Opening demo version:
    * http://127.0.0.1:8000 --> Web app
    * http://127.0.0.1:5000 --> Smtp4dev
    * http://127.0.0.1:8089 --> Api load test(locust)

---
