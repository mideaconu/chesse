import os
import shutil

import pytest
from loguru import logger

from tests import data as test_data


@pytest.fixture(scope="session", autouse=True)
def tmp():
    os.mkdir(test_data.tmp_dir)
    yield
    try:
        shutil.rmtree(test_data.tmp_dir)
    except OSError as e:
        logger.error(e)
