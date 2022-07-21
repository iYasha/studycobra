-- upgrade --
CREATE TABLE "homework_file" ("homework_id" UUID NOT NULL REFERENCES "homework" ("uuid") ON DELETE CASCADE,"file_id" UUID NOT NULL REFERENCES "file" ("uuid") ON DELETE CASCADE);
-- downgrade --
DROP TABLE IF EXISTS "homework_file";
