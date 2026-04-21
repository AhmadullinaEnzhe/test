from app.database import SessionLocal, engine
from app.models import Base, User, Role, BusinessElement, UserRole, AccessRoleRule
from app.auth import hash_password

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Создаём роли
    admin_role = Role(name="admin")
    user_role = Role(name="user")
    db.add(admin_role)
    db.add(user_role)
    db.commit()

    # Создаём бизнес‑элементы
    elements = [
        BusinessElement(name="users"),
        BusinessElement(name="access_rules"),
        BusinessElement(name="orders"),
        BusinessElement(name="products")
    ]
    for element in elements:
        db.add(element)
    db.commit()

    # Получаем ID созданных элементов
    users_element = db.query(BusinessElement).filter(BusinessElement.name == "users").first()
    access_rules_element = db.query(BusinessElement).filter(BusinessElement.name == "access_rules").first()
    orders_element = db.query(BusinessElement).filter(BusinessElement.name == "orders").first()
    products_element = db.query(BusinessElement).filter(BusinessElement.name == "products").first()

    # Правила для админа — полный доступ ко всем элементам
    admin_rules = [
        AccessRoleRule(
            role_id=admin_role.id,
            element_id=users_element.id,
            read_permission=True,
            read_all_permission=True,
            create_permission=True,
            update_permission=True,
            update_all_permission=True,
            delete_permission=True,
            delete_all_permission=True
        ),
        # Аналогично для остальных элементов...
    ]

    for rule in admin_rules:
        db.add(rule)

    # Правила для обычного пользователя
    user_rules = [
        AccessRoleRule(
            role_id=user_role.id,
            element_id=orders_element.id,
            read_permission=True,  # Может читать свои заказы
            read_all_permission=False,
            create_permission=True,
            update_permission=True,  # Может обновлять свои заказы
            update_all_permission=False,
            delete_permission=False,
            delete_all_permission=False
        )
    ]
    for rule in user_rules:
        db.add(rule)
    db.commit()

    # Создаём тестовых пользователей
    admin_user = User(
        name="Admin",
        surname="Admin",
        patronymic = "Admin",
        email="admin@example.com",
        password_hash=hash_password("admin"),
        is_active=True
    )
    regular_user = User(
        name="User",
        surname="User",
        patronymic="User",
        email="user@example.com",
        password_hash=hash_password("user"),
        is_active=True
    )
    db.add(admin_user)
    db.add(regular_user)
    db.commit()

    # Назначаем роли пользователям
    admin_ur = UserRole(user_id=admin_user.id, role_id=admin_role.id)
    user_ur = UserRole(user_id=regular_user.id, role_id=user_role.id)
    db.add(admin_ur)
    db.add(user_ur)
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
