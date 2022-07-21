-- upgrade --
CREATE TABLE "lesson_file" ("file_id" UUID NOT NULL REFERENCES "file" ("uuid") ON DELETE CASCADE,"lesson_id" UUID NOT NULL REFERENCES "lesson" ("uuid") ON DELETE CASCADE);
-- downgrade --
DROP TABLE IF EXISTS "lesson_file";