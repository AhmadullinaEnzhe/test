from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Модель для создания нового пользователя
class UserCreate(BaseModel):
    model_config = {"from_attributes": True}

    name: str
    surname: str
    patronymic: str
    email: EmailStr
    password: str
    confirm_password: str

# Модель для обновления данных пользователя
class UserUpdate(BaseModel):
    model_config = {"from_attributes": True}

    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None

# Модель ответа с данными пользователя
class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    surname: str
    patronymic: str
    email: str
    is_active: bool

# Модель ответа при успешной авторизации
class Token(BaseModel):
    model_config = {"from_attributes": True}

    access_token: str
    token_type: str

# Модель для создания правила доступа
class AccessRuleCreate(BaseModel):
    model_config = {"from_attributes": True}

    role_id: int
    element_id: int
    read_permission: bool = False
    read_all_permission: bool = False
    create_permission: bool = False
    update_permission: bool = False
    update_all_permission: bool = False
    delete_permission: bool = False
    delete_all_permission: bool = False

# Модель ответа с информацией о правиле доступа
class AccessRuleResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    role_id: int
    element_id: int
    read_permission: bool
    read_all_permission: bool
    create_permission: bool
    update_permission: bool
    update_all_permission: bool
    delete_permission: bool
    delete_all_permission: bool

# Модель для частичного обновления правила доступа
class AccessRuleUpdate(BaseModel):
    model_config = {"from_attributes": True}

    role_id: Optional[int] = None
    element_id: Optional[int] = None
    read_permission: Optional[bool] = None
    read_all_permission: Optional[bool] = None
    create_permission: Optional[bool] = None
    update_permission: Optional[bool] = None
    update_all_permission: Optional[bool] = None
    delete_permission: Optional[bool] = None
    delete_all_permission: Optional[bool] = None


