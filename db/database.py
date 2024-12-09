from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Определяем базовый класс для всех моделей
Base = declarative_base()

# Строка подключения к базе данных
DATABASE_URL = "postgresql://postgres_user:pw_library@localhost:5433/library_db?client_encoding=UTF8"

# Создаем объект engine
engine = create_engine(DATABASE_URL)

# Создаем таблицы в базе данных (если их нет)
Base.metadata.create_all(bind=engine)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

