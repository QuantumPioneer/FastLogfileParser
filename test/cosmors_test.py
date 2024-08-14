import os

import pytest

from fastlogfileparser.cosmors import fast_cosmors_logfile_parser

from .data_check_test import pytest_dep_args


@pytest.mark.dependency(**pytest_dep_args)
def test_fast_cosmors_logfile_parser():
    """
    Test cosmors parser
    """

    file = os.path.join(os.path.dirname(__file__), "data", "id1.cosmo")
    # note the comma, which returns the only element in the tuple rather than a tuple
    (result,) = fast_cosmors_logfile_parser(file)
    assert result.area == 307.84
    assert result.volume == 461.21
    assert result.energy == -179.1472514653
