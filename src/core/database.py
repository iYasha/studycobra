from core.config import settings

TORTOISE_ORM = {
    "connections": {"default": 'postgres://postgres:b2UfsCchRtrPyponeCw2kQ27eZcGDZaswFWjnH66Tr@localhost:5432/app'},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}