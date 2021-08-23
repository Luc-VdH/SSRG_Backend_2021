from ReportScraper import ReportScraper
import subprocess

from time import sleep

class Job:
	def __init__(self, files, reportName, username, flag):
		self.files = " ".join(files)
		self.reportName = reportName
		self.username = username
		self.flag = flag
		
		self.reportScraper = ReportScraper()
		self.urlOfRawReport = ''
	
	def start(self):
		print('Started Job: ' + self.reportName)
		self.uploadFilesToMoss()
		self.scrapeReport()
		self.updateReportDAO()
		self.emailJobComplete()
		print('Finished Job: ' + self.reportName)
	
	def uploadFilesToMoss(self):
		print('Files Uploading')
		cmd = f"moss -l {self.flag} {self.files}"
		output = subprocess.getoutput(cmd)
		self.urlOfRawReport = output.split('\n')[-1]
		if self.urlOfRawReport == '' or self.urlOfRawReport[0:4] != "http":
		    print('Error')
		    #TODO Handle 
		else:
			print('Received Moss Response')
		
	def emailJobComplete(self):
	    #TODO
		print('Job Complete (email)')
	
	def scrapeReport(self):
		self.reportScraper.scrapeReport(self.urlOfRawReport)
	
	def updateReportDAO(self):
		print('updated ReportDAO')
		#TODO
		print(self.urlOfRawReport)

