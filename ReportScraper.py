import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
from Match import Match
from webdriver_manager.chrome import ChromeDriverManager

# class for scraping moss for report information / html files
class ReportScraper:
    def __init__(self, url):
        self.urlOfRawReport = url
        print("setting driver...")
        opts = webdriver.ChromeOptions()
        opts.headless =True
        #self.__driver = webdriver.Chrome(ChromeDriverManager().install())
        self.__driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=opts)#self.__driver = webdriver.Firefox()
        self.__matches = []

    def scrapeReport(self):
        # self.urlOfRawReport = urlOfRawReport
        # if self.urlOfRawReport != '':
        #     print('Report Scraped')
        # urllib.request.urlretrieve(urlOfRawReport, path + "rawReport.html")

        print("getting webpage...")
        self.__driver.get(self.urlOfRawReport)

        print("getting content...")
        content = self.__driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        print("scraping index...")

        s = soup.findAll('a', href=True)
        for a in range(0, len(s) - 1):
            index = s[a].text.find("%")
            if index != -1:
                href = s[a]['href']
                file1 = s[a].text[:-6]
                file2 = s[a + 1].text[:-6]
                percent = s[a].text[-4:-1]
                a += 2
                print("scraping match...")
                lines = self.scrapeMatch(href)
                print("creating match...")
                m = Match(file1, file2, percent)
                for i in range(0, len(lines[0])):
                    m.addLines(lines[0][i], lines[1][i])

                self.__matches.append(m)

        print("done.")

    def scrapeMatch(self, url):

        print("\tgetting webpage...")
        self.__driver.get(url)

        print("\tgetting content...")
        content = self.__driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        frame0 = soup.find('frame', attrs={'name': '0'})
        frame1 = soup.find('frame', attrs={'name': '1'})
        lines = [[], []]

        print("\tscraping lines...")
        self.__driver.get(self.urlOfRawReport + "/" + frame0['src'])
        content = self.__driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for f in soup.findAll('font'):
            lines[0].append(f.text)

        self.__driver.get(self.urlOfRawReport + "/" + frame1['src'])
        content = self.__driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for f in soup.findAll('font'):
            lines[1].append(f.text)

        return lines

    def toString(self):
        out = '{"matches": ['
        for m in self.__matches:
            out += m.toString() + ", "
        out = out[:-2]
        out += ']}'
        return out


if __name__ == "__main__":
    rs = ReportScraper("http://moss.stanford.edu/results/7/3579624107546/")
    # rs = ReportScraper("http://moss.stanford.edu/results/2/4286344033639")
    rs.scrapeReport()
    print(rs.toString())
