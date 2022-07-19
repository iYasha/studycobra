-- upgrade --
ALTER TABLE "group" ADD "creator_id" UUID NOT NULL;
ALTER TABLE "group" ADD "is_archived" BOOL NOT NULL  DEFAULT False;
CREATE TABLE IF NOT EXISTS "group_student" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "is_archived" BOOL NOT NULL  DEFAULT False,
    "group_id" UUID NOT NULL REFERENCES "group" ("uuid") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("uuid") ON DELETE CASCADE
);
COMMENT ON TABLE "group_student" IS 'Модель связи группы и ученика';;
CREATE TABLE IF NOT EXISTS "group_teacher" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "role" VARCHAR(20) NOT NULL,
    "group_id" UUID NOT NULL REFERENCES "group" ("uuid") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("uuid") ON DELETE CASCADE
);;
ALTER TABLE "group" ADD CONSTRAINT "fk_group_user_f7d0b41b" FOREIGN KEY ("creator_id") REFERENCES "user" ("uuid") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "group" DROP CONSTRAINT "fk_group_user_f7d0b41b";
DROP TABLE IF EXISTS "group_student";
ALTER TABLE "group" DROP COLUMN "creator_id";
ALTER TABLE "group" DROP COLUMN "is_archived";
DROP TABLE IF EXISTS "group_teacher";
