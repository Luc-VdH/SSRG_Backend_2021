import os


class Report:
    COMPLETE = 1
    PROCCESSING = 0
    FAILED = -1

    def __init__(self, name, coursecode, status=0, rawURL='', scrapedURL=''):
        self.reportName = name
        self.coursecode = coursecode
        self.status = status
        self.urlOfRawReport = rawURL
        self.urlOfScrappedReport = scrapedURL
        self.writeToFile()

    def getCoursecode(self):
        return self.coursecode

    def isReport(self, name, coursecode):
        return self.reportName == name and self.coursecode == coursecode

    def getRawReport(self):
        if self.status == Report.COMPLETE:
            return self.urlOfRawReport
        else:
            return ''

    def getScrappedReport(self):
        if self.status == Report.COMPLETE:
            return self.urlOfScrappedReport
        else:
            return ''

    def checkStatus(self):
        return self.status

    def jobFailed(self):
        self.status = Report.FAILED

    def addRawURL(self, url):
        self.urlOfRawReport = url
        self.status = Report.COMPLETE
        self.writeToFile()

    def writeToFile(self):
        f = open(f"reports/{self.coursecode}/{self.reportName}/reportObject.txt", "w")
        f.write(f"{self.status}\n{self.urlOfRawReport}\n{self.urlOfScrappedReport}")
        f.close()

    def getJob(self):
        if self.status == Report.PROCCESSING:
            return '{"name":"' + self.reportName + '","status":"' + "Processing" + '","submissionDate":"' + "10/20/2000" +'"}'
        elif self.status == Report.COMPLETE:
            return '{"name":"' + self.reportName + '","status":"' + "Complete" + '","submissionDate":"' + "10/20/2000" +'"}'
        else:
            return '{"name":"' + self.reportName + '","status":"' + "Failed" + '","submissionDate":"' + "10/20/2000" +'"}'

    def delete(self):
        os.remove(f"reports/{self.coursecode}/{self.reportName}.txt")
