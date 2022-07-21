-- upgrade --
CREATE TABLE IF NOT EXISTS "file" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "content_type" VARCHAR(255) NOT NULL,
    "size" DOUBLE PRECISION NOT NULL
);
COMMENT ON TABLE "file" IS 'Модель хранения файлов ';;
CREATE TABLE IF NOT EXISTS "lesson" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(255),
    "description" TEXT,
    "start_at" TIMESTAMPTZ NOT NULL,
    "end_at" TIMESTAMPTZ NOT NULL,
    "group_id" UUID NOT NULL REFERENCES "group" ("uuid") ON DELETE CASCADE
);
COMMENT ON TABLE "lesson" IS 'Модель занятия';;
CREATE TABLE "lesson_group_teacher" ("groupteacher_id" UUID NOT NULL REFERENCES "group_teacher" ("uuid") ON DELETE CASCADE,"lesson_id" UUID NOT NULL REFERENCES "lesson" ("uuid") ON DELETE CASCADE);
-- downgrade --
DROP TABLE IF EXISTS "lesson_group_teacher";
DROP TABLE IF EXISTS "file";
DROP TABLE IF EXISTS "lesson";
