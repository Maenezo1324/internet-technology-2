# Задание 1: Bewise API (Backend)

## Технологии
Python 3.10, FastAPI, PostgreSQL, SQLAlchemy, Docker, Docker-compose.

## Запуск через Docker
1. Находясь в папке `1_backend_bewise`, выполните:
   `docker-compose up --build -d`
2. API будет доступно по адресу: http://localhost:8000
3. Документация (Swagger): http://localhost:8000/docs

## Пример запроса
POST `http://localhost:8000/api/questions`
```json
{
  "questions_num": 1
}