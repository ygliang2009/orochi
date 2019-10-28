#!/usr/bin/python
#encoding=utf8

import os
import time
import configparser as cp
import logging
import logging.config
import pyredis
import asyncio
import websockets
import json


class MonitorServer:

    def __init__(self, logger, configger):
        self.__logger = logger
        self.__config = configger
        self.__dbAddr = False
        self.__dbPort = False
        self.__monitorInterval = False
        self.__monitorClient = False
        self.__cleanThreshold = False
        self.__monitorSplitter = False
        self.__signalServerAddr = False
        self.__signalServerPort = False

    def initialize(self):
        self.__dbAddr = self.__config.get("monitor", "monitorServerAddr")
        self.__dbPort = int(self.__config.get("monitor", "monitorServerPort"))
        self.__monitorInterval = int(self.__config.get("monitor","monitorInterval"))
        self.__monitorClient = pyredis.Client(host = self.__dbAddr, port = self.__dbPort)
        self.__cleanThreshold = int(self.__config.get("monitor","cleanThreshold"))
        self.__monitorSplitter = self.__config.get("monitor","monitorSplitter") 
        self.__signalServerAddr = self.__config.get("signal", "signalServerLocalAddr")
        self.__signalServerPort = int(self.__config.get("signal", "signalServerPort"))

    def work(self):
        asyncio.get_event_loop().run_until_complete(self.__checkValidUser())

    async def __checkValidUser(self):
        #try:
        #waiting for Worker to start
        time.sleep(1)
        async with websockets.\
            connect('ws://' + self.__signalServerAddr + ":" + str(self.__signalServerPort))\
                as websocket:
            while True:
                time.sleep(self.__cleanThreshold)
                self.__logger.debug("begin monitor get valid roomlist oper")
                validUser = {}
                userlist = self.__monitorClient.keys("chatroom" + self.__monitorSplitter + "*")       
                for user in userlist:
                    user = user.decode('utf8')
                    triple = user.split(self.__monitorSplitter)  
                    if len(triple) != 3:
                        self.__logger.warning("Invalid userinfo in monitor {}".format(user))
                        continue
                    roomid = triple[1] 
                    userid = triple[2]
                    if not roomid in validUser:
                        validUser[roomid] = set([])     
                    validUser[roomid].add(userid)
                    self.__logger.debug("monitor get valid room " + roomid + " , user "  + userid)
                
                validUserList = {}
                for roomId, userSet in list(validUser.items()):
                     validUserList[roomId] = [n for n in userSet]

                request_dict = {}
                request_dict['type'] = 15
                request_dict['id'] = '-1'
                request_dict['msg'] = validUserList
                await websocket.send(json.dumps(request_dict))
                recv_msg = await websocket.recv()
                self.__logger.debug("server process message 15 result = {} ".format(json.dumps(recv_msg)))
                #self.__logger.info("monitor send websocket error, for reason = " + str(e))
        #except Exception as e:
        #    self.__logger.warning("server process job error, msg = {}".format(str(e)))

        #finally:
        self.__monitorClient.close()

if __name__ == "__main__":
    cf = cp.ConfigParser()
    cf.read("conf/Signal.conf")
    logging.config.fileConfig(cf.get("global","logConf"))
    logger = logging.getLogger("signal")
    ms = MonitorServer(logger, cf)
    ms.initialize()
    ms.work()
