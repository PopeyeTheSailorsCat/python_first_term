import os
import functools


class directory_reader_states:
    format_position_in_split = -1
    format_req = 'txt'


def print_iter(reader):  # a function decorator
    @functools.wraps(reader)
    def dir_reader_decorator(*args, **kwargs):  # the function that will be iterated
        inner_reader = reader(*args, **kwargs)
        for result in inner_reader:
            print(result)
            yield result

    return dir_reader_decorator


@print_iter
class DirReader:  # To read files in a directoryy
    def __init__(self, dir):
        self.walk = os.walk(dir)

    def work(self):
        for root, dirs, files in self.walk:
            if files:
                for file in files:
                    if file.split('.')[
                        directory_reader_states
                                .format_position_in_split] == directory_reader_states.format_req:  # If the file
                        # matches the format we need
                        yield root + "\\" + file  # giving the canonical path

    def __iter__(self):
        return self.work()
