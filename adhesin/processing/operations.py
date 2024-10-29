import csv
import warnings
import os
import pandas as pd
import numpy as np

scale = 0.852

#This function calculates the length between two points and is redundant to numpy, however, the ability to avoid numpy appears to allow the result to be directly added to the dataframe without merging
def leng(x1, y1, z1, x2, y2, z2):
    """Returns the length of a vector defined by two x y z coordinates"""
    point1 = np.array([x1,y1,z1])
    point2 = np.array([x2,y2,z2])
    return np.linalg.norm(point2 - point1)
