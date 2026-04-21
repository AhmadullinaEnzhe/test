from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Загружаем переменные из .env-файла
load_dotenv()

# Получаем URL базы данных из переменных окружения
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL не найден в переменных окружения")


# Создание движка базы данных с указанием URL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Создание локальной сессии для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей базы данных
Base = declarative_base()

# Генератор для получения и управления сессией базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

