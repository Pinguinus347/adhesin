import pytest
import numpy as np
import numpy.testing as npt
import csv
import pandas as pd
import os
@pytest.mark.parametrize(
    "input, tomogram, output, expected, expect_raises",
    [
        #optimal file configuration
        (
            "test_data/CdrA_good.txt",
            "d01t01",
            "temp/CdrA_good_read.csv",
            "test_data/CdrA_good.csv",
            None,
        ),
        # #missing conflags so warning
        # (
        #     "./test_data/CdrA_contflag.txt",
        #     "d01t02",
        #     "./temp/CdrA_contflag.csv",
        #     "./test_data/CdrA_good.csv"
        #     UserWarning,
        # ),
        # #fatal error
        # (
        #     "./test_data/CdrA_error.txt",
        #     "d01t03",
        #     "./temp/CdrA_error.csv",
        #     "./test_data/CdrA_good.csv"
        #     NotImplementedError,
        # ),
        # #overwriting warning
        # (
        #     "./test_data/CdrA_good.txt",
        #     "d01t04",
        #     "./temp/CdrA_good.csv",
        #     "./test_data/CdrA_good.csv"
        #     PermissionError,
        # ),
    ]
)
def test_CdrA_processing(input,tomogram,output,expected,expect_raises):
    """Tests that the import function is working as expected"""
    import adhesin as ad
    # Create a path relative to the test file's location
    input_path = os.path.join(os.path.dirname(__file__), input)
    output_path = os.path.join(os.path.dirname(__file__), output)
    expected_path = os.path.join(os.path.dirname(__file__), expected)
    # Create the output file for writing data into:
    df = pd.DataFrame(columns=['x','y','z','CdrA_molecule','Cell','Tomogram'])
    df.to_csv(output_path, index=False)
    if expect_raises is not None:
        with pytest.raises(expect_raises):
            ad.CdrA_processing(input, tomogram, output)
    else:
        ad.CdrA_processing(input_path, tomogram, output_path)
        with open(output_path, mode='r') as file1, open(expected_path, mode='r') as file2:
            reader1 = csv.reader(file1)
            reader2 = csv.reader(file2)
        
            for row1, row2 in zip(reader1, reader2):
                # Process rows here
                print("File1:", row1)
                print("File2:", row2)
                npt.assert_equal(row1, row2)