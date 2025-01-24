from pydantic import BaseModel, EmailStr, ConfigDict


class PermissionResponse(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class RoleResponse(BaseModel):
    name: str
    permissions: list[PermissionResponse]

    model_config = ConfigDict(from_attributes=True)


class AssignRole(BaseModel):
    user_email: EmailStr
    role_name: str


class AssignPermission(BaseModel):
    role_name: str
    permission_name: str | list[str]
