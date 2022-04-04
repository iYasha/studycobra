from core.celery_app import celery_app


@celery_app.task(name='test_celery', acks_late=True)
def test_celery(word: str) -> str:
    print(f"test task return {word}")
    return f"test task return {word}"
