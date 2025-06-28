import unittest
from src.mkdf.fs.brace_expansion import brace_expand

class TestBraceExpansion(unittest.TestCase):

    def test_simple_expansion(self):
        self.assertEqual(brace_expand("a{b,c}d"), ["abd", "acd"])

    def test_nested_expansion(self):
        self.assertEqual(brace_expand("a{b,c{d,e}}f"), ["abf", "acdf", "acef"])

    def test_no_braces(self):
        self.assertEqual(brace_expand("abc"), ["abc"])

    def test_empty_braces(self):
        self.assertEqual(brace_expand("a{}b"), ["ab"])

    def test_multiple_brace_groups(self):
        self.assertEqual(brace_expand("a{b,c}d{e,f}"), ["abde", "abdf", "acde", "acdf"])

    def test_numeric_range_expansion(self):
        self.assertEqual(brace_expand("file{1..3}.txt"), ["file1.txt", "file2.txt", "file3.txt"])
        self.assertEqual(brace_expand("item{5..2}.log"), sorted(["item5.log", "item4.log", "item3.log", "item2.log"]))

    def test_char_range_expansion(self):
        self.assertEqual(brace_expand("char{a..c}.js"), ["chara.js", "charb.js", "charc.js"])
        self.assertEqual(brace_expand("char{Z..X}.py"), sorted(["charZ.py", "charY.py", "charX.py"]))

    def test_mixed_range_and_list_expansion(self):
        self.assertEqual(brace_expand("prefix{1..2,a,b}suffix"), sorted(["prefix1suffix", "prefix2suffix", "prefixasuffix", "prefixbsuffix"]))

    def test_range_in_nested_expansion(self):
        self.assertEqual(brace_expand("outer{inner{1..2},c}end"), sorted(["outerinner1end", "outerinner2end", "outercend"]))

if __name__ == '__main__':
    unittest.main()