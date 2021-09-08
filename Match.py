class Match:
    def __init__(self, file1, file2, percent):
        self.__file1 = file1
        self.__file2 = file2
        self.__percent = percent
        self.__lines = [[]]

    def addLines(self, line1, line2):
        self.__lines.append([line1, line2])
        if [] in self.__lines:
            self.__lines.remove([])

    def toString(self):
        out = '{"files": ["' + self.__file1 + '", "' + self.__file2 + '"],'
        out += '"percent": "' + self.__percent + '", "lines": ['
        for line in self.__lines:
            out += '["'
            out += line[0].replace('\n', '\\n').replace('"', '\"') + '", "' + line[1].replace('\n', '\\n').replace('"', '\"')
            out += '"], '
        out = out[:-2]
        out += ']}'

        return out


if __name__ == "__main__":
    m = Match("file1", "file2", "20%")
    m.addLines("line00", "line01")
    m.addLines("line10", "line11")
    m.addLines("line20", "line21")
    print(m.toString())
