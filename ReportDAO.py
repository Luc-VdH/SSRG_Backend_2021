import os

from Report import Report


class ReportDAO:
    def __init__(self):
        self.reports = []
        self.initReports()

    def initReports(self):
        # TODO
        self.reports=[]
        for subdir, dirs, files in os.walk(os.getcwd() + "/reports"):
            for filename in files:
                filepath = subdir + os.sep + filename

                if filepath.endswith(".txt"):
                    f = open(filepath, "r")
                    parts = filepath.split("/")
                    status = f.readline().strip()
                    raw = f.readline().strip()
                    scraped = f.readline().strip()
                    f.close()
                    report = Report(parts[-2], parts[-3], int(status), raw, scraped)
                    self.reports.append(report)

        print("Initilising all reports")

    def addReport(self, name, coursecode):
        report = Report(name, coursecode)
        self.reports.append(report)

    def getReportIndex(self, name, coursecode):
        count = 0
        for r in self.reports:
            if r.isReport(name, coursecode):
                return count
            count += 1
        return -1

    def getReportStatus(self, name, coursecode):
        index = self.getReportIndex(name, coursecode)
        if index == -1:
            return -10
        return self.reports[index].checkStatus()

    def getReport(self, name, coursecode):
        index = self.getReportIndex(name, coursecode)
        if index == -1:
            return -10
        return self.reports[index].getRawReport()  # TODO: scraped

    def deleteReport(self, name, coursecode):
        index = self.getReportIndex(name, coursecode)
        if index == -1:
            return False
        self.reports.pop(index).delete()
        return True

    def getAllJobs(self, coursecode):
        self.initReports()
        jobs = ""
        for x in self.reports:
            if x.getCoursecode() == coursecode:
                jobs += x.getJob() + ", "
        return "[" + jobs[:len(jobs)-2] + "]"


