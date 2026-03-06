import os

import pytest

from fastlogfileparser.orca import fast_orca_logfile_parser

from .data_check_test import pytest_dep_args


@pytest.mark.dependency(**pytest_dep_args)
def test_fast_orca_logfile_parser():
    """
    Test orca parser
    """

    file = os.path.join(os.path.dirname(__file__), "data", "id0.log")
    # note the comma, which returns the only element in the tuple rather than a tuple
    (result,) = fast_orca_logfile_parser(file)
    assert result.route_section == "uHF dlpno-ccsd(t) def2-svp def2-svp/c TightSCF NormalPNO"
    assert result.run_time == 134.0
    assert result.charge_and_multiplicity == [0, 2]
    assert result.input_coordinates == [
        [0.256307, -0.406648, 2.317135],
        [0.297705, -1.259805, 1.245639],
        [-0.539949, -0.850201, 0.176618],
        [-0.070086, 0.335491, -0.324511],
        [0.637437, 0.432456, 2.034247],
        [-0.108817, -2.235017, 1.544546],
        [1.320494, -1.390846, 0.838664],
        [-0.059111, -1.988448, -2.831066],
        [1.106463, -1.103968, -3.261384],
        [-1.149412, -2.304802, -3.839054],
        [-1.443956, -1.392545, -2.696128],
        [2.197775, -1.845838, -4.026316],
        [1.671389, -0.346751, -2.060649],
        [0.308973, -3.026825, -1.889798],
        [0.679763, -0.303396, -3.893535],
        [-1.569249, -3.312352, -3.827048],
        [-1.020102, -1.876509, -4.836324],
        [-1.52236, -0.318202, -2.875701],
        [-2.055032, -1.752284, -1.867669],
        [3.0032, -1.160185, -4.320795],
        [2.637017, -2.639989, -3.40478],
        [1.77572, -2.307904, -4.929811],
        [2.808952, -0.082315, -1.865814],
        [0.757108, 0.032206, -1.19073],
        [0.644543, -3.834457, -1.132202],
    ]
    assert result.t1_diagnostic == 0.017012200


@pytest.mark.dependency(**pytest_dep_args)
def test_fast_orca_logfile_parser_dlpno():
    """
    Test orca parser
    """

    file = os.path.join(os.path.dirname(__file__), "data", "0.log")
    # note the comma, which returns the only element in the tuple rather than a tuple
    (result,) = fast_orca_logfile_parser(file)
    assert result.route_section == "uHF UNO DLPNO-CCSD(T)-F12D cc-pvtz-f12 def2/J cc-pvqz/c cc-pvqz-f12-cabs RIJCOSX NormalSCF NormalPNO"
    assert result.run_time == 356.0
    assert result.charge_and_multiplicity == [0, 2]
    assert result.dipole_au == 1.03126
    assert result.input_coordinates == [
        [-1.516928, -1.007427, -0.400551],
        [-1.471551, 0.245216, 0.33273],
        [-0.445848, 1.221215, -0.248996],
        [1.000886, 1.015454, 0.168008],
        [1.565196, -0.215203, -0.326833],
        [1.360864, -1.211668, 0.472979],
        [-0.673609, -1.552438, -0.232207],
        [-2.295263, -1.5754, -0.075045],
        [-2.462807, 0.718154, 0.244641],
        [-1.27851, 0.135553, 1.421852],
        [-0.521536, 1.197385, -1.347764],
        [-0.701554, 2.245313, 0.070574],
        [1.116944, 1.003499, 1.262404],
        [1.645021, 1.795278, -0.262281],
    ]
    assert result.t1_diagnostic == 0.020468528

    file = os.path.join(os.path.dirname(__file__), "data", "new0.log")
    (result,) = fast_orca_logfile_parser(file)
    assert result.route_section == "uHF UNO DLPNO-CCSD(T)-F12D cc-pvtz-f12 def2/J cc-pvqz/c cc-pvqz-f12-cabs RIJCOSX NormalSCF NormalPNO"
    assert result.run_time == 2487.0
    assert result.charge_and_multiplicity == [0, 2]
    assert result.dipole_au == 1.2223
    assert result.input_coordinates == [
        [3.168756, 0.617416, 0.838343],
        [3.342538, -0.171879, -0.273373],
        [3.231292, 1.52192, 0.496184],
        [-0.353131, 2.159183, -0.274323],
        [-1.383522, 1.260144, 0.210082],
        [-1.906832, 0.315325, -0.774906],
        [-1.015519, -0.14966, 0.327211],
        [-2.194255, -0.839194, 1.024401],
        [-3.117528, -0.362224, -0.138892],
        [0.395569, -0.625623, 0.323837],
        [0.784995, -1.897751, -0.325493],
        [1.104734, -0.625515, -0.941397],
        [-0.830015, 3.090032, -0.614811],
        [0.256545, 1.755537, -1.104269],
        [0.324377, 2.412603, 0.555524],
        [-1.67445, 0.440579, -1.835674],
        [-2.086192, -1.932501, 1.058548],
        [-2.424313, -0.45513, 2.028426],
        [-3.508643, -1.197417, -0.736345],
        [-3.938058, 0.317744, 0.131875],
        [1.003453, -0.303868, 1.182447],
        [1.623734, -2.464501, 0.091067],
        [0.034747, -2.493109, -0.857952],
        [2.288893, -0.298935, -0.766574]
    ]
    assert result.t1_diagnostic == 0.017765837
