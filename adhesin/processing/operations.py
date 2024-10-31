import csv
import warnings
import os
import pandas as pd
import numpy as np
scale = 0.852

def leng(x1, y1, z1, x2, y2, z2):
    """Returns the length of a vector defined by two x y z coordinates"""
    point1 = np.array([x1,y1,z1])
    point2 = np.array([x2,y2,z2])
    return np.linalg.norm(point2 - point1)
def angle(vector1, vector2):
    """"Calculates the angle between two coordinates in the same row"""
    result1 = np.arccos(np.dot(vector1,vector2)/(np.linalg.norm(vector1)*np.linalg.norm(vector2)))
    #The result is converted from radians to degrees
    result2 = np.degrees(result1)
    #controlling for if one or both vectors are pointing in the 'wrong' direction
    if result2 > 90:
        result2 = np.abs(result2-180)
    return pd.Series(result2)
def normal_group(group):
    """This considers the 1st, 4th and 8th point in the membrane object and returns the vector normal of the plane formed"""
    a = [5, 4, 4, 4, 4, 3, 3, 3]
    b = [2, 0, 0, 2, 2, 0, 0, 1]
    c = [7, 7, 8, 6, 7, 7, 8, 8]
    d = [0, 1, 2, 3, 4, 5, 6, 7]
    
    #a = [5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3]
    #b = [0, 0, 1, 2, 2, 0, 0, 0, 1, 1, 2, 2, 2, 0, 0, 0, 1, 1]
    #c = [7, 8, 7, 7, 8, 6, 7, 8, 6, 8, 6, 7, 8, 6, 7, 8, 7, 8]
    #d = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    
    n = 0

    for i in d:
        n += 1
        #Points are selected using panda .iloc to select the row and columns in each position, then converting these values to a list
        first_coord = np.array(group.iloc[b[i],0:3].values.tolist())
        second_coord = np.array(group.iloc[a[i],0:3].values.tolist())
        third_coord = np.array(group.iloc[c[i],0:3].values.tolist())
        #NB as this uses dataframe coordinates, if the format of the dataframe is altered the funciton must be adjusted
        vector1 = first_coord - second_coord
        vector2 = first_coord - third_coord
        product = np.cross(vector1,vector2)
        unit_product = product/np.linalg.norm(product)
        if i == 0:
            test_vector = unit_product
            #print(test_vector)
            result = test_vector
        else:
            #print(np.dot(unit_product,test_vector))
            trial = np.dot(unit_product,test_vector)
            if trial < 0:
                unit_product = unit_product*-1
            #print(unit_product)
            result = result + unit_product
    
    mean_normal = result/n
    print(f'mean normal = {mean_normal}')
    #The resultant normal is reshaped and returned as a dataframe for ease of merging
    # result1 = mean_normal.reshape(1,-1)
    # result2 = pd.DataFrame(result1, columns=['x1','y1','z1'])
    return mean_normal
def cumulative_distance(group):
    """Returns the cumulative distance for each point in a CdrA molecule using the precalculated distance between points"""
    
    #Checks the group is long enough to sum distances
    if len(group) >= 2:
        #The first point is the base and thus the total distance is not applicable
        result = [np.nan]

        #The code then iterates through each set of distances in the group
        for i in range(1, len(group)):

            #The group needing to be summed is first specified as a list using Pandas iloc
            #The final position in the group is actually the length of the group +1 (perhaps due to the NaN value?)
            group_to_sum = group['Distance'].iloc[1:i+1]

            #This produces a series, which must be converted to a list for summing
            list_to_sum = group_to_sum.tolist()

            #print(list_to_sum)
            
            #The sum is calculated
            cumulative_total = sum(list_to_sum)
            
            #print(f"[cumulative_total{cumulative_total}")
            
            #The result is appended to the result list
            result.append(cumulative_total)

    #Failsafe if group is too short, should not happen if CdrA is specified correctly
    else:
        result = [np.nan] * (len(group) - 2)
    
    #The result is transposed into a single column dataframe, then returned
    #result_df = pd.DataFrame(result, columns=['Cumulative_distance'])
    #print(result_df)
    return result
