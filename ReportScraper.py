import urllib.request 

class ReportScraper:
	def __init__(self):
		self.urlOfRawReport = ''
	
	def scrapeReport(self, urlOfRawReport, path):
		self.urlOfRawReport = urlOfRawReport
		if self.urlOfRawReport != '':
		    print('Report Scraped')
		urllib.request.urlretrieve(urlOfRawReport, path+"rawReport.html")
