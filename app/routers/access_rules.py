from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import AccessRuleResponse, AccessRuleCreate, AccessRuleUpdate
from app.auth import require_permission
from app.database import get_db
from app.services import access_rules_service

# Роутер для эндпоинтов, связанных с правилами доступа
router = APIRouter()

# Эндпоинт для получения списка всех правил доступа
@router.get("/access_rules", response_model=list[AccessRuleResponse], tags=["access rules"])
async def get_access_rules(current_user: User = Depends(require_permission("access_rules", "read")),
                           db: Session = Depends(get_db)):
    return await access_rules_service.get_access_rules(current_user, db)

# Эндпоинт для создания нового правила доступа
@router.post("/access_rules", response_model=AccessRuleResponse, tags=["access rules"])
async def create_access_rule(rule_data: AccessRuleCreate,
                             current_user: User = Depends(require_permission("access_rules", "create")),
                             db: Session = Depends(get_db)):
    return await access_rules_service.create_access_rule(rule_data, current_user, db)

# Эндпоинт для обновления существующего правила доступа по ID
@router.patch("/access_rules/{rule_id}", response_model=AccessRuleResponse, tags=["access rules"])
async def update_access_rule(rule_id: int,
                             rule_update: AccessRuleUpdate,
                             current_user: User = Depends(require_permission("access_rules", "update")),
                             db: Session = Depends(get_db)):
    return await access_rules_service.update_access_rule(rule_id, rule_update, current_user, db)

# Эндпоинт для удаления правила доступа по ID
@router.delete("/access_rules/{rule_id}", tags=["access rules"])
async def delete_access_rule(rule_id: int,
                             current_user: User = Depends(require_permission("access_rules", "delete")),
                             db: Session = Depends(get_db)):
    return await access_rules_service.delete_access_rule(rule_id, current_user, db)


    
