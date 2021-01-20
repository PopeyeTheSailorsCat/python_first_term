from src import structures
import logging as lg
from src.structures import Sequence


class File_studier:  # Class for reading and extracting useful data from files
    # Returns the Sequense list
    def parse_file(self, path, file):
        """
        :param str path:
        :param str file:
        :return: list Sequence read_seq: Read lines with data from this file
        """
        try:
            f = open(path + "\\" + file)  # We have a path to open the file and add the file name
        except IOError:
            lg.info("ERROR DURING FILE OPENING:" + file)
            return []

        read_seq = []
        lg.info("open" + file)
        for line in f:
            read_seq.append(self._parse_line(line))
        try:
            f.close()
        except IOError:
            lg.info("ERROR DURING FILE CLOSING. PROGRAM DOES NOT  CLOSE FILE: "+file)
            return read_seq

        lg.info("closed " + file)

        return read_seq

    @staticmethod
    def _parse_line(line):  # Getting useful data from the string
        return structures.Sequence(line.split()[1])  # THIS LINE IS STRICTLY TIED TO OUR DATA FORMAT
