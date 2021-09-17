import urllib.request
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from src.Match import Match
from webdriver_manager.chrome import ChromeDriverManager

# class for scraping moss for report information / html files
class ReportScraper:
    def __init__(self, url):
        self.urlOfRawReport = url
        # print("setting driver...")
        # opts = webdriver.ChromeOptions()
        # opts.headless =True
        # #self.__driver = webdriver.Chrome(ChromeDriverManager().install())
        # self.__driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=opts)#self.__driver = webdriver.Firefox()
        # self.__driver = request.get()
        self.__matches = []

    def scrapeReport(self):
        # self.urlOfRawReport = urlOfRawReport
        # if self.urlOfRawReport != '':
        #     print('Report Scraped')
        # urllib.request.urlretrieve(urlOfRawReport, path + "rawReport.html")

        print("getting webpage...")
        # self.__driver.get(self.urlOfRawReport)
        r = requests.get(self.urlOfRawReport)

        print("getting content...")
        # content = self.__driver.page_source
        content = r.content
        soup = BeautifulSoup(content, features="html.parser")
        print("scraping index...")
        count = 0
        count_mismatch = 0

        s = soup.findAll('a', href=True)
        for a in range(0, len(s) - 1, 2):
            index = s[a].text.find("%")
            if index != -1:
                href = s[a]['href']
                file1 = s[a].text[:-6]
                file2 = s[a + 1].text[:-6]
                percent = s[a].text[-4:-1]
                # a += 2
                print("scraping match...")
                count += 1
                lines = self.scrapeMatch(href)
                print("creating match...")
                m = Match(file1, file2, percent)
                length = min(len(lines[0]), len(lines[1]))
                if len(lines[0]) != len(lines[1]):
                    count_mismatch += 1
                for i in range(0, length):
                    m.addLines(lines[0][i], lines[1][i])

                self.__matches.append(m)

        print("done.")
        print("of", count, "matches,", count_mismatch, "matches were misaligned")

    def scrapeMatch(self, url):

        print("\tgetting webpage...")
        # self.__driver.get(url)
        r = requests.get(url)

        print("\tgetting content...")
        # content = self.__driver.page_source
        content = r.content
        soup = BeautifulSoup(content, features="html.parser")
        frameTop = soup.find('frame', attrs={'name': 'top'})
        frame0 = soup.find('frame', attrs={'name': '0'})
        frame1 = soup.find('frame', attrs={'name': '1'})
        lines = [[], []]

        print("\tscrapeing line count...")
        # self.__driver.get(self.urlOfRawReport + "/" + frameTop['src'])
        # content = self.__driver.page_source
        r = requests.get(self.urlOfRawReport + "/" + frameTop['src'])
        content = r.content
        soup = BeautifulSoup(content, features="html.parser")
        names = []
        for a in soup.findAll('a'):
            # TODO get line numbers for each block
            name = a['name']
            if name not in names:
                names.append(name)
        blocks = eval(names[-1])
        for i in range(0, blocks+1):
            lines[0].append("")
            lines[1].append("")

        print("\tscraping lines...")
        # self.__driver.get(self.urlOfRawReport + "/" + frame0['src'])
        # content = self.__driver.page_source
        r = requests.get(self.urlOfRawReport + "/" + frame0['src'])
        content = r.content
        soup = BeautifulSoup(content, features="html.parser")
        for f in soup.findAll('font'):
            a = f.find('a')
            h = a['href']
            # TODO what about 2 digit blocks !? split on #
            # block = eval(h[-1:])
            block = eval(h.split('#')[-1])
            # TODO identify if 2 sets of lines belong to the same block
            lines[0][block] += f.text

        # self.__driver.get(self.urlOfRawReport + "/" + frame1['src'])
        # content = self.__driver.page_source
        r = requests.get(self.urlOfRawReport + "/" + frame1['src'])
        content = r.content
        soup = BeautifulSoup(content, features="html.parser")
        for f in soup.findAll('font'):
            a = f.find('a')
            h = a['href']
            block = eval(h[-1:])
            # TODO identify if 2 sets of lines belong to the same block
            lines[1][block] += f.text

        return lines

    def toString(self):
        out = '"matches": ['
        for m in self.__matches:
            out += m.toString() + ", "
        out = out[:-2]
        out += ']'
        return out


if __name__ == "__main__":
    # rs = ReportScraper("http://moss.stanford.edu/results/7/3579624107546/")
    # rs = ReportScraper("http://moss.stanford.edu/results/2/4286344033639")
    # rs = ReportScraper("http://moss.stanford.edu/results/7/9634195485591")

    rs = ReportScraper(" http://moss.stanford.edu/results/3/4277668591562")
    rs.scrapeReport()
    print(rs.toString())
