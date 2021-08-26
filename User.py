class User:
    # object properties
    __username = "blank"
    __password = "none"
    __mossid = "none"

    # constructor function, creates a user object with username password and mossid
    def __init__(self, username, password, mossid):
        self.__username = username
        self.__password = password
        self.__mossid = mossid

    # getters
    def getPassword(self):
        return self.__password

    def getMossid(self):
        return self.__mossid

    def getCoursecode(self):
        return self.__username

    # write information to user text file for persistent storage
    def save(self):
        file = open("usrs/" + self.__username + ".txt", "w")
        file.write(self.__password + "\n" + self.__mossid + "\n")
