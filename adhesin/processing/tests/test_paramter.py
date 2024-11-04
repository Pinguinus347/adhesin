import pytest
import numpy as np
import numpy.testing as npt
import csv
import pandas as pd
import os
@pytest.mark.parametrize(
    "x1,y1,z1,x2,y2,z2, expected",
    [
        (
            0,0,0,
            2,0,0,
            2,
        ),
        (
            -1,0,-1,
            -1,0,-1,
            0,
        ),
        (
            7,4,3,
            17,6,2,
            10.246951,
        ),
    ]
)
def test_leng(x1,y1,z1,x2,y2,z2, expected):
    import processing as fun
    test_value = fun.leng(x1,y1,z1,x2,y2,z2)
    npt.assert_almost_equal(test_value, expected, decimal=5)

# def test_angle():

# def test_normal_group():

# def test_cumulative_distance():

# def test_radius_group():

# def test_midpoint():

# def test_normal():

# def test_curvature():

# def test_magnitude():

# def test_group_lengths():