# Задание 4: PyShop (Генерация чеков)

Сервис для генерации PDF-чеков для кухонь и клиентов ресторана на Django + RQ.

## Инструкция по запуску
1. Поднимите инфраструктуру (PostgreSQL, Redis, wkhtmltopdf):
   `docker-compose up -d`
2. Создайте виртуальное окружение и установите зависимости:
   `pip install -r requirements.txt`
3. Примените миграции БД:
   `python manage.py makemigrations checks`
   `python manage.py migrate`
4. Запустите локальный сервер Django:
   `python manage.py runserver`
5. В отдельном терминале (с активированным venv) запустите воркер:
   `python manage.py rqworker default`