def radius_group(group):
    """Acts on group containing 3 or more points and returns curvature for every 3 points at the position of the third point"""
    #Empty result list created for each application
    result = []

    #If statement checks group is long enough to check curvature
    if len(group) >= 3:
        #The result list is redefined so that the first two values are NA, as curvature cannot be calculated with less than 3 points
        result = [np.nan,np.nan]

        #The columns in the range 2 to the length of the group are then considered witha for loop
        #This range also prevents indices outside the range of the group being taken
        for i in range(2, len(group)):
            #The variables for input into the function curvature are defined based on the column name
            x1 = group['x'].iloc[i - 2]
            y1 = group['y'].iloc[i - 2]
            z1 = group['z'].iloc[i - 2]
            x2 = group['x'].iloc[i - 1]
            y2 = group['y'].iloc[i - 1]
            z2 = group['z'].iloc[i - 1]
            x3 = group['x'].iloc[i]
            y3 = group['y'].iloc[i]
            z3 = group['z'].iloc[i]

            #The radius of curvature is calculated with the above defined function
            radius = curvature(x1, y1, z1, x2, y2, z2, x3, y3, z3)
            #The curvature function includes the scale factor in its definition, so the result is in nm already

            #For each set of 3 points in the group (overlapping permitted), the result is appended to the list
            result.append(radius)
    
    #This else statement accounts for the case where the group is too small to define curvature - this should not happen with proper data collection and processing
    else:
        result = [np.nan] * (len(group) - 2)
    
    #The result list is transformed into a single column dataframe titled Radius, which is the output of the function
    #result_df = pd.DataFrame(result, columns=['Radius'])
    return result
def midpoint(x1, y1, z1, x2, y2, z2):
    """Returns midpoint of two points as a np.array"""
    vector1 = np.array([x1,y1,z1])
    vector2 = np.array([x2,y2,z2])
    mid = (vector1+vector2)/2
    return mid
def normal(x1, y1, z1, x2, y2, z2,x3,y3,z3):
    """Returns the normal of a plane defined by three points"""
    vector1 = np.array([x1,y1,z1])-np.array([x2,y2,z2])
    vector2 = np.array([x1,y1,z1])-np.array([x3,y3,z3])
    return np.cross(vector1,vector2)
def curvature(x1,y1,z1,x2,y2,z2,x3,y3,z3):
    """Returns the radius of curvature of three points using perpedincular bisectors"""    
    #Each point is defined as an array for vector maths
    pointA = np.array([x1,y1,z1])
    pointB = np.array([x2,y2,z2])
    pointC = np.array([x3,y3,z3])

    #First the the vectors formed between the points are considered, and their midpoints
    vectorAB = pointB-pointA
    midpointAB = midpoint(x1, y1, z1, x2, y2, z2)

    vectorBC = pointC -pointB
    midpointBC = midpoint(x2, y2, z2, x3, y3, z3)
    #This is calculated so the perpedincular bisectors can be computed

    #The plane normal of the 3 points is calculated with the cross product of the two vectors
    plane_normal = np.cross(vectorAB,vectorBC)
    
    #This if statement accounts for the unlikely event that the 3 points are colinear (though this may break the code later on)
    if np.linalg.norm(plane_normal) == 0:
        print("It's straight")
        return np.inf
    else:
        #These cross products give the directions of the perpendicular bisectors
        direction_1 = np.cross(vectorAB,plane_normal)
        direction_2 = np.cross(vectorBC,plane_normal)
        #This vector points out of the plane, and should be the same direction as the plane normal  (it is likely redudntant here, but this maths is to calculate the minimum distance between two lines not assuming they cross)
        n = np.cross(direction_1,direction_2)
        

        #This gives the vector between the two midpoints
        direction_3 = midpointBC-midpointAB

        #The next line gives the distance between the two closest points, which should always be zero
        #d = (np.dot(n,(midpointAB-midpointBC)))/np.linalg.norm(n)
        #print(f"d={d}")

        #The next two lines solve the paramters in the vector equation description of the perpendicular bisectors, for which they are closest together
        t1 = (np.dot(np.cross(direction_2,n),direction_3))/np.dot(n,n)
        #print(f't1 = {t1}')
        t2 = (np.dot(np.cross(direction_1,n),direction_3))/np.dot(n,n)
        #print(f't2 = {t2}')

        #Using the parameter in the vector equation, the coordinate of the intersect of the bisectors, ie the centre of the circle including the 3 points of interest, is obtained
        intersect1 = midpointAB + t1*direction_1

        #This can be additionally verified considering the other perpendicular bisector
        #intersect2 = midpointBC + t2*direction_2

        #The radius of curvature is defined here as the radius of the circle containing the 3 points, calculated by the maginuted of the vector between the centre of the circle and the first point
        radius = np.linalg.norm(pointA-intersect1)

        #This scale factor is used to convert the radius into nm
        scale = 0.852
        return radius*scale
