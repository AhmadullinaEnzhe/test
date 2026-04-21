from fastapi import FastAPI
from app.routers import access_rules, users
from app.database import Base, engine

# Инициализация экзепляра приложения FastAPI
app = FastAPI(title="Бэкенд-приложение для аутентификации и авторизации")

# Создание таблиц в БД (если их еще нет)
Base.metadata.create_all(bind=engine)

# Подключение роутеров(маршрутизаторов) из отдельных
app.include_router(users.router)
app.include_router(access_rules.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
    