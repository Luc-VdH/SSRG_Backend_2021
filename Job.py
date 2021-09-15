from ReportScraper import ReportScraper
import subprocess
from urllib import request
import json
import ssl
import certifi

from time import sleep


# class for running the moss script in parallel
class Job:

    # constructor
    def __init__(self, files, reportName, username, flag, email, mossID):
        self.files = files
        self.reportName = reportName
        self.username = username
        self.flag = flag
        self.email = email
        self.mossID = mossID

        self.urlOfRawReport = ''
        self.scrapedData = ''
        self.status = 1
        self.retry = 1

    # start the job, this is called and run in celery
    def start(self):
        print('Started Job: ' + self.reportName)
        # make calls to helper functions
        self.uploadFilesToMoss()
        if self.status != -1:
            self.scrapeReport()
        self.updateReportDAO()
        if self.email:
            self.emailJobComplete()
        print('Finished Job: ' + self.reportName)

    # runs the moss script
    def uploadFilesToMoss(self):
        attempt = str(11-self.retry)
        print('Files Uploading: '+self.files+"\nAttempt"+attempt)
        # build run command string
        try:
            cmd = f"./moss -l {self.flag} -d {self.files}/*/*"
        except:
            print("Moss Upload Failed")
            self.status = -1
        # run the command
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # wait for it to finish
        p.wait()
        # get the output from the script
        out, err = p.communicate()
        word = out.decode("utf-8")
        print(word)
        # extract the url from the output
        url = "http" + (word.split("http")[-1])
        print(url)
        # save the url
        self.urlOfRawReport = url.strip()
        # check if the job has failed
        if self.urlOfRawReport == '' or self.urlOfRawReport[0:7] != "http://":
            # self.report.jobFailed()
            print(f'Job Failed: {self.urlOfRawReport}')
            self.urlOfRawReport = word
            self.status = -1
            #reduce retries amount available
            self.retry -= 1
            #if there havent been 10 retries, try again
            if self.retry > 0:
                #retry every hour
                sleep(3600)
                self.uploadFilesToMoss()
        # TODO Handle
        else:
            print('Received Moss Response\nURL set to ' + self.urlOfRawReport)

    # scrape the report from moss
    def scrapeReport(self):
        rs = ReportScraper(self.urlOfRawReport)
        rs.scrapeReport()
        self.scrapedData = rs.toString()
        print("SCRAPE")

    # send a request to app to update the report
    def updateReportDAO(self):
        # check if running on EC2 or locally to determine IP and Port
        user = subprocess.check_output("whoami", shell=True).decode("utf-8")
        if user.strip() == "ubuntu":
            host = "172.31.24.225:8080"
        else:
            host = "0.0.0.0:8000"

        # build a request url
        url = f"https://{host}/updatereport"
        print(url)
        # build the request
        req = request.Request(url, method="POST")
        req.add_header('Content-Type', 'application/json')
        data = {
            "id": "BackendSSRG1",
            "reportName": self.reportName.replace('"', ''),
            "coursecode": self.username,
            "status": self.status,
            "rawurl": self.urlOfRawReport,
            "scraped": self.scrapedData
        }
        data = json.dumps(data)
        data = data.encode()
        # send the request
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.verify_mode = ssl.CERT_NONE
        context.check_hostname = False
        # context.load_verify_locations(cafile=certifi.where())
        # r = request.urlopen(req, data=data, context=ssl.create_default_context(cafile=certifi.where()))
        r = request.urlopen(req, data=data, context=context)

        content = r.read()
        print(content)
        print(f'Updated ReportDAO. \nUrlOfRawReport set to:{self.urlOfRawReport}')
        
    # send a request to app to send the conformation email
    def emailJobComplete(self):
        # check if running on EC2 or locally to determine IP and Port
        user = subprocess.check_output("whoami", shell=True).decode("utf-8")
        if user.strip() == "ubuntu":
            host = "172.31.24.225:8080"
        else:
            host = "0.0.0.0:8000"

        # build a request url
        url = f"https://{host}/sendemails"
        
        # build the request
        req = request.Request(url, method="POST")
        req.add_header('Content-Type', 'application/json')
        data = {
            "id": "BackendSSRG1",
            "reportName": self.reportName.replace('"', ''),
            "coursecode": self.username,
            "status": self.status,
        }
        data = json.dumps(data)
        data = data.encode()
        # send the request
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.verify_mode = ssl.CERT_NONE
        context.check_hostname = False
        # context.load_verify_locations(cafile=certifi.where())
        # r = request.urlopen(req, data=data, context=ssl.create_default_context(cafile=certifi.where()))
        r = request.urlopen(req, data=data, context=context)
        content = r.read()
        print(content)
        print(f'Sending Emails.')
