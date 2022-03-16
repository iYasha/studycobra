from typing import List

from pydantic.main import BaseModel
from starlette.authentication import SimpleUser
from starlette.authentication import UnauthenticatedUser


class Group(BaseModel):
    slug: str


class Permission(BaseModel):
    slug: str


class SSOUserCommonData(BaseModel):
    sso_user_id: int
    sid: str
    given_name: str
    family_name: str
    email: str


class BaseSSOUser(BaseModel):
    sso_user_id: int
    sid: str
    given_name: str
    family_name: str
    email: str
    groups: List[Group]
    permissions: List[Permission]

    @property
    def group_slugs(self) -> List[str]:
        return [group.slug for group in self.groups]

    @property
    def permission_slugs(self) -> List[str]:
        return [permission.slug for permission in self.permissions]

    @property
    def common_data(self) -> dict:
        return {
            "sso_user_id": self.sso_user_id,
            "sid": self.sid,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "email": self.email,
        }

    def has_group(self, group_slug: str) -> bool:
        return group_slug in self.group_slugs

    def has_permission(self, permission_slug: str) -> bool:
        return permission_slug in self.permission_slugs

    def has_common_groups(self, groups: List[str]) -> bool:
        return bool(set(groups).intersection(self.group_slugs))

    def has_common_permissions(self, permissions: List[str]) -> bool:
        return bool(set(permissions).intersection(self.permission_slugs))


class SSOUser(BaseSSOUser, SimpleUser):
    pass


class UnauthenticatedSSOUser(BaseSSOUser, UnauthenticatedUser):
    pass


def make_sso_user(user_data: dict) -> SSOUser:
    return SSOUser(
        sso_user_id=user_data["sso_user_id"],
        sid=user_data["sid"],
        given_name=user_data["given_name"],
        family_name=user_data["family_name"],
        email=user_data["email"],
        groups=[Group(slug=group) for group in user_data["groups"]],
        permissions=[Permission(slug=permission) for permission in user_data["permissions"]],
    )
