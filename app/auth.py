from fastapi import Request, Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.models import User, UserRole
from app.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
import os

# # Загружаем переменные из .env-файла
load_dotenv()

# Получаем настройки из переменных окружения
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Значение по умолчанию
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))  # По умолчанию 30 минут

# Проверяем, что SECRET_KEY установлен
if not SECRET_KEY:
    raise ValueError("SECRET_KEY не найден в переменных окружения")

# Контекст для работы с хэшированием паролей. Использует алгоритм bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

# Хэширует пароль пользователя с помощью алгоритма bcrpt
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Проверяет, соответсвует ли пароль сохраненному хэшу
def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)

# Создает JWT-токен доступа
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Проверяет и декодирует JWT-токен
def verify_token(token: str) -> Optional[str]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception
    
# Извлекает текущего пользователя из токена, переданного в cookies
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    email = verify_token(token)
    user = db.query(User).filter(User.email == email, User.is_active == True).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден или неактивен",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

# Проверяет, имеет ли пользователь разрешение на действие надбизнес-элементом
async def check_permission(user: User, element_name: str, permission_type: str) -> bool:
    roles = [ur.roles for ur in user.user_roles]
    

    for role in roles:
        for rule in role.access_role_rules:
            if rule.business_elements.name == element_name:
                if permission_type == "read" and rule.read_permission:
                    return True
                elif permission_type == "read_all" and rule.read_all_permission:
                    return True
                elif permission_type == "create" and rule.create_permission:
                    return True
                elif permission_type == "update" and rule.update_permission:
                    return True
                elif permission_type == "update_all" and rule.update_all_permission:
                    return True
                elif permission_type == "delete" and rule.delete_permission:
                    return True
                elif permission_type == "delete_all" and rule.delete_all_permission:
                    return True
                else:
                    return False
    return False

# Проверка прав доступа
def require_permission(element_name: str, permission_type: str):
    async def dependency(user: User = Depends(get_current_user)) -> User:
        if not await check_permission(user, element_name, permission_type):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения операции"
            )
        return user
    return dependency



