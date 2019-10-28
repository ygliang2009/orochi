class User:
    def __init__(self):
        self.__role = False
        self.__id = False
        self.__sock = False
        self.__room = False
        self.__msgBuffer = {}
        self.__alias = False
    
    def __del__(self):
        self.__sock.close()

    def getAlias(self):
        return self.__alias

    def setAlias(self, alias):
        self.__alias = alias

    def getRole(self):
        return self.__role

    def setRole(self, role):
        self.__role = role

    def getId(self):
        return self.__id

    def setId(self, idvar):
        self.__id = idvar

    def setSock(self, sock):
        self.__sock = sock
        
    def getSock(self):
        return self.__sock

    def getRoom(self):
        return self.__room

    def setRoom(self, room):
        self.__room = room

    def getMsgById(self, msgid):
        if msgid in self.__msgBuffer:
            return self.__msgBuffer[msgid]
        return None

    def getMsgBuffer(self):
        return self.__msgBuffer

    def setMsgBuffer(self, msgBuffer):
        self.__msgBuffer = msgBuffer

    def appendMsg(self, msgid, msg):
        self.__msgBuffer[msgid] = msg

