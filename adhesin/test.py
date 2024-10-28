from make_csv import *
import os
import pandas as pd
output_path = os.path.join(os.path.dirname(__file__), "tests/temp/CdrA_good_read.csv")
input_path = os.path.join(os.path.dirname(__file__), "tests/test_data/CdrA_contflag.txt")
df = pd.DataFrame(columns=['x','y','z','CdrA_molecule','Cell','Tomogram'])
df.to_csv(output_path, index=False)

print(os.path.dirname(__file__), "/test/test_data/CdrA_contflag.txt")
print(input_path)
print("Hello")
CdrA_processing(input_path, "d01t02", output_path)