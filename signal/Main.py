#!/usr/bin/python
import configparser as cp
import logging
import logging.config
import SignalServer as ss
import os
import signal
#import MonitorServer as ms

class Server:
    
    def __init__(self):
        self.__logPath = False
        self.__serverAddr = False
        self.__serverPort = False
        self.__serverPrefix = False
        self.__logger = False
        self.__signal = False
        self.__cf = False
        self.__sigServer = False
        self.__moniServer = False
        self.__pid = False

    def Init(self):
        self.__cf = cp.ConfigParser()
        self.__cf.read("conf/Signal.conf")
        logging.config.fileConfig(self.__cf.get("global","logConf"))
        self.__logger = logging.getLogger("signal")
        self.__logger.debug("Init Server")

    def Run(self):
        self.__sigServer = ss.SignalServer(self.__logger, self.__cf)
        self.__sigServer.initialize()
        #write pid
        self.__sigServer.work()

    def ProcSig(self,signum, frame):
        os.kill(self.__pid, signal.SIGKILL)
        os.waitpid(self.__pid)


if __name__ == "__main__":
    server = Server()
    server.Init()
    server.Run()
