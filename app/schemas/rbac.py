from pydantic import BaseModel, EmailStr, ConfigDict


class PermissionResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class RoleResponse(BaseModel):
    id: int
    name: str
    permissions: list[PermissionResponse]

    model_config = ConfigDict(from_attributes=True)


class AssignRoleForm(BaseModel):
    user_email: EmailStr
    role_name: str


class AssignPermissionForm(BaseModel):
    role_name: str
    permission_name: str | list[str]
