from sqlalchemy.orm import Session
from app.models.permission import Permission


class PermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str) -> Permission:
        permission = Permission(name=name)
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        return permission

    def get_by_name(self, name: str):
        return self.db.query(Permission).filter_by(name=name).first()

    def get_all(self):
        return self.db.query(Permission).all()
