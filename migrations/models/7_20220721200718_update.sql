-- upgrade --
ALTER TABLE "quiz_answers" ALTER COLUMN "text" SET NOT NULL;
-- downgrade --
ALTER TABLE "quiz_answers" ALTER COLUMN "text" DROP NOT NULL;
