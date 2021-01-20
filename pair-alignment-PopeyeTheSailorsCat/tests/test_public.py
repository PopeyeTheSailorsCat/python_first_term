from src import main as mn
from src import NV_alignment as alignment

assert mn.hamming("ab", "aa") == 1
assert mn.hamming("aaa", "aaa") == 0
assert mn.hamming("aaba", "babb") == 2
seq1 = "TGCTCGGACTACACGCATTATTGCAG"
seq2 = "TATTATGTATAGAGTTACACGGGCAT"
assert mn.hamming(seq1, seq2) == 16

assert alignment.calc_score(93, 83, 77, 1, 3, 3, -1) == 90.0
assert alignment.calc_score(84, 50, 50, 0, 3, 3, -2) == 81.0
seq1 = "TGTTACCCATTACATTG"
seq2 = "TTTCCAAGGCATCTT"
res, line = alignment.align(seq1, seq2, 4, 4, -1)
assert res == 20

seq1 = "AGTGTCGGCT"
seq2 = "ACTTCTACCCCAGC"
res, line = alignment.align(seq1, seq2, 1.399, 2.2168, -4.4499)
assert abs(res - -3.4872) < 1e-2
print(line[0])
