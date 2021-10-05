
import requests
from bs4 import BeautifulSoup

from Match import Match


try:
    from Match import Match
except:
    from src.Match import Match

# class for scraping moss for report information / html files
class ReportScraper:
    # constructor function
    def __init__(self, url):
        # set the url and declare an empty array of matches
        self.urlOfRawReport = url
        self.__matches = []

    def scrapeReport(self):
        # get the main webpage of the report
        print("getting webpage...")
        r = requests.get(self.urlOfRawReport)

        # get the content of the main webpage
        print("getting content...")
        content = r.content
        # pass the content to an html parser
        soup = BeautifulSoup(content, features="html.parser")
        # scrape the base info for each match from index.html
        print("scraping index...")
        # find all the <a> tags containing links to the individual matches
        s = soup.findAll('a', href=True)
        # loop through all the elements
        for a in range(0, len(s) - 1, 2):
            # check if the text contains a %, if it does it links to a match
            index = s[a].text.find("%")
            if index != -1:
                # get the link to the match
                href = s[a]['href']
                # extract the 2 file names and the match percentage from the element
                file1 = s[a].text.split('(')[0][:-2]
                file2 = s[a+1].text.split('(')[0][:-2]
                percent = s[a].text.split("(")[-1][:-1]
                # pass the link to scrape match function to get the individual blocks of matching code and the whole file
                print("scraping match...")
                lines = self.scrapeMatch(href)
                print("creating match...")
                # create a new match object and add the scraped lines of code
                m = Match(file1, file2, percent)
                m.addLines(lines)

                # append the new object to the array of matches
                self.__matches.append(m)

        print("done.")

    def scrapeMatch(self, url):
        # get the match webpage
        print("\tgetting webpage...")
        r = requests.get(url)

        # get the html content of the match webpage
        print("\tgetting content...")
        content = r.content
        soup = BeautifulSoup(content, features="html.parser")
        # the page is divided into 3 regions, each on is a frame, get all 3 frame elements
        frameTop = soup.find('frame', attrs={'name': 'top'})
        frame0 = soup.find('frame', attrs={'name': '0'})
        frame1 = soup.find('frame', attrs={'name': '1'})
        lines = [[], []]

        # use the top frame to scrape the number of matches (line count)
        print("\tscrapeing line count...")
        r = requests.get(self.urlOfRawReport + "/" + frameTop['src'])
        content = r.content
        soup = BeautifulSoup(content, features="html.parser")
        names = []
        # there are <a> elements containing links and IDs for each match, get all those details and store them in the
        # names array
        for a in soup.findAll('a'):
            # TODO get line numbers for each block
            name = a['name']
            if name not in names:
                names.append(name)
        # the last element contains the largest ID value, store this value in blocks
        blocks = eval(names[-1])
        # loop in range from 0 to blocks, appending to the lines arrays, building them as arrays of length max ID
        for i in range(0, blocks + 1):
            lines[0].append("")
            lines[1].append("")

        # scrape the lines of code from each matching file
        print("\tscraping lines...")
        r = requests.get(self.urlOfRawReport + "/" + frame0['src'])
        content = r.content
        soup = BeautifulSoup(content, features="html.parser")
        # get the text of the whole file (matches included)
        code0 = soup.find('pre').text
        # each matching block is stored in a font element, find all these elements and add their content to the lines array in the position of their ID
        for f in soup.findAll('font'):
            # inside each font element is an <a> element containing a link that contains the id of the match
            a = f.find('a')
            h = a['href']
            block = eval(h.split('#')[-1])
            lines[0][block] += f.text

        # go through each match and remove its text from the overall file
        for i in range(len(lines[0])):
            if lines[0][i] != '':
                # replace it with the match ID separated by a the symbols ` and §
                code0 = code0.replace(lines[0][i], "`" + str(i) + "§")

        # split the code on § to isolate the blocks of non-matching code
        codearr0 = code0.split("§")
        # empty array to be filled with dictionaries, this will be turned in JSON later
        line1 = []
        # loop through each non-match block
        for i in range(len(codearr0) - 1):
            chunk = codearr0[i].split('`')
            # remove the ID and the ` and build up the array of dictionaries with the non-match block and the match
            line1.append({"matchFlag": "none", "line": chunk[0]})
            if len(chunk) > 0:
                line1.append({"matchFlag": eval(chunk[1]), "line": lines[0][eval(chunk[1])]})
        line1.append({"matchFlag": "none", "line": codearr0[-1]})

        r = requests.get(self.urlOfRawReport + "/" + frame1['src'])
        content = r.content
        soup = BeautifulSoup(content, features="html.parser")
        # get the text of the whole file (matches included)
        code1 = soup.find('pre').text
        # each matching block is stored in a font element, find all these elements and add their content to the lines array in the position of their ID
        for f in soup.findAll('font'):
            # inside each font element is an <a> element containing a link that contains the id of the match
            a = f.find('a')
            h = a['href']
            block = eval(h.split('#')[-1])
            # TODO identify if 2 sets of lines belong to the same block
            lines[1][block] += f.text

        # go through each match and remove its text from the overall file
        for i in range(len(lines[1])):
            if lines[1][i] != '':
                # replace it with the match ID separated by a the symbols ` and §
                code1 = code1.replace(lines[1][i], "`" + str(i) + "§")

        # split the code on § to isolate the blocks of non-matching code
        codearr1 = code1.split("§")
        # empty array to be filled with dictionaries, this will be turned in JSON later
        line2 = []
        # loop through each non-match block
        for i in range(len(codearr1) - 1):
            chunk = codearr1[i].split('`')
            # remove the ID and the ` and build up the array of dictionaries with the non-match block and the match
            line2.append({"matchFlag": "none", "line": chunk[0]})
            if len(chunk) > 0:
                line2.append({"matchFlag": eval(chunk[1]), "line": lines[1][eval(chunk[1])]})
        line2.append({"matchFlag": "none", "line": codearr1[-1]})

        # return a 2D array of dictionaries
        out = [line1, line2]
        return out

    def toString(self):
        # build a JSON string containing an array of the output from each match
        if self.__matches != []:
            out = '"matches": ['
            for m in self.__matches:
                out += m.toString() + ", "
            out = out[:-2]
            out += ']'
        else:
            out = '"matches": "no matches"'
        return out


if __name__ == "__main__":
    rs = ReportScraper("http://moss.stanford.edu/results/9/5151095819632/")
    rs.scrapeReport()
    print(rs.toString())
