import csv
import warnings
import os
import pandas as pd
import numpy as np

class cell:
    """A cell (=object) within a 3dmod model"""
    def __init__(self, ID):
        self.ID = ID
        self.adhesins = []
    def add_adhesin(self, coords, ID=None):
        if ID == None:
            try:
                ID = self.adhesins[-1].ID+1
            except IndexError:
                ID = 1
        print("Coords =")
        print(coords)
        print(ID)
        new_adhesin = adhesin(coords=coords, ID=ID)
        print(new_adhesin)
        self.adhesins.append(new_adhesin)
    def list_adhesins(self):
        for i in self.adhesins:
            print(i)
    def __str__(self):
        return " ID is: " + str(self.ID)
class tomogram:
    """A tomogram with a 3dmod model"""
    def __init__(self, name, conditions = None):
        self.name = name
        self.conditions = conditions
        self.cells = []
    def add_cell(self, ID=None):
        if ID == None:
            try:
                ID = self.cells[-1].ID +1
            except IndexError:
                ID = 1
        new_cell = cell(ID)
        self.cells.append(new_cell)
    def list_cells(self):
        for i in self.cells:
            print(i)

    

class contour:
    """A 3dmod contour
    This is a class which defines a 3dmod contour with a series of x, y, z coordinates as well as tomogram and cell of origin.
    It is intended to be generated from a csv file.
    Parameters
    ----------

    ID: number, optional
    coords: a dataframe of coordinates, required
    """
    def __init__(self, coords, ID = None):
        ### Check input parameters
        self.ID = ID
        self.coords = coords
    def __str__(self):
        return str(self.coords['x'])


class adhesin(contour):
    def __init__(self, coords, ID = None):
        super().__init__(ID)
        super().__init__(coords)
        self.membrane = {}

    def add_membrane(self, coords):
        self.membrane = contour(coords)

    def __str__(self):
        return str(self.coords)

d01t01 = tomogram('d01t01')
cell1 = d01t01.add_cell(1)
d01t01.list_cells()
print(d01t01.cells[0])
adhesin1 = {
    "x": [1, 2, 3, 4],
    "y": [5, 6, 7, 8],
    "z": [0, 0, 2, 2],
}

pd.read_csv("/home/callum/adhesin/output_CdrA.csv")

#write code to sort through the different tomograms and cells, and create objects for each

#then write code to append membrane to these

#then write functions within adhesin class to automatically generate summary information

#then return everything to a dataframe through a function in tomogram class (e.g. unpack)

#then develop plotting capabilities.

d01t01.cells[0].add_adhesin(coords = pd.DataFrame(adhesin1), ID = 1)
print(d01t01.cells[0].adhesins[0])

# test = adhesin(pd.DataFrame(adhesin1),1)
# print(test)
scale = 0.852

#This function calculates the length between two points and is redundant to numpy, however, the ability to avoid numpy appears to allow the result to be directly added to the dataframe without merging
def leng(x1, y1, z1, x2, y2, z2):
    """Returns the length of a vector defined by two x y z coordinates"""
    point1 = np.array([x1,y1,z1])
    point2 = np.array([x2,y2,z2])
    return np.linalg.norm(point2 - point1)
