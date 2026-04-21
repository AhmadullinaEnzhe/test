from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate, Token
from app.auth import create_access_token, hash_password, verify_password

# Регистрация нового пользователя
async def register(user_data: UserCreate, db: Session) -> UserResponse:
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пароли не совпадают")
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )
    hashed_password = hash_password(user_data.password)

    new_user = User(name=user_data.name,
                    surname=user_data.surname,
                    patronymic=user_data.patronymic,
                    email=user_data.email,
                    password_hash=hashed_password,
                    is_active=True)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Вход пользователя в систему
async def login(email: str, password: str, response: Response, db: Session) -> Token:
    user = db.query(User).filter(User.email == email, User.is_active == True).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
        )
    
    access_token = create_access_token(data={"sub": user.email})

    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token,
            "token_type": "bearer"}

# Выход пользователя из системы
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Успешный выход из системы"}

# Обовление профиля текущего пользователя
async def update_profile(user_update: UserUpdate,
                         current_user: User,
                         db: Session) -> UserResponse:
    user = db.query(User).filter(User.email == current_user.email, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.surname is not None:
        user.surname = user_update.surname
    if user_update.patronymic is not None:
        user.patronymic = user_update.patronymic

    db.commit()
    db.refresh(user)
    return user

# Деактивация аккаунта текущего пользователя
async def delete_account(current_user: User,
                         db: Session):
    current_user.is_active = False
    db.commit()
    return {"message": "Аккаунт деативирован"}