-- upgrade --
CREATE TABLE IF NOT EXISTS "homework" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(255),
    "description" TEXT,
    "time_terms" TIMESTAMPTZ NOT NULL,
    "retakes_count" INT NOT NULL,
    "difficulty_level" INT NOT NULL,
    "overdue_pass" BOOL NOT NULL  DEFAULT False,
    "author_id" UUID REFERENCES "group_teacher" ("uuid") ON DELETE SET NULL,
    "lesson_id" UUID NOT NULL REFERENCES "lesson" ("uuid") ON DELETE CASCADE
);
COMMENT ON TABLE "homework" IS 'Модель домашнего задания';
-- downgrade --
DROP TABLE IF EXISTS "homework";
