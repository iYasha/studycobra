-- upgrade --
ALTER TABLE "user" ADD "avatar_id" UUID;
ALTER TABLE "user" ADD CONSTRAINT "fk_user_file_88f4d33d" FOREIGN KEY ("avatar_id") REFERENCES "file" ("uuid") ON DELETE SET NULL;
-- downgrade --
ALTER TABLE "user" DROP CONSTRAINT "fk_user_file_88f4d33d";
ALTER TABLE "user" DROP COLUMN "avatar_id";
