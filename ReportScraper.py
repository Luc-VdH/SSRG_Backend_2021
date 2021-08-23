class ReportScraper:
	def __init__(self):
		self.urlOfRawReport = ''
	
	def scrapeReport(self, urlOfRawReport):
	    self.urlOfRawReport = urlOfRawReport
	    if self.urlOfRawReport != '':
		    print('Report Scraped')
