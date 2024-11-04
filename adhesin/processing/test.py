d01t01 = tomogram('d01t01')
cell1 = d01t01.add_cell(1)
d01t01.list_cells()
print(d01t01.cells[0])
adhesin1 = pd.DataFrame({
    "x": [1, 2, 3, 4],
    "y": [5, 6, 7, 8],
    "z": [0, 0, 2, 2],
})
membrane1 = pd.DataFrame({
    "x": [1, 2, 3, 4,1, 2, 3, 4,1],
    "y": [5, 6, 7, 8,1, 2, 3, 4,1],
    "z": [0, 0, 2, 2,1, 2, 3, 4,1],
})
test_adhesin = adhesin(adhesin1, "CdrA",15)
test_adhesin.add_membrane(membrane1,0.5)
print(test_adhesin.membrane.coords)
test_adhesin.calculate_paramters()
print(test_adhesin.length)
# test_contour = contour(adhesin1, 1)
# print("checking")
# print(test_contour.ID)
# value = test_contour.ID
# print(value)
# print("checking adhesin")
# print(test_adhesin.ID)
# d01t01.cells[0].add_adhesin(coords = pd.DataFrame(adhesin1), adhesin_type = 'CdrA',ID = 1)
# print("TEST")
# print(d01t01.cells[0].adhesins[0].ID)

input = pd.read_csv("/home/callum/adhesin/output_CdrA.csv")

adhesin_type = 'CdrA'

input.groupby(['Tomogram','Cell',adhesin_type]).apply(classify)

d01t11_even = tomogram.instances["d01t11_even"]
# print("accessing adhesin 1")
# print("printing adhesin list")
d01t11_even.list_cells()
# print(test_adhesin)
# print("different syntax")
# print(test_adhesin.ID)
# print("why no ID?")
# print(d01t11_even.cells[0])
d01t11_even.csv_make()
# print(d01t11_even.csv_view())


#write code to sort through the different tomograms and cells, and create objects for each

#then write code to append membrane to these

#then write functions within adhesin class to automatically generate summary information

#then return everything to a dataframe through a function in tomogram class (e.g. unpack)

#then develop plotting capabilities.



# test = adhesin(pd.DataFrame(adhesin1),1)
# print(test)
