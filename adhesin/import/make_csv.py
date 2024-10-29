import csv
import warnings
import os
import pandas as pd
#Function to see if the output file already exists

def check_and_create_csv(file_path, obj):
    # Check if the file exists
    if not os.path.exists(file_path):
        # Create the file if it doesn't exist
        df = pd.DataFrame(columns=['x','y','z',obj,'Cell','Tomogram'])
        df.to_csv(file_path, index=False)
        print(f"{file_path} has been created.")
        return True
    else:
        print(f"{file_path} already exists.")
        df = pd.read_csv(file_path)
        if obj in df.columns:
            print("Column found in header, all is well")
        else:
            raise ValueError("The given output file does not have a column titled [obj]; please chose an alternative output location")
        return False


#Function to process contour data from text file
def contour_processing(Tomogram, obj, filepath, outpath):
    """
    Takes a text filepath and Tomogram name of the file, and appends it to the csv given by outpath
    """
    #There is no return as the function is outputting to the csv file

    #Initial parameters are set to OFF/0
    record_lines=False
    Number_objects = 0
    Correct_object=False
    line_number = 0
    with open(filepath) as f:
        found = any((obj in line) and ("name" in line) for line in f)
        if not found:
            raise NotImplementedError("No objects containing the given text could be found")
        else:
            pass
    #With is used so that the file will be closed after the function is finished
    with open(filepath) as f:
        #The code iterates through every line in the text file
        for line in f:
            line_number += 1
            #This first step finds the first incidence of object, sets the correct_object paramter to false as a baseline
            if "object" in line:
                Correct_object = False
            
            #This function records the CdrA molecule of interest, so it starts considering if data should be recorded when CdrA is observed after object - ie an object named with 'CdrA'
            if obj in line:
                Correct_object = True
                #The number of times CdrA is printed should correspond to the number of cells containing CdrA in the tomogram
                print(f"Adding {Tomogram}-Cell{Number_objects+1}")
                #Each CdrA-containing object must be titled with CdrA
                
                #The Number_objects parameter is used to record which cell a CdrA molecule belongs to
                #Number_objects = cell_number
                Number_objects = Number_objects + 1

                #The current_contour count is reset for each cell
                Current_contour = 0
            
            #This code accounts for the case where for unknown reasons the contour is not bounded by contflags - as the result is appended line by line, this should work in the case that the next line is contour (as the molecule number will increase by one anway) or that the next line starts with a letter provided the code is already recording
            if Correct_object:
                first_char = line[0]
                if first_char.isalpha():
                    if "contour" in line:
                        record_lines = True
                        Current_contour = Current_contour + 1
                        check = list(line.strip().split())
                        if not int(check[1]) == Current_contour - 1 :
                            raise NotImplementedError("Contour counter and number in file are out of sync, check input file")
                    elif record_lines:
                        record_lines = False
                        if "contflags" in line:
                            continue
                            #print("contflags")
                        #This next bit doesnt usually work because if object is in the line, the Correct_object parameter will already be false, but if any other string than contflags bounds the contour (suggesting an error) it should be caught here
                        else:
                            warnings.warn(f"Found '{line}' at end of contour in line {line_number} of {Tomogram}", UserWarning)
            else:
                #If the object is wrong data should not be recorded
                record_lines = False
                #If the object is correct, data should be recorded if a contour is being read
            
            #The function is thus set to record after reading 'contour' within an object containing 'CdrA'
            if record_lines:
                #The first three if statements ensure that the line containing contour is not recorded, and that if the molecule ends in an empty line or line with spaces this is passed and so not appended to the csv
                if "contour" in line:
                    pass
                elif not line:
                    warnings.warn(f"Contour ends with no next line at line {line_number} of {filepath}", UserWarning)
                    pass
                elif line.isspace():
                    warnings.warn(f"Contour ends with space not contflags at line {line_number} of {filepath}", UserWarning)
                    pass
                else:
                    #list is creating the list. Map is convering the strings into float (as this is the next argument)
                    #line.strip() removes white spaces at each end; .split() separates using space as the divider
                    Points = list(map(float, line.strip().split()))
                    #The next line appends which CdrA molecule the point belongs to to the list (f specifies formula, {} used for the variable)
                    Points.append(Current_contour)
                    #Same as above, but for the Cell of origin
                    Points.append(Number_objects)
                    #Same as above, but for the tomogram of interest
                    Points.append(Tomogram)
                    #This opens the csvfile so the data can be added ('a' for appending data); newline='' is apparently important to add in windows

                    #NOTE this function appends the data to an existing csv file, so if it is run multiple times per filepath the data will be duplicated
                    with open(outpath,'a',newline='') as csvfile:
                        #I'm not entirely sure what this line does
                        csvwriter=csv.writer(csvfile)
                        #This adds the current point list to the next rown in Csv
                        csvwriter.writerow(Points)