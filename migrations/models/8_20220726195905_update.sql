-- upgrade --
CREATE TABLE IF NOT EXISTS "homeworkanswer" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "answer" TEXT,
    "teacher_description" TEXT,
    "points" INT,
    "file_id" UUID REFERENCES "file" ("uuid") ON DELETE SET NULL,
    "homework_id" UUID NOT NULL REFERENCES "homework" ("uuid") ON DELETE CASCADE,
    "student_id" UUID NOT NULL REFERENCES "user" ("uuid") ON DELETE CASCADE,
    "teacher_file_id" UUID REFERENCES "file" ("uuid") ON DELETE SET NULL
);
COMMENT ON TABLE "homeworkanswer" IS 'Модель решения домашнего задания';
-- downgrade --
DROP TABLE IF EXISTS "homeworkanswer";
