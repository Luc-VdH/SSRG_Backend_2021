import os

from src.Report import Report
import unittest


class TestReport(unittest.TestCase):
    def test_init(self):
        report = Report("Job1", "coursecode", "10/10/2021")
        self.assertEqual(report.getCoursecode(), "coursecode")
        self.assertEqual(report.getJob(), '{"name":"Job1","status":"' + "Processing" + '","submissionDate":"10/10/2021"}')
        exists = os.path.isfile("reports/coursecode/Job1/reportObject.txt")
        self.assertEqual(exists, True)

    def test_complete(self):
        report = Report("Job2", "coursecode", "10/10/2021")
        report.addJobCompleteInfo("rawUrl", "data")
        self.assertEqual(report.getStatus(), 1)
        self.assertEqual(report.getRawReport(), "rawUrl")
        self.assertEqual(report.getScrappedReport(), "data")

    def test_fail(self):
        report = Report("Job3", "coursecode", "10/10/2021")
        report.jobFailed()
        self.assertEqual(report.getStatus(), -1)

    def test_equal(self):
        report = Report("Job4", "coursecode", "10/10/2021")
        self.assertEqual(report.isReport("Job4", "coursecode"), True)
