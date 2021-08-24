from User import User
import os.path


class UserDAO:
    __users = []

    def __init__(self):
        pass

    def addUser(self, coursecode, password, mossid):
        user = User(coursecode, password, mossid)
        user.save()
        self.__users.append(user)

    def signIn(self, coursecode, password):
        index = self.getUserIndex(coursecode)
        pw = self.__users[index].getPassword()
        if password == self.__users[index].getPassword():
            return 1
        else:
            return 0

    def deleteUser(self):
        pass

    def updateUserInfo(self):
        pass

    def userExists(self, coursecode):
        exists = os.path.isfile("usrs/" + coursecode + ".txt")
        if exists:
            index = self.getUserIndex(coursecode)
            if index == -1:
                file = open("usrs/" + coursecode + ".txt")
                password = file.readline().strip()
                mossid = file.readline().strip()
                file.close()
                user = User(coursecode, password, mossid)
                self.__users.append(user)
        return exists

    def getUserIndex(self, coursecode):
        index = -1
        count = 0
        for user in self.__users:
            if user.getCoursecode() == coursecode:
                index = count
            count += 1
        return index
