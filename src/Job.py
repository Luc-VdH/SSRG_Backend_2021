import subprocess
from urllib import request
import json
import ssl
import certifi
import os

from time import sleep

try:
    from ReportScraper import ReportScraper
except:
    from src.ReportScraper import ReportScraper

# class for running the moss script in parallel
class Job:

    # constructor
    def __init__(self, files, base, reportName, username, flag, email, mossID):
        self.files = files
        self.reportName = reportName
        self.username = username
        self.flag = flag
        self.email = email
        self.mossID = mossID
        
        if base != []:
            self.base = "-b "+" -b ".join(base) + " "
            print(self.base)
        else:
            self.base = ''
            
        self.urlOfRawReport = ''
        self.scrapedData = ''
        self.status = 1
        self.retry = 1

    # start the job, this is called and run in celery
    def start(self):
        print('Started Job: ' + self.reportName)
        # make calls to helper functions
        self.uploadFilesToMoss()
        self.scrapeReport()
        self.updateReportDAO()
        self.emailJobComplete()
        print('Finished Job: ' + self.reportName)

    # runs the moss script
    def uploadFilesToMoss(self):
        #checks if the files were valid (done in the archiver class)
        if self.files[0:7]=="Invalid":
            self.urlOfRawReport = self.files
            print(f'Job Failed: {self.urlOfRawReport}')
            self.status = -1
            return False
        attempt = str(self.retry)
        print('Files Uploading: '+self.files+"\nAttempt: "+attempt)
        # build run command string
        mossdown = False
        try:
            #create moss command
            cmd = f"./moss -i {self.mossID} -l {self.flag} {self.base}-d {self.files}/*/*"
            print("Running Moss Script: "+cmd)
            # run the command
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            # wait for it to finish
            p.wait()
            # get the output from the script
            out, err = p.communicate()
            word = out.decode("utf-8")
            print(word)

            if "Connection refused" in word:
                mossdown = True
            # extract the url from the output
            url = "http" + (word.split("http")[-1])
            # save the url
            self.urlOfRawReport = url.strip()
        except:
            print("Moss Upload Failed")
            self.status = -1
            self.urlOfRawReport = "MOSS Upload Failed"
            return False
        # check if the job has failed
        if self.urlOfRawReport == '' or self.urlOfRawReport[0:7] != "http://":
            # self.report.jobFailed()
            print(f'Job Failed: {self.urlOfRawReport}')
            # self.urlOfRawReport = word
            if not mossdown:
                self.urlOfRawReport = "No URL returned, please check MOSS ID or files"
                self.retry = 11
            else:
                self.urlOfRawReport = "MOSS servers offline"
            self.status = -1
            #reduce retries amount available
            self.retry += 1
            #if there havent been 10 retries, try again
            if self.retry <= 10:
                print(self.retry <= 0, self.retry)
                print("retry")
                #retry every hour
                sleep(3600)
                self.uploadFilesToMoss()
            else:
                return False
        # TODO Handle
        else:
            print('Received Moss Response\nURL set to ' + self.urlOfRawReport)
            return True

    # scrape the report from moss
    def scrapeReport(self):
        if self.status == -1:
            return False
        rs = ReportScraper(self.urlOfRawReport)
        rs.scrapeReport()
        self.scrapedData = rs.toString()
        print("SCRAPED")
        return True

    # send a request to app to update the report
    def updateReportDAO(self):
        try:
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
            return True
        except:
            print("Updating ReportDAO failed")
            return False
        
    # send a request to app to send the conformation email
    def emailJobComplete(self):
        try:
            if False == self.email:
                return False
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
            return True
        except:
            print("Unable to send Email")
            return False