def magnitude(x1, y1, z1):
    """This calculates the magnitude of a vector x1, y1, z1, but is redundant given numpy"""
    return np.sqrt((x1)**2+(y1)**2+(z1)**2)
def group_lengths(group):
    """Applies the length function to a dataframe of coordinates"""
    lengths = []
    global scale
    print(len(group))
    for i in range(0,len(group)):
        if i == 0:
            length = 0
        else:
            x1, y1, z1 = group[["x","y","z"]].iloc[i - 1]
            x2, y2, z2 = group[["x","y","z"]].iloc[i]
            length = leng(x1, y1, z1, x2, y2, z2)
        lengths.append(length*scale)
    return pd.Series(lengths)
class cell:
    """A cell (=object) within a 3dmod model"""
    def __init__(self, ID):
        self.ID = ID
        self.adhesins = []
    def add_adhesin(self, coords, adhesin_type, ID=None):
        if ID == None:
            try:
                ID = self.adhesins[-1].ID+1
            except IndexError:
                ID = 1
        #print("Coords =")
        #print(coords)
        #print(ID)
        new_adhesin = adhesin(coords=coords, adhesin_type=adhesin_type, ID=ID)
        #print(new_adhesin.ID)
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
        self.cells.insert((ID - 1), new_cell)
    def list_cells(self):
        cell_list = []
        for i in self.cells:
            cell_list.append(i.ID)
        return(cell_list)
    def csv_make(self):
        self.path = "/home/callum/adhesin/" + self.name + ".csv"
        for cell in self.cells:
            for adhesin in cell.adhesins:
                df = adhesin.coords
                df[adhesin.adhesin_type] = adhesin.ID
                #print(adhesin.ID)
                df['Cell'] = cell.ID
                df['Tomogram'] = self.name
                if cell.ID == 1 and adhesin.ID == 1:
                    #print("on the right track")
                    df.to_csv(self.path, index = False)
                else:
                    df2 = pd.read_csv(self.path)
                    df =  pd.concat([df2,df],axis=0)
                    df.to_csv(self.path, index = False)
    def csv_view(self):
        print(self.path)
        return pd.read_csv(self.path)
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
    def __init__(self, coords, adhesin_type, ID = None):
        super().__init__(coords, ID)
        self.adhesin_type = adhesin_type
        self.membrane = None
        self.resampled = None

    def add_membrane(self, coords, warning_limit = 5):
        self.membrane = contour(coords)
        x1, y1, z1 = self.membrane.coords.iloc[1]
        x2, y2, z2 = self.coords.iloc[0]
        #print(type(membrane_origin)) 
        print(x1, y1, z1)
        displacement=leng(x1,y1,z1,x2,y2,z2)
        global scale
        if displacement*scale > warning_limit:
            warnings.warn("There is a large separation between the membrane and adhesin in molecule ID "+str(self.ID), UserWarning)
        #print(np.array(membrane_origin))       

    def add_resampled(self, coords, warning_limit = 0.1):
        self.resampled = contour(coords)
        x1, y1, z1 = self.resampled.coords.iloc[0]
        x2, y2, z2 = self.coords.iloc[0]
        #print(type(membrane_origin)) 
        print(x1, y1, z1)
        displacement=leng(x1,y1,z1,x2,y2,z2)
        global scale
        if displacement*scale > warning_limit:
            warnings.warn("There is a large separation between the membrane and adhesin in molecule ID "+str(self.ID), UserWarning)

    def calculate_paramters(self):
        global scale
        self.lengths = group_lengths(self.coords)
        self.length = self.lengths.sum()
        self.EtE = np.array(self.coords.iloc[1])-np.array(self.coords.iloc[0])
        self.initial_vector = np.array(self.coords.iloc[1])-np.array(self.coords.iloc[0])
        if self.membrane is not None:
            normal = normal_group(self.membrane.coords)
            self.angle = angle(self.initial_vector,normal)
            self.extension = scale*abs((np.dot(self.EtE,normal))/np.linalg.norm(normal))
        if self.resampled is not None:
            self.resampled.coords['Distance'] = self.resampled.coords.apply(group_lengths)
            if (self.resampled.coords['Distance'] < 2.0).any():
                raise ValueError("A value in the 'Distance' column is less than 2.0.")
            self.resampled.coords['Cumulative_distance'] = self.resampled.coords.apply(cumulative_distance)
            self.resampled.coords['Radius'] = self.resampled.coords.apply(radius_group)
            if (1/self.resampled.coords['Raidus'] > 0.4).any():
                raise ValueError("A value in the 'Radius' column has reciprocol greater than 0.4")
            self.mean_curvature = self.resampled.coords['Radius'].mean()
    def normalise(self):
        """Function to rotate all points to the membrane normal"""
        return None
    def __str__(self):
        return str(self.coords)

