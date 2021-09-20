import os
import datetime
import subprocess

location = subprocess.check_output("pwd", shell=True).decode("utf-8")
if "ssrg_backend/test" in location:
    from src.Report import Report
else:
    from Report import Report


# class for managing all reports
class ReportDAO:
    # constructor
    def __init__(self):
        self.reports = []
        if "ssrg_backend/test" not in location:
            self.initReports()

    # read all report object files and populate list of report objects
    def initReports(self):
        # reset list
        self.reports = []
        # go through all files and dirs in reports dir
        for subdir, dirs, files in os.walk(os.getcwd() + "/reports"):
            for filename in files:
                filepath = subdir + os.sep + filename
                # if it is a text file, read it
                if filepath.endswith(".txt"):
                    f = open(filepath, "r")
                    # break path into array of directory names, for getting the coursecode and jobname
                    parts = filepath.split("/")
                    # read data from file
                    status = f.readline().strip()
                    date = f.readline().strip()
                    raw = f.readline().strip()
                    scraped = f.readline().strip()
                    f.close()
                    # create report object
                    report = Report(parts[-2], parts[-3], date, int(status), raw, scraped)
                    # add object to list
                    self.reports.append(report)

        print("Initilising all reports")

    # create a new report object is status: processing and no urls and add it to the list
    def addReport(self, name, coursecode):
        fulldate = datetime.datetime.now()
        date = str(fulldate.year) + "/" + "{:02d}".format(fulldate.month) + "/" + "{:02d}".format(fulldate.day) + " - " + "{:02d}".format(
            fulldate.hour) + ":" + "{:02d}".format(fulldate.minute)
        report = Report(name, coursecode, date, 0, "none", "none")
        self.reports.append(report)

    # search the list and return the index of the report object desired
    def getReportIndex(self, name, coursecode):
        count = 0
        for r in self.reports:
            if r.isReport(name, coursecode):
                return count
            count += 1
        return -1

    # get the status of a particular report
    def getReportStatus(self, name, coursecode):
        index = self.getReportIndex(name, coursecode)
        if index == -1:
            return -10
        # self.reports[index].refresh()
        return self.reports[index].checkStatus()

    # get the raw moss url of a report
    def getReport(self, name, coursecode):
        index = self.getReportIndex(name, coursecode)
        if index == -1:
            # return junk address if the report cant be found TODO account for failed/incomplete jobs
            return "no course"
        return self.reports[index].getRawReport(), self.reports[index].getScrappedReport(), self.reports[index].getStatus()  # TODO: scraped

    # delete a report based on its name and coursecode
    def deleteReport(self, name, coursecode):
        index = self.getReportIndex(name, coursecode)
        if index == -1:
            return False
        self.reports.pop(index).delete()
        return True

    # go through all the reports and build a json array as text containing all the job information
    def getAllJobs(self, coursecode):
        jobs = ""
        for x in self.reports:
            if x.getCoursecode() == coursecode:
                jobs += x.getJob() + ", "
        return "[" + jobs[:len(jobs) - 2] + "]"

    # update a report with the information provided
    def updateReport(self, name, coursecode, status, url, data):
        index = self.getReportIndex(name, coursecode)
        if index == -1:
            return False
        if status == -1:
            self.reports[index].jobFailed()
        else:
            self.reports[index].addJobCompleteInfo(url, data)

if __name__ == "__main__":
    rd = ReportDAO()
    rd.addReport("job", "course")
    print(rd.getAllJobs("course"))
