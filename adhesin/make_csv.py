import csv

#Function to process CdrA data from text file
def CdrA_processing(filepath, Tomogram, outpath):
    """
    
    Takes a text filepath and Tomogram name of the file, and appends it to the csv given by outpath"""
    #There is no return as the function is outputting to the csv file

    #Initial parameters are set to OFF/0
    record_lines=False
    Number_objects = 0
    Correct_object=False    
    
    #With is used so that the file will be closed after the function is finished
    with open(filepath) as f:
        #The code iterates through every line in the text file
        for line in f:

            #This first step finds the first incidence of object, sets the correct_object paramter to false as a baseline
            if "object" in line:
                Correct_object = False
            
            #This function records the CdrA molecule of interest, so it starts considering if data should be recorded when CdrA is observed after object - ie an object named with 'CdrA'
            if "CdrA" in line:
                Correct_object = True
                #The number of times CdrA is printed should correspond to the number of cells containing CdrA in the tomogram
                print(f"{Tomogram}-Cell{Number_objects}")
                #Each CdrA-containing object must be titled with CdrA
                
                #This is a workaround to allow the cell to be in a different order than the membrane:
                #index_cell = line.find("Cell")
                #cell_number = line[index_cell + len("Cell"):].split('_')[0]
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
                    elif record_lines:
                        record_lines = False
                        if "contflags" in line:
                            continue
                            #print("contflags")
                        #This next bit doesnt usually work because if object is in the line, the Correct_object parameter will already be false, but if any other string than contflags bounds the contour (suggesting an error) it should be caught here
                        else:
                            print(f"Weird in {line} of {Tomogram}")
            else:
                #If the object is wrong data should not be recorded
                record_lines = False
                #If the object is correct, data should be recorded if a contour is being read
            
            #Previous code where contflags had to be manually added in minority of cases
            # if Correct_object:
            #     if "contour" in line:
            #     #A contour is one molecule, used to determine which molecule a point belongs to, and mark the start of data recording
            #     #The record_lines parameter is True/False, used to enable the later if statement 
            #     # to record information between the start and end of a contour
            #         record_lines = True
            #         Current_contour = Current_contour+1
            #     #The contour text itself is not a point, so does not need to be recorded. Continue means that the loop continues
            #     #** Does this mean that the later if statement is not processed after the completion of the first?
            #         continue
            
            # #Marks the end of each object for some reason. Code ends the recording of point data
            # if "contflags" in line:
            #     record_lines = False
            
            #The function is thus set to record after reading 'contour' within an object containing 'CdrA'
            if record_lines:
                #The first three if statements ensure that the line containing contour is not recorded, and that if the molecule ends in an empty line or line with spaces this is passed and so not appended to the csv
                if "contour" in line:
                    pass
                elif not line:
                    print("Hello")
                    pass
                elif line.isspace():
                    print("Hi")
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