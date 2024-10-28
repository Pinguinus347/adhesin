import argparse
import numpy as np
from adhesin import * ## importing all known functions

parser = argparse.ArgumentParser(
        description = """ This programme will compile coordinate information from IMOD model text file outputs.
        The format of the models is important in this, for object naming conventions see README.md.
        Please specify the input file(s), output file, and whether to overwrite all existing data.
        The output csv should have columns as specified in the README file; please generate a new csv if unsure.
        Input files should be located in a single folder, and titled in the form [tomgoram].txt
        Further commands are in development to run analysis.""",
        epilog = 'That is how you run this programme!')
parser.add_argument("-input_path", "--in_pth", nargs = '?', default = 0, type = str,
                    help="input text file path [/]")
parser.add_argument("-tomograms", "--tomograms", nargs = '+', type = str,
                    help="input tomogram name(s)")
parser.add_argument("-output_path", "--out_pth", nargs = '?', default = ".output.csv", type = str,
                    help="output csv file path [.csv]")
parser.add_argument("-overwrite", "--over", nargs = '?', default = 'N', type = str,
                    help="Should the programme overwrite data associated with the existing tomogram by default? [Y/N]")

def main():
    ## Setting up the variables
    args = parser.parse_args()
    tomo_lst = list(args.tomograms)
    print(tomo_lst)
    print("Hello", flush=True)
    ## Running the programme
    if check_and_create_csv(args.out_pth):
        print("Wrong", flush=True)
        pass
        #if a file has just been written, the above statement is true so there is no need to check for overwriting
    else:
        print("True", flush=True)
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
                print(i, flush=True)
                i = str(i)
                #Only retaining input tomograms which do not have any entries in the output file
                if i in output_df['Tomogram'].values:
                    print(i)
                    print(tomo_lst)
                    output_lst.remove(i)
                    print(tomo_lst, flush=True)
            tomo_lst = output_lst
            print(tomo_lst)
    for i in tomo_lst:
        input_path = args.in_pth + '/' + i + '.txt'
        CdrA_processing(input_path, i, args.out_pth)

if __name__ == "__main__":
    main()
