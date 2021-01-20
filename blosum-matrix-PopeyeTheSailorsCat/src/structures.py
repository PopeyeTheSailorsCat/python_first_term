from src import counter


class Sequence:  # This class implements logic for working with strings
    def __init__(self, line):  # Remember the value
        self.line = line
        return

    def __str__(self):
        return self.line

    def __len__(self):
        return len(self.line)

    def __getitem__(self, item):  # For element-by-element treatment
        return self.line[item]


class Sequence_column:  # This class implements logic for working with columns
    def __init__(self, column):
        self.column = column
        self.counter = counter.DNA_counter()  # Creating a counter for each instance
        self.prob = -1  # Initially set the percentage of matches to -1

    def __str__(self):  # For easy display in the debug
        return ''.join(self.column)

    def __getitem__(self, item):
        return self.column[item]

    def __len__(self):
        return len(self.column)

    def calc(self):  # Use the counter to count the number of elements in the column. Updating the value of matches
        for symb in self.column:
            self.counter.count(symb)  # Giving an element to the counter to count it
        self.prob = self.counter.max / len(self)

    def get_prob(self):  # Gets the percentage of string similarity
        return self.prob
        # return

    def ban_less_percent(self, percent):  # Remove a column if it has less than the required probability
        if self.prob >= percent:
            return False  # Delete logic is implemented where the method is called
        return True

    def ban_unknown_symbol(self):  # Remove the column if it has a character other than ATGC
        if self.counter.value_of('A') + self.counter.value_of('C') + self.counter.value_of('T') + self.counter.value_of(
                'G') != len(self.column):  # If the working data changes(for example, we will receive proteins),
            # it requires
            # processings
            return True  # Delete logic is implemented where the method is called
        return False

    @staticmethod
    def build(sequences):
        """
        Gets a set of sequences as input
        Creates a set of columns for them
        :param list sequences:
        :return list Sequence_column: columns of the sequence matrix
        """
        columns = []
        for j in range(len(sequences[0])):  # Go through the rows, as we create columns
            column = []
            for i in range(len(sequences)):  # going down by the number of rows
                column.append(sequences[i][j])
            columns.append(Sequence_column(column))

        return columns
