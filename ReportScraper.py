import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup


# class for scraping moss for report information / html files
class ReportScraper:
    def __init__(self):
        self.urlOfRawReport = ''

    def scrapeReport(self):
        # self.urlOfRawReport = urlOfRawReport
        # if self.urlOfRawReport != '':
        #     print('Report Scraped')
        # urllib.request.urlretrieve(urlOfRawReport, path + "rawReport.html")
        matches = []
        print("setting driver...")
        driver = webdriver.Firefox()
        print("getting webpage...")
        driver.get("http://moss.stanford.edu/results/7/3579624107546/")

        print("getting content...")
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        print("scraping...")

        for a in soup.findAll('a', href=True):
            matches.append(a.text)
            print(a.text)
        print("done.")
        print(matches)


if __name__ == "__main__":
    rs = ReportScraper
    rs.scrapeReport(rs)

