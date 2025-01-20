from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.permission import Permission
from app.models.user import User


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str) -> Role:
        role = Role(name=name)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def get_all(self):
        return self.db.query(Role).all()

    def get_by_name(self, name: str):
        return self.db.query(Role).filter_by(name=name).first()

    def assign_permission_to_role(
        self, role: Role, permission: Permission
    ) -> Role:
        role.permissions.append(permission)
        self.db.commit()
        self.db.refresh(role)
        return role

    def assign_role_to_user(self, user: User, role: Role) -> None:
        user.roles.append(role)
        self.db.commit()
        self.db.refresh(user)
        return user
