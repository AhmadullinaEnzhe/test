# Веб-приложение для аутентификации и авторизации

REST API на FastAPI с системой аутентификации, авторизации и управления правами доступа.

## Технологии
* **Backend** FastAPI (Python 3.12)
* **База данных** PostgreSQL
* **ORM** SQLAlchemy 2.0+
* **Аутентификация** JWT (JSON Web Tokens)
* **Валидация данных** Pydantic 2.x
* **Хэширование паролей** bcrypt
* **Управление зависимостями** pip

## Учётные данные для входа

Для тестирования доступны следующие учётные записи:

* **Администратор:**  
  * **Логин (email):** `admin@example.com`  
  * **Пароль:** `admin`

* **Обычный пользователь:**  
  * **Логин (email):** `user@example.com`  
  * **Пароль:** `user`

**Важно:** учётные записи созданы исключительно для целей тестирования.

## Установка и запуск локально

### Предварительные требования
* Python 3.12+
* PostgreSQL (установленный и запущенный локально)
* Менеджеров пакетов 'pip'

### Пошаговая инструкция

1. **Клонирование репозиторий:**
```bash
git clone <URL-вашего репозитория>
cd <название-папки-проекта>
```

2. **Создайте и активируйте виртуальные окружения**
```bash
python -m venv venv
source venv/bin/activate # Linux/macOS
или
venv\Scripts\activate # Windows
```

3. **Установите зависимости**
```bash
pip install -r requirements.txt
```

4. **Настройте PostgreSQL**
#### Запустите сервер PostgreSQL
#### Создайте базу данных auth_system:
```bash
CREATE DATABASE auth_system;
```


Убедитесь, что у вас есть пользователь справами на эту БД (по умолчанию - postgres)

5. **Настройте переменные окружения**
#### Создайте файл .env на основе примера:
```bash
cp .env.example .env
```
#### Отредактируйте .env, указав корректные данные для подключения к вашей локальной БД:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/auth_system
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

6. **Запустите прилодение**
```bash
python main.py
```

7. **Проверьте работу**
```bash
Приложение будет доступно по адресу: http://127.0.0.1:5000

Документация API (Swagger UI): http://127.0.0.1:5000/docs

ReDoc: http://127.0.0.1:5000/redoc
```

## Структура проекта

```
.
├── app                                 # основная логика приложения
|   ├── routers/                        # роутеры (endpoints) API
|   |   ├──__init__.py                  # инициализация пакета routers
|   |   ├── access_rules.py             # роутеры для работы с правилами доступа
|   |   └── users.py                    # роутеры для работы с пользователями
|   ├── services/                       # бизнес-логика
|   |   ├──__init__.py                  # инициализация пакета services
|   |   ├── access_rules_service.py     # сервис для работы с правилами доступа
|   |   └── user_service.py             # сервис для работы с пользователями
|   ├── __init__.py                     # инициализация пакета app
|   ├── .env.example                    # пример файла .env для демонстрации структуры
|   ├── auth.py                         # логика аутентификации и авторизации
|   ├── database.py                     # настройка подключения к БД
|   ├── models.py                       # ORM-модели
|   └──schemas.py                       # Pydantic-схемы
├── .gitignore                          # файл с правилами игноривания файлов для Git
├── main.py                             # точка входа в приложение
├── README.md                           # документация по проекту
└── requirements.txt                    # список зависимостей проекта
```


## API Endpoints
#### Аутентификация
```bash
POST /register — регистрация пользователя

POST /login — вход в систему (получение JWT‑токена)

POST /logout — выход из системы
```

#### Пользователи
```bash
PATCH /profile — обновление профиля

DELETE /account — деактивация аккаунта
```

#### Управление доступом
```bash
GET /access_rules — получить все правила доступа

POST /access_rules — создать новое правило

PATCH /access_rules/{id} — обновить правило

DELETE /access_rules/{id} — удалить правило
```
