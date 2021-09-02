class User:
    # object properties
    __username = "blank"
    __password = "none"
    __mossid = "none"
    __email = []

    # constructor function, creates a user object with username password and mossid
    def __init__(self, username, password, mossid):
        self.__username = username
        self.__password = password
        self.__mossid = mossid
        self.__email = []

    # getters
    def getPassword(self):
        return self.__password

    def getMossid(self):
        return self.__mossid

    def getCoursecode(self):
        return self.__username

    def getEmails(self):
        return self.__email

    # setters
    def setPassword(self, password):
        self.__password = password

    def setCoursecode(self, coursecode):
        self.__username = coursecode

    def setMossid(self, mossid):
        self.__mossid = mossid

    def addEmail(self, email):
        self.__email.append(email)

    def clearEmails(self):
        self.__email = []
    # write information to user text file for persistent storage
    def save(self):
        file = open("usrs/" + self.__username + ".txt", "w")
        file.write(self.__password + "\n" + self.__mossid + "\n")
        for e in self.__email:
            file.write(e + "#")
        file.write("\n")
        file.close()
