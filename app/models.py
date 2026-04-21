from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Модель User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    patronymic = Column(String(30), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user_roles = relationship('UserRole', back_populates='users')

# Модель Role
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    user_roles = relationship('UserRole', back_populates='roles')
    access_role_rules = relationship('AccessRoleRule', back_populates='roles')

# Модель UserRole
class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'))

    users = relationship('User', back_populates='user_roles')
    roles = relationship('Role', back_populates='user_roles')

# Модель BusinessElement
class BusinessElement(Base):
    __tablename__ = 'business_elements'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String)

    access_role_rules = relationship('AccessRoleRule', back_populates='business_elements')

# Модель AccessRoleRule
class AccessRoleRule(Base):
    __tablename__ = 'access_roles_rules'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'))
    element_id = Column(Integer, ForeignKey('business_elements.id', ondelete='CASCADE'))
    read_permission = Column(Boolean, default=False)
    read_all_permission = Column(Boolean, default=False)
    create_permission = Column(Boolean, default=False)
    update_permission = Column(Boolean, default=False)
    update_all_permission = Column(Boolean, default=False)
    delete_permission = Column(Boolean, default=False)
    delete_all_permission = Column(Boolean, default=False)

    roles = relationship('Role', back_populates='access_role_rules')
    business_elements = relationship('BusinessElement', back_populates='access_role_rules')


