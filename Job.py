from ReportScraper import ReportScraper
import subprocess   


from time import sleep

class Job:
	
	reportDAO = None
	
	def __init__(self, files, reportName, username, flag):
		self.files = " ".join(files)
		self.reportName = reportName
		self.username = username
		self.flag = flag
		
		self.reportScraper = ReportScraper()
		self.urlOfRawReport = ''
		
		
		#Job.reportDAO.addReport(reportName, username)
		#self.report = Job.reportDAO.getReport(reportName, username)
	
	def setReportDAO(reportDAO):
		Job.reportDAO = reportDAO
		
	
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
			#self.report.jobFailed()
			print(f'Job Failed: {self.urlOfRawReport}')
		    #TODO Handle 
		else:
			print('Received Moss Response')
		
	def emailJobComplete(self):
	    #TODO
		print('Job Complete (email)')
	
	def scrapeReport(self):
		#self.reportScraper.scrapeReport(self.urlOfRawReport,f"reports/{self.coursecode}/{self.reportName}/")
		print("SCRAPE")
	
	def updateReportDAO(self):
		#self.report.addRawURL(self.urlOfRawReport)
		file = open("reports/" + self.username + "/" + self.reportName + "/reportObject.txt", "w")
		file.write("1\n" + self.urlOfRawReport + "\n" + "")
		file.close()
		print(f'Updated ReportDAO. \nUrlOfRawReport set to:{self.urlOfRawReport}')
		#TODO

