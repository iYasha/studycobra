from core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DB_URI},
    "apps": {
        "models": {
            "models": ["models.sessions", "models.users", "aerich.models"],
            "default_connection": "default",
        },
    },
}