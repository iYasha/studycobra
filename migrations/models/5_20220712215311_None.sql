-- upgrade --
CREATE TABLE IF NOT EXISTS "user" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(40),
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255)
);
COMMENT ON TABLE "user" IS 'Базовая модель пользователя ';
CREATE TABLE IF NOT EXISTS "session" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "ip_address" VARCHAR(20),
    "user_agent" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "access_token" VARCHAR(255),
    "refresh_token" VARCHAR(255),
    "platform" VARCHAR(20) NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "user" ("uuid") ON DELETE CASCADE
);
COMMENT ON TABLE "session" IS 'Модель сессии пользователя ';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
