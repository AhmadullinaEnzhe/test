from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserResponse, Token, UserUpdate
from app.auth import get_current_user
from app.database import get_db
from app.services import user_service

# Роутер для эдпоинтов, связанных с пользователе
router = APIRouter()

# Эндпоинт для регистрации ногово пользователя
@router.post("/register", response_model=UserResponse, tags=["users"])
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return await user_service.register(user_data, db)

# Энпоинт для авторизации пользователя
@router.post("/login", response_model=Token, tags=["users"])
async def login(email: str, password: str, response: Response, db: Session = Depends(get_db)):
    return await user_service.login(email, password, response, db)

# Эндпоинт для выхода пользователя из системы
@router.post("/logout", tags=["users"])
async def logout(response: Response):
    return await user_service.logout(response)

# Эндпоинт для обновления профиля текущего пользователя
@router.patch("/profile", response_model=UserResponse, tags=["users"])
async def update_profile(user_update: UserUpdate,
                         current_user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    return await user_service.update_profile(user_update, current_user, db)

# Эндпоинт для деактивации аккаунта текущего пользователя
@router.delete("/account", tags=["users"])
async def delete_account(current_user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    return await user_service.delete_account(current_user, db)