def classify(group):
    tomo_name = group['Tomogram'].iloc[0]
    cell_no = group['Cell'].iloc[0]
    global adhesin_type
    molecule_ID = group[adhesin_type].iloc[0]
    #print(tomo_name, cell_no, molecule_ID)
    coordinates = group[['x','y','z']]
    #print(coordinates)
    
    
    # Check if 'tomo_name' already exists in a collection or the `tomogram` class
    if not hasattr(tomogram, 'instances'):
        tomogram.instances = {}
        #print("Initialising dict")
    # Check if 'tomo_name' is already an instance in `tomogram.instances`
    if tomo_name not in tomogram.instances:
        tomogram.instances[tomo_name] = tomogram(tomo_name)
        #print("tomogram is appended as a class in the list")
        #print(type(tomo_name))
    tomo = tomogram.instances[tomo_name]

    cell_list = tomo.list_cells()
    #print(cell_list)
    if not cell_no in cell_list:
        tomo.add_cell(cell_no)
    tomo.cells[cell_no - 1].add_adhesin(coords = coordinates, adhesin_type=adhesin_type, ID = molecule_ID)

def add_membranes(group):
    tomo_name = group['Tomogram'].iloc[0]
    cell_no = group['Cell'].iloc[0]
    molecule_ID = group['membrane'].iloc[0]
    #print(tomo_name, cell_no, molecule_ID)
    coordinates = group[['x','y','z']]
    if tomo_name not in tomogram.instances:
        raise IndexError("The intended target tomogram does not exist in the dataframe")
    tomo = tomogram.instances[tomo_name]
    cell_list = tomo.list_cells()
    if cell_no not in cell_list:
        raise IndexError("The intended target cell does not exist in the dataframe")
    current_cell = cell_list[cell_no -1]
    if not current_cell.adhesins[molecule_ID-1].ID == molecule_ID:
        raise IndexError("The intended target adhesin does not exist in the dataframe")
    current_adhesin = current_cell.adhesins[molecule_ID-1]
    current_adhesin.add_membrane(coordinates)


#This function calculates the length between two points and is redundant to numpy, however, the ability to avoid numpy appears to allow the result to be directly added to the dataframe without merging

