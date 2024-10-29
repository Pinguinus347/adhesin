import pytest
import numpy as np
import numpy.testing as npt
import csv
import pandas as pd
import os
@pytest.mark.parametrize(
    "input, tomogram, obj, output, expected, expect_raises",
    [
        #optimal file configuration
        (
            "test_data/CdrA_good.txt",
            "d01t01",
            "CdrA",
            "CdrA_read.csv",
            "test_data/CdrA_good.csv",
            None,
        ),
        #missing conflags so warning
        (
            "test_data/CdrA_contflag.txt",
            "d01t01",
            "CdrA",
            "CdrA_read.csv",
            "test_data/CdrA_good.csv",
            UserWarning,
        ),
        #fatal error - obj numbers do not match counter
        (
            "test_data/CdrA_error.txt",
            "d01t01",
            "CdrA",
            "CdrA_read.csv",
            "test_data/CdrA_good.csv",
            NotImplementedError,
        ),
        #fatal error - no objects matching the string
        (
            "test_data/CdrA_good.txt",
            "d01t01",
            "cdrb",
            "CdrA_read.csv",
            "test_data/CdrA_good.csv",
            NotImplementedError,
        ),
        #Recording membrane instead
        (
            "test_data/CdrA_good.txt",
            "d01t01",
            "membrane",
            "membrane_read.csv",
            "test_data/membrane_good.csv",
            None,
        ),
    ]
)
def test_CdrA_processing(tmp_path, input,tomogram,obj,output,expected,expect_raises):
    """Tests that the import function is working as expected"""
    import adhesin as ad
    # Create a path relative to the test file's location
    input_path = os.path.join(os.path.dirname(__file__), input)
    expected_path = os.path.join(os.path.dirname(__file__), expected)
    # Create a temporary output path
    output_path = tmp_path / output
    # Create the output file for writing data into:
    df = pd.DataFrame(columns=['x','y','z',obj,'Cell','Tomogram'])
    df.to_csv(output_path, index=False)
    if expect_raises is NotImplementedError:
        with pytest.raises(expect_raises):
            ad.contour_processing(tomogram, obj, input_path, output_path)
    elif expect_raises is not None:
        with pytest.warns(expect_raises):
            ad.contour_processing(tomogram, obj, input_path, output_path)
            with open(output_path, mode='r') as file1, open(expected_path, mode='r') as file2:
                reader1 = csv.reader(file1)
                reader2 = csv.reader(file2)
        
                for row1, row2 in zip(reader1, reader2):
                    # Process rows here
                    print("File1:", row1)
                    print("File2:", row2)
                    npt.assert_equal(row1, row2)

    else:
        ad.contour_processing(tomogram, obj, input_path, output_path)
        with open(output_path, mode='r') as file1, open(expected_path, mode='r') as file2:
            reader1 = csv.reader(file1)
            reader2 = csv.reader(file2)
        
            for row1, row2 in zip(reader1, reader2):
                # Process rows here
                npt.assert_equal(row1, row2)

@pytest.mark.parametrize(
    "filepath, obj, expected, expect_raises",
    [
        #file creation successfully
        (
            "test.csv",
            "CdrA",
            True,
            None,
        ),
        #file exists with correct columns
        (
            "test_data/CdrA_good.csv",
            "CdrA",
            False,
            None,
        ),
        #fatal error - file exists with incorrect columns
        (
            "test_data/membrane_good.csv",
            "CdrA",
            False,
            ValueError,
        ),
    ]
)
def test_csv_checking(tmp_path,filepath,obj,expected,expect_raises):
    """Tests that checking for the output csv is working as expected"""
    import adhesin as ad
    if expected:
        temp_file = tmp_path / filepath
        #Checking the file does not exist before the function is run
        npt.assert_equal(os.path.exists(temp_file), False)
        #Function is run and output recorded
        output = ad.check_and_create_csv(temp_file,obj)
        #Correct output
        npt.assert_equal(output,expected)
        #Checking the file now exists as expected
        npt.assert_equal(os.path.exists(temp_file), True)
    else:
        # Create a path relative to the test file's location
        input_path = os.path.join(os.path.dirname(__file__), filepath)
        if expect_raises is not None:
            with pytest.raises(expect_raises):
                ad.check_and_create_csv(input_path, obj)
        else:
            npt.assert_equal(ad.check_and_create_csv(input_path,obj),expected)
