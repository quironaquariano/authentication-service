from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.models.role import Role


class RBACService:
    def __init__(self, db: Session):
        self.role_repo = RoleRepository(db)
        self.permission_repo = PermissionRepository(db)
        self.user_repo = UserRepository(db)

    def create_role(self, name):
        if self.role_repo.get_by_name(name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role already exists",
            )
        return self.role_repo.create(name)

    def create_permission(self, name: str):
        if self.permission_repo.get_by_name(name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission already exists",
            )
        return self.permission_repo.create(name)

    def assign_permission_to_role(
        self, role_name: str, permissions: list[str]
    ):
        role = self.role_repo.get_by_name(role_name)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found",
            )
        permissions = (
            [permissions] if isinstance(permissions, str) else permissions
        )
        for permission_name in permissions:
            permission = self.permission_repo.get_by_name(permission_name)
            if not permission:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Permision not found",
                )

            if permission in role.permissions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Permission {permission} already assigned to role {role}",
                )

            self.role_repo.assign_permission_to_role(role, permission)

        return {
            "message": "Permissions assigned successfully",
            "result": {
                "role": role_name,
                "permissions": permission_name,
            },
        }

    def assign_role_to_user(self, role_name: str, user_email: str):
        role = self.role_repo.get_by_name(role_name)
        user = self.user_repo.get_by_email(user_email)

        if not role or not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role or User not found",
            )
        if role in user.roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role already assigned",
            )
        self.role_repo.assign_role_to_user(user, role)
        return {
            "message": "Role assigned successfully",
            "result": {"user": user.email, "role": role_name},
        }

    def roles_list(self):
        return self.role_repo.get_all()

    def permissions_list(self):
        return self.permission_repo.get_all()

    def users_list(self):
        return self.user_repo.get_all()

    def get_role_by_name(self, name: str) -> Role:
        return self.role_repo.get_by_name(name)
