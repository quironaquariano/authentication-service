from fastapi import HTTPException, status
from typing import Union, List
from app.models.user import User


class RBAC:

    def check_permission(
        self, user: User, permission_name: Union[str, List[str]]
    ):
        """Check if the user has at least one of the specified permissions.

        Args:
            user (User): The authenticated user instance.
            permission_name (Union[str, List[str]]): A single permission name or a list of permission names to check.

        Raises:
            HTTPException: If the user does not have the required permissions.

        Returns:
            bool: True if the user has the required permission(s).
        """
        if isinstance(permission_name, str):
            permission_name = {permission_name}
        else:
            permission_name = set(permission_name)

        for role in user.roles:
            user_permissions = {
                permission.name for permission in role.permissions
            }
            if permission_name.intersection(user_permissions):
                return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )


rbac = RBAC()
