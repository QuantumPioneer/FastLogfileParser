import os

import pytest

pytest_dep_args = dict(depends=["test/data_check_test.py::test_data_exists"], scope="session")


@pytest.mark.dependency()
def test_data_exists():
    """
    Check that the test data has been decompressed
    """

    file = os.path.join(os.path.dirname(__file__), "data", "id0.log")
    assert os.path.exists(file), "Missing data files - did you decompress the test data?"
