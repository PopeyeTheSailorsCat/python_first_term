import os
import sys
import unittest

import src.directory_reader as d_r
import src.file_reader as f_r


class TestF(unittest.TestCase):
    def test_DirReader(self):
        for file in d_r.DirReader("test_dir"):
            self.assertEqual(file, "test_dir"+"\\test.txt")
