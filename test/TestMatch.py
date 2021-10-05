from src.Match import Match
import unittest


class TestMatch(unittest.TestCase):
    def testMatch(self):
        m = Match("file1", "file2", "90%")
        self.assertEqual(m.toString(), '{"files": ["file1", "file2"], "percent": "90%", "lines": [[]]}')
        lines = [["line1", "line2"], ["line3", "line4"]]
        m.addLines(lines)
        self.assertEqual(m.toString(), '{"files": ["file1", "file2"], "percent": "90%", "lines": [["line1", "line2"], ["line3", "line4"]]}')