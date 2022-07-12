import json
import pathlib
from os.path import join

import pytest

EXPECTED_RESULT_DIR = pathlib.Path(__file__).parent.absolute().joinpath("expected_results")


@pytest.fixture
def expected_user_create() -> dict:
    with open(join(EXPECTED_RESULT_DIR, "users/user_create.json")) as f:
        return json.load(f)


@pytest.fixture
def expected_admin_create() -> dict:
    with open(join(EXPECTED_RESULT_DIR, "users/admin_create.json")) as f:
        return json.load(f)
