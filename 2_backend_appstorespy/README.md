# Задание 2: Appstorespy API (GraphQL + Celery)

Реализация бекенда для асинхронной обработки файлов через GraphQL API.

## Технологии
Python 3.10, FastAPI, Strawberry (GraphQL), PostgreSQL, Celery, Redis, Docker.

## Запуск
1. `docker-compose up --build -d`
2. GraphQL интерфейс доступен по адресу: http://localhost:8001/graphql

## Примеры запросов (выполнять в GraphiQL интерфейсе)

**1. Регистрация:**
```graphql
mutation { register(email: "test@mail.com", password: "123") }