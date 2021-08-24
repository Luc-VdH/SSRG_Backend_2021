class User:
    __username = "blank"
    __password = "none"
    __mossid = "none"

    def __init__(self, username, password, mossid):
        self.__username = username
        self.__password = password
        self.__mossid = username

    def getPassword(self):
        return self.__password

    def getMossid(self):
        return self.__mossid

    def getCoursecode(self):
        return self.__username

    def save(self):
        file = open("usrs/" + self.__username + ".txt", "w")
        file.write(self.__password + "\n" + self.__mossid + "\n")
