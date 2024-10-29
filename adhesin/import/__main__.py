import argparse
import numpy as np
from adhesin import make_csv ## importing the functions
import pandas as pd

parser = argparse.ArgumentParser(
        description = """ This programme will compile coordinate information from IMOD model text file outputs.
        The format of the models is important in this, for object naming conventions see README.md.
        Please specify the input file(s), output file, and whether to overwrite all existing data.
        The output csv should have columns as specified in the README file; please generate a new csv if unsure.
        Input files should be located in a single folder, and titled in the form [tomgoram].txt
        Please specify the object title to be read using -object_name, the default is CdrA.
        Further commands are in development to run analysis.""",
        epilog = 'That is how you run this programme!')
parser.add_argument("-input_path", "--in_pth", nargs = '?', default = 0, type = str,
                    help="input text file path [/]")
parser.add_argument("-tomograms", "--tomograms", nargs = '+', type = str,
                    help="input tomogram name(s)")
parser.add_argument("-output_path", "--out_pth", nargs = '?', type = str,
                    help="output csv file path [.csv]")
parser.add_argument("-overwrite", "--over", nargs = '?', default = 'N', type = str,
                    help="Should the programme overwrite data associated with the existing tomogram by default? [Y/N]")
parser.add_argument("-object_name", "--obj", nargs = '?', default = 'CdrA', type = str,
                    help="What is the component of the 3dmod object name the function should search for? e.g. CdrA. NB - this is case sensitive")    

def main():
    ## Setting up the variables
    args = parser.parse_args()
    # Set the default output path based on the obj argument if out_pth is not provided
    if args.out_pth is None:
        args.out_pth = f"output_{args.obj}.csv"
    tomo_lst = list(args.tomograms)
    print(tomo_lst)
    ## Running the programme
    print(args.out_pth, flush=True)
    if make_csv.check_and_create_csv(args.out_pth, args.obj):
        pass
        #if a file has just been written, the above statement is true so there is no need to check for overwriting
    else:
        output_df = pd.read_csv(args.out_pth)
        if args.over == 'Y':
            print("Overwriting", flush=True)
            for i in tomo_lst:
                i = str(i)
                #Removing any data regarding tomograms which are to be re-analysed
                output_df = output_df[output_df['Tomogram'] != i]
            output_df.to_csv(args.out_pth, index = False)
        else:
            print("Contracting list", flush=True)
            output_lst = tomo_lst[:]
            for i in tomo_lst:
                i = str(i)
                #Only retaining input tomograms which do not have any entries in the output file
                if i in output_df['Tomogram'].values:
                    output_lst.remove(i)
            tomo_lst = output_lst
    print("Running: "+str(tomo_lst))
    for i in tomo_lst:
        input_path = args.in_pth + '/' + i + '.txt'
        make_csv.contour_processing(i, args.obj, input_path, args.out_pth)

if __name__ == "__main__":
    main()
