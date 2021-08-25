from Report import Report

class ReportDAO:
	def __init__(self):
		self.reports = []
		self.initReports()

	def initReports(self):
		#TODO
		print("Initilising all reports")
        
	def addReport(self, name, coursecode):
		self.reports.append(Report(name, coursecode))
        
	def getReportIndex(self, name, coursecode):
		count = 0
		for r in self.reports:
			if r.isReport(name, coursecode):
				return count
			count += 1
		return -1
      
	def getReportStatus(self, name, coursecode):
		index = getReportIndex(name, coursecode)
		if index==-1:
			return -10
		return reports[index].checkStatus()
    
	def getReport(self, name, coursecode):
		index = getReportIndex(name, coursecode)
		if index==-1:
			return -10
		return reports[index].getRawReport()#TODO: scraped
    	
	def deleteReport(self, name, coursecode):
		index = getReportIndex(name, coursecode)
		if index==-1:
			return False
		reports.pop(index).delete()
		return True
    
	def getAllJobs(self):
		return [x.getJob() for x in reports]
