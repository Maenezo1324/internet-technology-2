import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from database import Base, SessionLocal, User, FileTask, engine
from tasks import process_file_task

Base.metadata.create_all(bind=engine)

@strawberry.type
class FileTaskType:
    id: int
    filename: str
    status: str
    lines_count: int

@strawberry.type
class Query:
    @strawberry.field
    def get_file_status(self, task_id: int) -> FileTaskType:
        db = SessionLocal()
        task = db.query(FileTask).filter(FileTask.id == task_id).first()
        db.close()
        if not task:
            return FileTaskType(id=0, filename="Not found", status="error", lines_count=0)
        return FileTaskType(
            id=task.id, filename=task.filename, 
            status=task.status, lines_count=task.lines_count
        )

@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(self, email: str, password: str) -> str:
        db = SessionLocal()
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            db.close()
            return "Пользователь уже существует"
        new_user = User(email=email, password=password)
        db.add(new_user)
        db.commit()
        db.close()
        return f"Пользователь {email} зарегистрирован"

    @strawberry.mutation
    def login(self, email: str, password: str) -> str:
        db = SessionLocal()
        user = db.query(User).filter(User.email == email, User.password == password).first()
        db.close()
        if user:
             return f"Успешный вход. Token-{email}"
        return "Неверные данные"

    @strawberry.mutation
    def upload_file(self, email: str, filename: str, content: str) -> int:
        db = SessionLocal()
        new_task = FileTask(user_email=email, filename=filename, status='pending')
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        task_id = new_task.id
        db.close()
        
        # Отправляем в Celery
        process_file_task.delay(task_id, content)
        return task_id

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")