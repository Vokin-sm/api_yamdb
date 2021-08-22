# API YaMDb
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

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
Создайте супер пользователя:
```bash
python manage.py createsuperuser
```
И запускайте сервер:
```bash
python manage.py runserver
```

## Регистрация пользователя
Отправьте POST-запрос на ссылку: ```http://127.0.0.1:8000/api/v1/auth/email/``` — не забудьте указать в параметрах вашу почту!
Пример:
```bash
curl -X POST -F "email=ваша_почта@gmail.com" http://127.0.0.1:8000/api/v1/auth/email/
```
В папке ```./sent_emails/``` появится новое "письмо", откройте его и скопируйте код для авторизации.

Теперь отправьте POST-запрос, только с кодом на ```http://127.0.0.1:8000/api/v1/auth/token/```, чтобы получить токен. Пример:
```bash
curl -X POST -F "email=ваша_почта@gmail.com" -F "confirmation_code=ваш_код" http://127.0.0.1:8000/api/v1/auth/token/
```

## Стек технологий
Python 3.7.10, Django 3, 2, 3, Django REST Framework, SQLite3, Simple JWT.

## Документация
Чтобы открыть документацию, запустите сервер и перейдите по ссылке:
```http://127.0.0.1:8000/redoc/```
