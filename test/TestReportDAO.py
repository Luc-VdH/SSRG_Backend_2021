from src.ReportDAO import ReportDAO
import unittest


class TestUserDAO(unittest.TestCase):
    def test_report(self):
        rd = ReportDAO()
        rd.addReport("JobD1", "coursecodeDAO")
        self.assertEqual(rd.getReportStatus("JobD1", "coursecodeDAO"), 0)

        rd.updateReport("JobD1", "coursecodeDAO", 1, "url", "data")
        raw, data, status = rd.getReport("JobD1", "coursecodeDAO")
        self.assertEqual(raw, "url")
        self.assertEqual(data, "data")
        self.assertEqual(status, 1)

        rd.addReport("JobD2", "coursecodeDAO")
        rd.updateReport("JobD2", "coursecodeDAO", -1, "url", "data")
        self.assertEqual(rd.getReportStatus("JobD2", "coursecodeDAO"), -1)

        jobs = False
        alljobs = rd.getAllJobs("coursecodeDAO")
        if '"name":"JobD1","status":"Complete"' in alljobs and '"name":"JobD2","status":"Failed"' in alljobs:
            jobs = True

        self.assertEqual(jobs, True)

        # rd.deleteReport("JobD1", "coursecode")
        # self.assertEqual(rd.getReportIndex("JobD1", "coursecode"), -1)
        # self.assertEqual(rd.deleteReport("JobD3", "coursecode"), False)

