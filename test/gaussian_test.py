import os

from fastlogfileparser.gaussian import fast_gaussian_logfile_parser


def test_fast_gaussian_logfile_parser():
    """
    Test parser using a log file with gaussian LINK of three consecutive semi-empirical level jobs AM1, PM7, XTB
    """

    file = os.path.join(os.path.dirname(__file__), "data", "rxn_11.log")
    job_1, job_2, job_3 = fast_gaussian_logfile_parser(file)

    assert job_1["gibbs"] == 0.453491
    assert job_2["gibbs"] == 0.377958
    assert job_3["gibbs"] == -57.116221
    assert job_1["e0_zpe"] == 0.501018
    assert job_2["e0_zpe"] == 0.424827
    assert job_3["e0_zpe"] == -57.066865
    assert job_1["zpe"] == 0.2756248
    assert job_2["zpe"] == 0.2546919
    assert job_3["zpe"] == 0.2611432
    assert job_1["e0_h"] == 0.519054
    assert job_2["e0_h"] == 0.442973
    assert job_3["e0_h"] == -57.047106
    assert job_1['hf'] == 0.2253936
    assert job_2['hf'] == 0.1701352
    assert job_3['hf'] == -57.3280082
    assert job_1["cpu_time"] == 1729.1
    assert job_2["cpu_time"] == 732.8
    assert job_3["cpu_time"] == 450.9
    assert job_1["wall_time"] == 133.3
    assert job_2["wall_time"] == 57.3
    assert job_3["wall_time"] == 67.0
    assert job_1["number_of_atoms"] == 35
    assert job_2["number_of_atoms"] == 35
    assert job_3["number_of_atoms"] == 35
    assert job_1["number_of_optimization_steps"] == 18
    assert job_2["number_of_optimization_steps"] == 9
    assert job_3["number_of_optimization_steps"] == 31
    assert job_1["recovered_energy"] == None
    assert job_2["recovered_energy"] == None
    assert job_3["recovered_energy"][0] == -57.3069045667
    assert job_3["recovered_energy"][1] == -57.3139032763
    assert job_3["recovered_energy"][-2] == -57.328008209
    assert job_3["recovered_energy"][-1] == -57.3280082435
    assert len(job_3["recovered_energy"]) == 31
    assert job_1["frequencies"][0] == [-2302.4897, -44.9107, 19.427]
    assert job_1["frequencies"][-1] == [3202.7059, 3209.6301, 3367.7609]
    assert len(job_1["frequencies"]) == 33
    assert job_2["frequencies"][0] == [-2110.8474, -65.2439, -37.1754]
    assert job_2["frequencies"][-1] == [2770.4387, 2772.4802, 2849.8632]
    assert len(job_2["frequencies"]) == 33   
    assert job_3["frequencies"][0] == [-1070.248, 21.2558, 34.2835]
    assert job_3["frequencies"][-1] == [3144.2251, 3148.1604, 3481.313]
    assert len(job_3["frequencies"]) == 33  
    assert len(job_1['std_forces']) == 19
    assert len(job_1['std_forces'][0]) == 35
    assert job_1['std_forces'][0][0] == [1.0, 1.0, -0.012034736, 0.000231533, -0.008718935]
    assert job_1['std_forces'][0][-1] == [35.0, 1.0, 0.002160253, -0.010676581, -0.009002864]
    assert job_1['std_forces'][-1][0] == [1.0, 1.0, -8e-08, -9e-09, 1.92e-07]
    assert job_1['std_forces'][-1][-1] == [35.0, 1.0, -2.2e-08, 1.8e-08, -1e-09]
    assert len(job_2['std_forces']) == 10
    assert len(job_2['std_forces'][0]) == 35
    assert job_2['std_forces'][0][0] == [1.0, 1.0, 0.013295924, -0.000472478, 0.000883286]
    assert job_2['std_forces'][0][-1] == [35.0, 1.0, -0.000877563, 0.001225992, 0.003512116]
    assert job_2['std_forces'][-1][0] == [1.0, 1.0, 2.06e-07, -1.15e-07, -2.2e-08]
    assert job_2['std_forces'][-1][-1] == [35.0, 1.0, 6e-09, 5e-09, 2e-09]
    assert len(job_3['std_forces']) == 32
    assert len(job_3['std_forces'][0]) == 35
    assert job_3['std_forces'][0][0] == [1.0, 1.0, -0.016887644, -0.00517337, -0.008264572]
    assert job_3['std_forces'][0][-1] == [35.0, 1.0, -0.001623912, 0.006837508, 0.008029253]
    assert job_3['std_forces'][-1][0] == [1.0, 1.0, -5.19e-07, -2.07e-07, 3.29e-07]
    assert job_3['std_forces'][-1][-1] == [35.0, 1.0, 1.95e-07, -5.4e-08, 8.3e-08]

    """  decided on a different output format for the time being
    assert job_1["frequency_modes"] == {
        1: ("H", (-0.0, -0.02, -0.01)),
        2: ("O", (-0.01, 0.01, -0.05)),
        3: ("O", (0.01, 0.01, 0.03)),
        4: ("N", (0.01, -0.01, 0.01)),
        5: ("N", (0.0, 0.0, 0.0)),
        6: ("N", (0.0, -0.0, 0.0)),
        7: ("N", (0.0, 0.0, -0.0)),
        8: ("C", (-0.02, 0.04, -0.06)),
        9: ("C", (-0.0, -0.0, 0.0)),
        10: ("C", (-0.0, 0.0, -0.0)),
        11: ("C", (-0.0, -0.0, -0.0)),
        12: ("C", (-0.0, -0.0, -0.0)),
        13: ("C", (-0.0, -0.0, 0.0)),
        14: ("C", (-0.0, 0.0, 0.0)),
        15: ("C", (0.0, 0.0, -0.0)),
        16: ("C", (0.0, 0.0, -0.0)),
        17: ("C", (-0.0, 0.0, 0.0)),
        18: ("C", (-0.0, 0.0, 0.0)),
        19: ("C", (0.0, 0.0, 0.0)),
        20: ("C", (-0.0, -0.0, -0.0)),
        21: ("C", (0.0, 0.0, 0.0)),
        22: ("H", (0.02, -0.64, 0.74)),
        23: ("H", (-0.01, -0.05, 0.1)),
        24: ("H", (-0.01, -0.05, 0.11)),
        25: ("H", (-0.0, -0.0, 0.0)),
        26: ("H", (0.0, 0.0, 0.0)),
        27: ("H", (0.0, 0.0, 0.0)),
        28: ("H", (-0.0, 0.0, -0.0)),
        29: ("H", (-0.0, -0.0, -0.0)),
        30: ("H", (-0.0, -0.0, 0.0)),
        31: ("H", (-0.0, -0.0, 0.0)),
        32: ("H", (-0.0, 0.0, 0.0)),
        33: ("H", (0.0, 0.0, 0.0)),
        34: ("H", (0.0, -0.0, 0.0)),
        35: ("H", (0.0, 0.0, 0.0)),
    }
    """
