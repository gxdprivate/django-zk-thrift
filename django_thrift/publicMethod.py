#coding=utf-8

from django.conf import settings
import socket


class ReadSetting:

    def __init__(self,settings):
        self.settings = settings

    # 从django的setting文件获取服务接口名字
    def getServiceName(self):
        try:
            serviceName = self.settings.THRIFT['SERVICE']
        except Exception as e:
            serviceName = None

        return serviceName

    # 从django的setting文件获取zk地址
    def getZkAddress(self):
        try:
            host = self.settings.ZK['HOST']
            port = self.settings.ZK['PORT']
            zkAddress = str(host) + ':' + str(port)
        except Exception as e:
            zkAddress = None
        return zkAddress

    # 从django的setting文件获取服务分组
    def getGroupName(self):
        try:
            groupName = self.settings.THRIFT['GROUPNAME']
        except Exception as e:
            groupName = 'dev'
        return groupName

    # 从django的setting文件获取服务版本
    def getVersion(self):
        try:
            version = self.settings.THRIFT['VERSION']
        except Exception as e:
            version = 'v1'
        return version

class SocketInfo:

    def __init__(self):
        pass

    # 获取当前主机ip地址
    def getCurrentHost(self):
        hostName = socket.gethostname()
        currenIp = socket.gethostbyname(hostName)
        return currenIp

    # 获取一个端口，默认从8801端口以后轮询占用
    def getAvailablePort(self):
        defaultPort = 8801
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        currentIp = self.getCurrentHost()
        while (defaultPort < 50000):
            try:
                result = s.connect_ex((currentIp, defaultPort))
                if result != 0:
                    break
                else:
                    defaultPort = defaultPort + 1
            except Exception as e:
                print(e)
                return None

        return defaultPort