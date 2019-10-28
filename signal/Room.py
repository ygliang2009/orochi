#!/usr/bin/python
import time

class Room:
    def __init__(self):
        self.__roomId = False
        self.__userBuffer = {}
        self.__createTime = False
   
    def _setRoomId(self, roomid):
        self.__roomId = roomid

    def getRoomId(self):
        return self.__roomId

    def setUserBuffer(self, userBuffer):
        self.__userBuffer = userBuffer

    def getUserBuffer(self):
        return self.__userBuffer

    def addUser(self, userid, user):
        self.__userBuffer[userid] = user

    def getUserById(self, userid):
        return self.__userBuffer.get(userid)

    def deleteUserById(self, userid):
        del(self.__userBuffer[userid])

    def createRoom(self, creator):
        #capsulate message
        self.__roomId =  creator.getId() + "_" + str(time.time())
        self.addUser(creator.getId(), creator)
        creator.setRoom(self)
        return self.__roomId
