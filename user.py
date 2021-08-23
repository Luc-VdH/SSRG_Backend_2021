class User:
    __username = "blank"
    __password = "none"
    __mossid = "none"

    def __init__(self, username):
        self.__username = username
        file = open("usrs/" + username + ".txt", "r")
        __password = file.readline()
        __mossid = file.readline()

    def getPassword(self):
        return self.__password

    def getMossid(self):
        return self.__mossid

    def save(self):
        file = open("usrs/" + self.__username + ".txt", "w")
        file.write(self.__password + "\n" + self.__mossid + "\n")
