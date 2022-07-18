-- upgrade --
ALTER TABLE "session" ALTER COLUMN "access_token" TYPE TEXT USING "access_token"::TEXT;
ALTER TABLE "session" ALTER COLUMN "refresh_token" TYPE TEXT USING "refresh_token"::TEXT;
-- downgrade --
ALTER TABLE "session" ALTER COLUMN "access_token" TYPE VARCHAR(255) USING "access_token"::VARCHAR(255);
ALTER TABLE "session" ALTER COLUMN "refresh_token" TYPE VARCHAR(255) USING "refresh_token"::VARCHAR(255);
