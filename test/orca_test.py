import os

from fastlogfileparser.orca import fast_orca_logfile_parser


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
