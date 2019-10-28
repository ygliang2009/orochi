#!/usr/bin/python
#encoding=utf8

import asyncio
import websockets
import json
import WhiteList as wl
import Room
import User
import os

class SignalServer:
  
    def __init__(self, logger, configger):
        self.__logger = logger
        self.__config = configger
        self.__serveAddr = False
        self.__servePort = False
        self.__serveProtocol = False
        self.__sockPool = {}
        self.__roomBuffer = {}
        self.__userTTL = False

    def initialize(self):
        self.__serveProtocol = self.__config.get("signal","signalServerPrefix")
        self.__serveAddr = self.__config.get("signal","signalServerAddr")
        self.__servePort = int(self.__config.get("signal","signalServerPort"))
        self.__userTTL = int(self.__config.get("monitor","userTTL"))

    def work(self):
        fullPath = self.__joinFullPath()
        self.__logger.debug("serving address = %s"%(fullPath))
        self.startWork(self.__serveAddr, self.__servePort)

    def __joinFullPath(self):
        return self.__serveProtocol + "://" + self.__serveAddr + "/"

    def startWork(self, serveAddr, servePort):
        start_server = websockets.serve(self.procMessage, serveAddr, servePort)
        asyncio.get_event_loop().run_until_complete(start_server) 
        asyncio.get_event_loop().run_forever()


    async def procMessage(self, websocket, path):
        while True:
            self.__logger.debug("waiting new request")
            msg = await websocket.recv()
            msg_obj = False
            try:
                msg_obj = json.loads(msg)
            except Exception as e:
                await websocket.send("send parameter format error, json is needed " + str(e))
                self.__logger.error("Receive Message analyze error, raw message = " + msg)
                continue
            self.__logger.debug("Receive Message Success: {}".format(str(msg_obj)))
             
            respObj = {}
            respObj["msgtype"] = "RESP"
            if msg_obj != False and "roomid" in msg_obj and "uid" in msg_obj:
                msgType = int(msg_obj["type"])
                self.__logger.debug("receive msg info = " + str(msg_obj) + " , websocket = " + str(websocket))
                
                if msgType == 200:
                    #create chatroom
                    self.__logger.debug("process request room")
                    roomid = msg_obj['roomid']
                    uid = msg_obj['uid']
                    #一个人可以创建多个room
                    if roomid not in self.__roomBuffer:
                        self.__roomBuffer[roomid] = {}
                    self.__logger.debug("add socket roomid = %s, uid = %s"%(roomid, uid))
                    self.__roomBuffer[roomid][uid] = websocket

                    respObj["msgid"] = "200"
                    respObj["code"] = "0"
                    respObj["roomid"] = roomid
                    respObj["msg"] = "create room ok, room ids = %s"%(self.__roomBuffer[roomid].keys())
                    await websocket.send(json.dumps(respObj))    
                    self.__logger.debug("send response ok for msg 200")

                elif msgType == 119:
                    roomid = msg_obj['roomid']
                    uid = msg_obj['uid'] 
                    msg = msg_obj['msg']

                    respObj = {}
                    if roomid not in self.__roomBuffer:
                        respObj["msgid"] = "110"
                        respObj["msg"] = "no room info"
                    else:
                        respObj["msgid"] = "10"
                        respObj["msg"] = "push room info ok"
                  
                        self.__logger.debug("xxxxx")
                        for puid,sock in self.__roomBuffer[roomid].items():
                            self.__logger.debug("pppp")
                            if puid != uid:
                                self.__logger.debug("puid = %s"%(puid))
                                pmsg = {}
                                pmsg['msgid'] = "100" 
                                pmsg['msg'] = msg 
                                pmsg['fuid'] = uid

                                await sock.send(json.dumps(pmsg)) 
                          
                    await websocket.send(json.dumps(respObj))    
                    
