
from src import structures as st
from src import calculator
from src import counter as ct


def counter_test():
    print("Проверяю счетчик элементов...")
    test_dna_count = "AGTTGGC"
    counter = ct.DNA_counter()
    for symb in test_dna_count:
        counter.count(symb)
    assert counter.value_of('G') == 3
    assert counter.max == 3
    print("Успешно!")


def sqn_test():
    print("Проверяю Sequence...")
    test = "ATTAGC"
    seq = st.Sequence(test)
    assert seq[3] == test[3]
    assert seq[1] == test[1]
    print("Успешно!")


def sqn_col_test():
    print("Проверяю Col Sequence...")
    test_1 = "AT"
    test_2 = "GC"
    cols = st.Sequence_column.build([st.Sequence(test_1), st.Sequence(test_2)])  # Checking the creation of a list of
    # columns
    assert cols[0][1] == 'G'
    assert cols[1][0] == 'T'

    test = ['A', 'T', 'C', 'C', 'T', 'T', 'G', 'G', 'G', 'A']
    col = st.Sequence_column(test)
    col.calc()
    assert col.counter.value_of('A') == 2
    # print(col.get_prob())
    assert col.prob == 0.3  # 10 items, a maximum of 3 similar
    assert col.ban_unknown_symbol() is False
    assert col.ban_less_percent(0.5) is True
    print("Успешно!")


def calculate_test():
    print("Проверяю BLOSUM calculator")
    line_1, line_2, line_3, line_4 = "CTCA", "ATGA", "CTGA", "CGGT"
    dictionary = {0: 'A', 1: 'T', 2: 'G',
                  3: 'C'}
    sqn = [st.Sequence(line_1), st.Sequence(line_2), st.Sequence(line_3), st.Sequence(line_4)]
    cols = st.Sequence_column.build(sqn)
    for elem in cols:
        elem.calc()
        print(elem)
    res = calculator.create_matrix(dictionary, cols)
    print(res)
    assert res[0][0] == 2  # NOT COUNTED BY HAND, BUT USING THE SAME PROGRAM!!!
    assert res[1][1] == 2
    print("Успешно")


counter_test()
sqn_test()
sqn_col_test()
calculate_test()
