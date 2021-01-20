class DNA_counter:  # Class for easy calculation of nitrogenous bases
    def __init__(self):
        self.dict = {'A': 0, 'T': 0, 'G': 0, 'C': 0}  # If we are working with something else, you should change
        self.max = 0  # We will use max to determine whether the column is identical(max/number of elements)

    def count(self, elem):
        """
        :param elem: char\str element to count
        :return: None
        """
        current_count = self.dict.get(elem)  # Getting the current calculated value
        if current_count is None:  # If there is no such element
            return  # we do not stop the program, as there may be permission for unfamiliar elements

        if self.max < current_count + 1:  # update the maximum value if necessary
            self.max = current_count + 1
        self.dict.update(**{elem: current_count + 1})  # Updating the counter value

    def value_of(self, elem):
        return self.dict.get(elem)  # We return what we counted

    def max(self):  # Returning our maximum
        return self.max
