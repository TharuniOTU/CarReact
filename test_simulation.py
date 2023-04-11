"""
Pytest
Validate data to make sure simulation is working accuratley
"""

import sys
import os
cwd = os.getcwd()
from functions import *
        

# must accept the null hypothesis to prove the numbers generated are random 
def test_rand_pos_oj():
    expected_rand_list = read_file("Data/RandPos_Expected.txt") 
    actual_rand_list = read_file("Data/RandPos_Actual.txt")

    chi_square_test = chi_test(expected_rand_list, actual_rand_list, 0.05)

    assert chi_square_test == expcted_result1

# there should be a correlation between the breaking distance data online and the calculated one
def test_reaction_distance():
    expected_dist_list = read_file("Data/ReactDistance_Expected.txt")
    actual_dist_list = read_file("Data/ReactDistance_Actual.txt")
    chi_square_test = chi_test(expected_dist_list, actual_dist_list, 0.05)

    assert chi_square_test == expcted_result2