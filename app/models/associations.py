from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base import Base


role_permission_table = Table(
    "role_permssion",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column(
        "permission_id",
        Integer,
        ForeignKey("permissions.id"),
        primary_key=True,
    ),
)

user_role_table = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)
