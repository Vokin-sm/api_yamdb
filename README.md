# API YaMDb
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

## Стек технологий
Python 3.7.10, Django 3, 2, 3, Django REST Framework, SQLite3, Simple JWT.

## Инструкция по развёртыванию
Создайте виртуальное окружение:
```bash
python -m venv venv
```
Активируйте его:
```bash
source venv/Scripts/activate
```
Установите зависимости:
```bash
pip install -r requirements.txt
```
Сделайте миграции:
```bash
python manage.py migrate
```
Создайте в корневой директории файл с названием "```.env```" и поместите в него:
```
SECRET_KEY=любой_секретный_ключ_на_ваш_выбор
DEBUG=False
ALLOWED_HOSTS=*
```
Создайте супер пользователя:
```bash
python manage.py createsuperuser
```
И запускайте сервер:
```bash
python manage.py runserver
```

## Регистрация пользователя
1. Отправьте POST-запрос с параметрами ```email``` и ```username``` на эндпоинт
```http://127.0.0.1:8000/api/v1/auth/signup/```.

2. Сервис YaMDB отправит письмо с кодом подтверждения (```confirmation_code```) 
на указанный адрес ```email```.

3. Отправьте POST-запрос с параметрами ```username``` и ```confirmation_code``` 
на эндпоинт ```http://127.0.0.1:8000/api/v1/auth/token/```, в ответе на запрос 
вам придёт token (JWT-токен).

В результате вы получаете токен и можете работать с API проекта, отправляя этот 
токен с каждым запросом.

После регистрации и получения токена вы можете отправить PATCH-запрос на эндпоинт
```http://127.0.0.1:8000/api/v1/users/me/``` и заполнить поля в своём профайле 
(описание полей — в документации).

Если пользователя создаёт администратор, например, через POST-запрос на эндпоинт 
```http://127.0.0.1:8000api/v1/users/``` — письмо с кодом отправлять не нужно 
(описание полей запроса для этого случая — в документации).

## Документация
Чтобы открыть документацию, запустите сервер и перейдите по ссылке:
```http://127.0.0.1:8000/redoc/```
