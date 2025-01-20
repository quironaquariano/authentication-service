from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependecies.rbac import rbac
from app.dependecies.auth import auth_dependencies
from app.models.user import User
from app.schemas.rbac import AssignPermissionForm, AssignRoleForm
from app.services.rbac_service import RBACService
from app.core.db import database


router = APIRouter()


@router.post("/create-role")
def create_role(
    name: str,
    db: Session = Depends(database.get_session),
    current_user: User = Depends(auth_dependencies.ge_current_user),
):
    rbac.check_permission(current_user, ["creator"])
    service = RBACService(db)
    return service.create_role(name)


@router.post("/create-permission")
def create_permission(
    name: str,
    db: Session = Depends(database.get_session),
    current_user: User = Depends(auth_dependencies.ge_current_user),
):
    rbac.check_permission(current_user, ["creator"])
    service = RBACService(db)
    return service.create_permission(name)


@router.post("/assign-permissions")
def assign_permissions(
    form: AssignPermissionForm,
    db: Session = Depends(database.get_session),
    current_user=Depends(auth_dependencies.ge_current_user),
):
    rbac.check_permission(current_user, ["creator", "editor"])
    service = RBACService(db)
    return service.assign_permission_to_role(
        form.role_name, form.permission_name
    )


@router.post("/assign-role")
def assign_role(
    form: AssignRoleForm,
    db: Session = Depends(database.get_session),
    current_user=Depends(auth_dependencies.ge_current_user),
):
    rbac.check_permission(current_user, ["creator", "editor"])
    service = RBACService(db)
    return service.assign_role_to_user(form.role_name, form.user_email)


@router.get("/roles")
def get_roles_list(
    db: Session = Depends(database.get_session),
    current_user=Depends(auth_dependencies.ge_current_user),
):
    rbac.check_permission(current_user, "viewer")
    service = RBACService(db)
    return service.roles_list()


@router.get("/users")
def get_users_list(
    db: Session = Depends(database.get_session),
    current_user=Depends(auth_dependencies.ge_current_user),
):
    rbac.check_permission(current_user, "viewer")
    service = RBACService(db)
    return service.users_list()


@router.get("/permissions")
def get_permissions_list(
    db: Session = Depends(database.get_session),
    current_user=Depends(auth_dependencies.ge_current_user),
):
    rbac.check_permission(current_user, "viewer")
    service = RBACService(db)
    return service.permissions_list()


# For testing
@router.get("/protected-endpoint")
def protected_endpoint(
    db: Session = Depends(database.get_session),
    current_user=Depends(auth_dependencies.ge_current_user),
):
    rbac.check_permission(current_user, "developer")
    return {"message": "Permission granted"}
