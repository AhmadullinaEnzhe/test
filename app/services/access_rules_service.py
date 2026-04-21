from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import User, AccessRoleRule, Role, BusinessElement
from app.schemas import AccessRuleResponse, AccessRuleCreate, AccessRuleUpdate


# Получение списка всех правил из базы данных
async def get_access_rules(current_user: User,
                           db: Session) -> list[AccessRuleResponse]:
    rules = db.query(AccessRoleRule).all()
    return rules

# Создание нового правила доступа
async def create_access_rule(rule_data: AccessRuleCreate,
                             current_user: User,
                             db: Session) -> AccessRuleResponse:
    role = db.query(Role).filter(Role.id == rule_data.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Роль не найдена"
        )
    
    element = db.query(BusinessElement).filter(BusinessElement.id == rule_data.element_id).first()
    if not element:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бизнес-элемент не найден"
        )
    
    new_rule = AccessRoleRule(role_id=rule_data.role_id,
                               element_id=rule_data.element_id,
                               read_permission=rule_data.read_permission,
                               read_all_permission=rule_data.read_all_permission,
                               create_permission=rule_data.create_permission,
                               update_permission=rule_data.update_permission,
                               update_all_permission=rule_data.update_all_permission,
                               delete_permission=rule_data.delete_permission,
                               delete_all_permission=rule_data.delete_all_permission)
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule

# Обновление существующего правила доступа по ID
async def update_access_rule(rule_id: int,
                             rule_update: AccessRuleUpdate,
                             current_user: User,
                             db: Session) -> AccessRuleResponse:
    rule = db.query(AccessRoleRule).filter(AccessRoleRule.id == rule_id).first()

    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Правило доступа не найдено"
        )
    
    if rule_update.role_id is not None:
        rule.role_id = rule_update.role_id
    if rule_update.element_id is not None:
        rule.element_id = rule_update.element_id
    if rule_update.read_permission is not None:
        rule.read_permission = rule_update.read_permission
    if rule_update.read_all_permission is not None:
        rule.read_all_permission = rule_update.read_all_permission
    if rule_update.create_permission is not None:
        rule.create_permission = rule_update.create_permission
    if rule_update.update_permission is not None:
        rule.update_permission = rule_update.update_permission
    if rule_update.update_all_permission is not None:
        rule.update_all_permission = rule_update.update_all_permission
    if rule_update.delete_permission is not None:
        rule.delete_permission = rule_update.delete_permission
    if rule_update.delete_all_permission is not None:
        rule.delete_all_permission = rule_update.delete_all_permission

    db.commit()
    db.refresh(rule)
    return rule

# Удаление правила доступа по ID
async def delete_access_rule(rule_id: int,
                             current_user: User,
                             db: Session):
    rule = db.query(AccessRoleRule).filter(AccessRoleRule.id == rule_id).first()

    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Правило доступа не найдено"
        )
    
    db.delete(rule)
    db.commit()
    return {"message:": "Правило доступа удалено"}


    
