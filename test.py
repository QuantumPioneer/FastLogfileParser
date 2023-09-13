import pytest
from fast_gaussian_logfile_parser import fast_gaussian_logfile_parser

# Test function for fast_gaussian_logfile_parser
# TODO: fix failed tests
# TODO: 

def test_fast_gaussian_logfile_parser():

    test_fast_gaussian_logfile_parser_link()

def test_fast_gaussian_logfile_parser_link():
    """
    Test parser using a log file with gaussian LINK of three consecutive semi-empirical level jobs AM1, PM7, XTB   
    """

    file = "data/rxn_11.log"
    out = fast_gaussian_logfile_parser(file)
    
    assert out['gibbs'] == [0.453491, 0.377958, -57.116221]
    assert out['e0_zpe'] == [0.501018, 0.424827, -57.066865]
    assert out['zpe'] == [0.2756248, 0.2546919, 0.2611432]
    assert out['e0_h'] == [0.519054, 0.442973, -57.047106]
    assert out['cpu_time'] == [1729.1, 732.8, 450.9]
    assert out['wall_time'] == [133.3, 57.3, 67.0]
    assert out['number_of_atoms'] == 35
    assert out['steps'] == [18, 9, 31]

    assert out['xyz'] == False # bug: currently xyz is not matched with each level of theory, need post-processing 
    assert out['std_xyz'] == False # same bug
    assert out['std_forces'] == False # same bug

    assert out['frequencies'] == False # should expect 3 set of freqncies, 1 for each level of theory, and in each set should have 99 modes; 
    # currently this function return only 99 modes that seems to have freqnecies mixed up with all 3 level of theory
    
    # need to parse the frequency modes for analyzing reaction coordinates, following is an exmaple from AM1 negative frequency. We should parse all modes.     
    assert out['frequency_modes'] == {1: ('H', (-0.0, -0.02, -0.01)), 2: ('O', (-0.01, 0.01, -0.05)), 3: ('O', (0.01, 0.01, 0.03)), 4: ('N', (0.01, -0.01, 0.01)), 5: ('N', (0.0, 0.0, 0.0)), 6: ('N', (0.0, -0.0, 0.0)), 7: ('N', (0.0, 0.0, -0.0)), 8: ('C', (-0.02, 0.04, -0.06)), 9: ('C', (-0.0, -0.0, 0.0)), 10: ('C', (-0.0, 0.0, -0.0)), 11: ('C', (-0.0, -0.0, -0.0)), 12: ('C', (-0.0, -0.0, -0.0)), 13: ('C', (-0.0, -0.0, 0.0)), 14: ('C', (-0.0, 0.0, 0.0)), 15: ('C', (0.0, 0.0, -0.0)), 16: ('C', (0.0, 0.0, -0.0)), 17: ('C', (-0.0, 0.0, 0.0)), 18: ('C', (-0.0, 0.0, 0.0)), 19: ('C', (0.0, 0.0, 0.0)), 20: ('C', (-0.0, -0.0, -0.0)), 21: ('C', (0.0, 0.0, 0.0)), 22: ('H', (0.02, -0.64, 0.74)), 23: ('H', (-0.01, -0.05, 0.1)), 24: ('H', (-0.01, -0.05, 0.11)), 25: ('H', (-0.0, -0.0, 0.0)), 26: ('H', (0.0, 0.0, 0.0)), 27: ('H', (0.0, 0.0, 0.0)), 28: ('H', (-0.0, 0.0, -0.0)), 29: ('H', (-0.0, -0.0, -0.0)), 30: ('H', (-0.0, -0.0, 0.0)), 31: ('H', (-0.0, -0.0, 0.0)), 32: ('H', (-0.0, 0.0, 0.0)), 33: ('H', (0.0, 0.0, 0.0)), 34: ('H', (0.0, -0.0, 0.0)), 35: ('H', (0.0, 0.0, 0.0))}


