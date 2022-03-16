from typing import Optional

from starlette import authentication


def get_sso_user_params(sso_user: Optional[authentication.BaseUser] = None) -> dict:
    """Данные пользователей из SSO."""
    sso_user_id = None
    sso_sid = None

    if sso_user is not None:
        sso_user_id = getattr(sso_user, "sso_user_id", None)
        sso_sid = getattr(sso_user, "sid", None)

    return {
        "sso_user_id": sso_user_id,
        "sso_sid": sso_sid,
    }
