import os
import sys
import unittest

curr_dir = os.path.abspath('')
parent_dir = os.path.dirname(curr_dir)
if not parent_dir in sys.path:
    sys.path.append(parent_dir)

import src.main as mn
import src.NV_alignment as align


class TestF(unittest.TestCase):
    def test_hamming(self):
        self.assertEqual(mn.hamming("aac", "cab"), 2)
        self.assertEqual(mn.hamming("sss", "sss"), 0)
        self.assertEqual(mn.hamming("ooo", "aaa"), 3)

    def test_init(self):
        self.assertEqual(align.init(1, 1, 2), [[0, -2], [-2, 0]])
        self.assertEqual(align.init(1, 2, 0), [[0, 0, 0], [0, 0, 0]])

    def test_calc_score(self):
        self.assertEqual(align.calc_score(93, 83, 77, 1, 3, 3, -1), 90.0)
        self.assertEqual(align.calc_score(84, 50, 50, 0, 3, 3, -2), 81.0)

    def test_align(self):
        seq1 = "TGTTACCCATTACATTG"
        seq2 = "TTTCCAAGGCATCTT"
        res, line = align.align(seq1, seq2, 4, 4, -1)
        self.assertEqual(res, 20)

        seq1 = "AGTGTCGGCT"
        seq2 = "ACTTCTACCCCAGC"
        res, line = align.align(seq1, seq2, 1.399, 2.2168, -4.4499)
        self.assertLess(abs(res - -3.4872), 1e-2)
        self.assertEqual(line[0], "AG-TGTC-------GGCT")
