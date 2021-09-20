import os.path
import os
import subprocess

location = subprocess.check_output("pwd", shell=True).decode("utf-8")
if "ssrg_backend/test" in location:
    from src.User import User
else:
    from User import User


# class for managing user objects
class UserDAO:
    __users = []

    # empty constructor
    def __init__(self):
        pass

    # add a new user to the list of users and instruct the object to save its information to a text file
    def addUser(self, coursecode, password, mossid):
        user = User(coursecode, password, mossid)
        user.save()
        self.__users.append(user)

    # sign in method for checking passwords
    def signIn(self, coursecode, password):
        # get the user object from the array
        index = self.getUserIndex(coursecode)
        # check if the provided password matches the one stored in the user obejct
        if password == self.__users[index].getPassword():
            return 1
        else:
            return 0

    def getUserEmail(self, coursecode):
        index = self.getUserIndex(coursecode)
        if index != -1:
            return self.__users[index].getEmails()
        else:
            return "not found"

    def addUserEmail(self, coursecode, email):
        index = self.getUserIndex(coursecode)
        if index != -1:
            self.__users[index].addEmail(email)
            self.__users[index].save()
            return "success"
        else:
            return "not found"

    def removeUserEmail(self, coursecode, email):
        index = self.getUserIndex(coursecode)
        if index != -1:
            self.__users[index].removeEmail(email)
            self.__users[index].save()
            return "success"
        else:
            return "not found"

    def getUserMossid(self, coursecode):
        index = self.getUserIndex(coursecode)
        if index != -1:
            return self.__users[index].getMossid()
        else:
            return "not found"

    def deleteUser(self, coursecode, password):
        index = self.getUserIndex(coursecode)
        if self.signIn(coursecode, password):
            os.system("rm usrs/" + coursecode + ".txt")
            self.__users.pop(index)
            return 1
        else:
            return 0

    # TODO update user info
    def updateUserInfo(self, coursecode, password, mossid):
        index = self.getUserIndex(coursecode)
        if index != -1:
            self.__users[index].setPassword(password)
            self.__users[index].setMossid(mossid)
            self.__users[index].save()
            return 1
        else:
            return 0

    # function for checking if a user exists
    def userExists(self, coursecode):
        # first check if the text file for the user exists
        exists = os.path.isfile("usrs/" + coursecode + ".txt")
        # if the file exists, make sure that it has a corresponding object in the list
        if exists:
            index = self.getUserIndex(coursecode)
            if index == -1:
                # open the file
                file = open("usrs/" + coursecode + ".txt", "r")
                # read the data from the file
                password = file.readline().strip()
                mossid = file.readline().strip()
                # build a new user object using that data
                user = User(coursecode, password, mossid)
                e = file.readline().strip()
                emails = e.split("#")
                for i in emails:
                    if i != '':
                        user.addEmail(i)

                file.close()
                # add the object the list
                self.__users.append(user)
        # return true if the user exists
        return exists

    # function for finding the index of the user in the list
    def getUserIndex(self, coursecode):
        # set to -1, will be returned if the object is not found
        index = -1
        count = 0
        # loop through the users checking for the object with the matching coursecode
        for user in self.__users:
            if user.getCoursecode() == coursecode:
                index = count
            count += 1
        return index
