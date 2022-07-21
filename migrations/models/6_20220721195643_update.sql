-- upgrade --
CREATE TABLE IF NOT EXISTS "quiz" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "answer_type" VARCHAR(20) NOT NULL,
    "homework_id" UUID NOT NULL REFERENCES "homework" ("uuid") ON DELETE CASCADE
);
COMMENT ON TABLE "quiz" IS 'Модель теста для домашнего задания';;
CREATE TABLE IF NOT EXISTS "quiz_answers" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "text" TEXT,
    "is_correct" BOOL NOT NULL  DEFAULT False,
    "quiz_id" UUID NOT NULL REFERENCES "quiz" ("uuid") ON DELETE CASCADE
);
COMMENT ON TABLE "quiz_answers" IS 'Модель ответа на тест';;
ALTER TABLE "homework" ADD "homework_type" VARCHAR(20) NOT NULL;
CREATE TABLE "quiz_file" ("file_id" UUID NOT NULL REFERENCES "file" ("uuid") ON DELETE CASCADE,"quiz_id" UUID NOT NULL REFERENCES "quiz" ("uuid") ON DELETE CASCADE);
-- downgrade --
DROP TABLE IF EXISTS "quiz_file";
ALTER TABLE "homework" DROP COLUMN "homework_type";
DROP TABLE IF EXISTS "quiz_answers";
DROP TABLE IF EXISTS "quiz";
