import json


# object to hold the information for a pair of matching files
class Match:
    def __init__(self, file1, file2, percent):
        # store the 2 file names and percentage matching
        self.__file1 = file1
        self.__file2 = file2
        self.__percent = percent
        # empty 2D array for the matching lines
        self.__lines = [[]]

    def addLines(self, lines):
        # add the lines to the object
        self.__lines = lines

    def toString(self):
        # build a dictionary with the information from the object
        outdict = {"files": [self.__file1, self.__file2], "percent": self.__percent, "lines": self.__lines}

        # turn the dictionary into a json string to be sent to the server
        return json.dumps(outdict)


if __name__ == "__main__":
    m = Match("file1", "file2", "20%")
    print(m.toString())
    lines = [["line1", "line2"], ["line3", "line4"]]
    m.addLines(lines)
    print(m.toString())
