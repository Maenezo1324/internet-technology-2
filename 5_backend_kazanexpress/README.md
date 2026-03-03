# Задание 5: KazanExpress Admin Panel

Django админ-панель для управления контентом интернет-магазина с ролевой моделью.

## Запуск проекта
1. Создайте виртуальное окружение и установите зависимости: `pip install -r requirements.txt`
2. Выполните миграции: `python manage.py makemigrations store` затем `python manage.py migrate`
3. Создайте суперпользователя: `python manage.py createsuperuser`
4. Запустите сервер: `python manage.py runserver`
5. Перейдите в http://127.0.0.1:8000/admin/