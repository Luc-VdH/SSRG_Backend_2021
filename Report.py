import os


# class for managing a single report
class Report:
    # variables to map statuses to integer values
    COMPLETE = 1
    PROCCESSING = 0
    FAILED = -1

    # constructor
    def __init__(self, name, coursecode, status=0, rawURL='', scrapedURL=''):
        self.reportName = name
        self.coursecode = coursecode
        self.status = status
        self.urlOfRawReport = rawURL
        self.urlOfScrappedReport = scrapedURL
        # write information to file for persistent storage
        self.writeToFile()

    # coursecode getter
    def getCoursecode(self):
        return self.coursecode

    # check if this report matches coursecode and job name
    def isReport(self, name, coursecode):
        return self.reportName == name and self.coursecode == coursecode

    # raw moss url getter
    def getRawReport(self):
        print(self.status)
        if self.status == 1:
            return self.urlOfRawReport
        else:
            return "incomplete"

    # scrapped report getter
    def getScrappedReport(self):
        if self.status == Report.COMPLETE:
            return self.urlOfScrappedReport
        else:
            return ''

    # status getter
    def checkStatus(self):
        return self.status

    # set status to failed and update file
    def jobFailed(self):
        self.status = Report.FAILED
        self.writeToFile()

    # setter for raw url, updates file
    def addRawURL(self, url):
        self.urlOfRawReport = url
        self.status = Report.COMPLETE
        self.writeToFile()

    # writes all fields to a file
    def writeToFile(self):
        # create a path to the report files
        path = os.path.join("reports", self.coursecode, self.reportName)
        # make the directory if it does not exist
        if not os.path.exists(path):
            print('Making directory: ' + path)
            os.makedirs(path)
        # write fields to file names reportObject.txt in the directory
        f = open(f"reports/{self.coursecode}/{self.reportName}/reportObject.txt", "w")
        f.write(f"{self.status}\n{self.urlOfRawReport}\n{self.urlOfScrappedReport}")
        f.close()

    # getter for all job information
    def getJob(self):
        if self.status == Report.PROCCESSING:
            return '{"name":"' + self.reportName + '","status":"' + "Processing" + '","submissionDate":"' + "10/20/2000" + '"}'
        elif self.status == Report.COMPLETE:
            return '{"name":"' + self.reportName + '","status":"' + "Complete" + '","submissionDate":"' + "10/20/2000" + '"}'
        else:
            return '{"name":"' + self.reportName + '","status":"' + "Failed" + '","submissionDate":"' + "10/20/2000" + '"}'

    # delete the report persistent storage
    def delete(self):
        os.remove(f"reports/{self.coursecode}/{self.reportName}.txt")

    # read the object file to update values of object
    def refresh(self):
        file = open("reports/" + self.coursecode + "/" + self.reportName + "/reportObject.txt", "w")
        s = file.readline().strip()
        r = file.readline().strip()
        sc = file.readline().strip()
        self.status = int(s)
        self.urlOfRawReport = r
        self.urlOfScrappedReport = sc
