#!/usr/bin/python
#encoding=utf8

class Message:
    def __init__(self):
        self.__messageId = False
        self.__payLoad = False
        self.__sender = False
        self.__msgRoom = False
        self.__bornTime = False

    def setPayLoad(self, payload):
        self.__payLoad = payload

    def getPayLoad(self):
        return self.__payLoad
