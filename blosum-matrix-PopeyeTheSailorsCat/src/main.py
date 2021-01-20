import os
import logging as lg

from src import file_scanner as fs
from src import structures as st
from src import calculator

# C:\Users\Admin\Desktop\python-hw\blosum-matrix-PopeyeTheSailorsCat\data 0.5 1
# my working param

if __name__ == '__main__':
    lg.basicConfig(filename='log.txt', filemode='w', level=lg.INFO)
    lg.info("Program stated")
    dictionary = {0: 'A', 1: 'T', 2: 'G',
                  3: 'C'}  # Dictionary of elements to work with. If the working data is changed, change it
    print("input path, percent of identity, and can be unknown symb")
    path, percent_req, unknown = input().split()
    percent_of_similarity = float(percent_req)
    lg.info("path:" + path)
    lg.info("percent:" + percent_req)
    lg.info("unknown:" + unknown)
    unknown = int(unknown)  # 1 can 0 can't have column with unknown symb
    data = []
    parser = fs.File_studier()  # To read files and get sequences from them
    for root, dirs, files in os.walk(path):
        if len(files) > 0:
            for file in files:
                data.extend(parser.parse_file(root, file))  # Write all the received strings to a single list
    seq_col = st.Sequence_column.build(data)  # Getting columns from our data

    for col in seq_col:  # Calculating our columns
        col.calc()

    delete_elem = []  # Many elements that we will delete due to unsuitability
    for col in seq_col:
        if col.ban_less_percent(percent_of_similarity):  # Where the similarity percentage is less than the boundary
            # value
            delete_elem.append(col)
        elif unknown == 0 and col.ban_unknown_symbol():  # If you were told to delete columns that contain unknown
            # characters (like -)
            delete_elem.append(col)

    print("Убранные строки:")
    lg.info("delete " + str(len(delete_elem)) + " bad line")
    for col in delete_elem:  # Deleting bad lines
        seq_col.remove(col)
        print(col)
    print()
    result = calculator.create_matrix(dictionary, seq_col)  # Getting the result from the calculator
    elem = []
    for i in range(len(dictionary)):  # For a Beautiful output
        elem.append(dictionary.get(i))
    print(elem)
    i = 0
    for elem in result:  # output
        print(dictionary.get(i), elem)
        i += 1
