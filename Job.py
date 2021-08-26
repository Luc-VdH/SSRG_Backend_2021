from ReportScraper import ReportScraper
import subprocess
from urllib import request
import json

from time import sleep


class Job:
    
    def __init__(self, files, reportName, username, flag):
        self.files = " ".join(files)
        self.reportName = reportName
        self.username = username
        self.flag = flag

        self.reportScraper = ReportScraper()
        self.urlOfRawReport = ''

    # Job.reportDAO.addReport(reportName, username)
    # self.report = Job.reportDAO.getReport(reportName, username)

    def start(self):
        print('Started Job: ' + self.reportName)
        self.uploadFilesToMoss()
        self.scrapeReport()
        self.updateReportDAO()
        self.emailJobComplete()
        print('Finished Job: ' + self.reportName)

    def uploadFilesToMoss(self):
        print('Files Uploading')
        cmd = f"./moss -l {self.flag} {self.files}"
        # output = subprocess.getoutput(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        word = out.decode("utf-8")
        print(word)
        url = "http"+(word.split("http")[-1])
        #word = str(out)
        #all = word.split("\"")[-2]
        #url = all.split("http")[-1]
        #url = "http" + url
        #url = url[:-2]
        print(url)
        self.urlOfRawReport = url
        if self.urlOfRawReport == '' or self.urlOfRawReport[0:4] != "http":
            # self.report.jobFailed()
            print(f'Job Failed: {self.urlOfRawReport}')
            self.urlOfRawReport = ''
        # TODO Handle
        else:
            print('Received Moss Response\nURL set to ' + self.urlOfRawReport)

    def emailJobComplete(self):
        # TODO
        print('Job Complete (email)')

    def scrapeReport(self):
        # self.reportScraper.scrapeReport(self.urlOfRawReport,f"reports/{self.coursecode}/{self.reportName}/")
        print("SCRAPE")

    def updateReportDAO(self):
        # self.report.addRawURL(self.urlOfRawReport)
        # file = open("reports/" + self.username + "/" + self.reportName + "/reportObject.txt", "w")
        # file.write("1\n" + self.urlOfRawReport + "\n" + "")
        # file.close()
        
        user = subprocess.check_output("whoami", shell=True).decode("utf-8")
        if (user.strip() == "ubuntu"):
            host="172.31.24.225:8080"
        else:
            host = "0.0.0.0:8000"
        
        url = f"http://{host}/updatereport"
        print(url)
        req = request.Request(url, method="POST")
        req.add_header('Content-Type', 'application/json')
        data = {
            "id": "BackendSSRG1",
            "reportName": self.reportName,
            "coursecode": self.username,
            "status": 1,
            "rawurl": self.urlOfRawReport
        }
        data = json.dumps(data)
        data = data.encode()
        r = request.urlopen(req, data=data)
        content = r.read()
        print(content)
        print(f'Updated ReportDAO. \nUrlOfRawReport set to:{self.urlOfRawReport}')
    # TODO
