# coding=utf-8

from kazoo.client import KazooClient
from django_thrift.publicMethod import ReadSetting,SocketInfo
from random import randint
import socket

'''
约定：serviceName就是thrift的接口名
说明：zkAddress一般是zk地址，例如：ip:port形式
服务化：groupName分组名，例如：dev，test，pro随意自定义等 ； version服务版本号，用于不同事业部定制化需求
'''

class ForClient(object):

    def __init__(self,settings):
        self.settings = settings
        self.kazooClient = KazooClient(hosts=ReadSetting(self.settings).getZkAddress())
        self.kazooClient.start()
        self.serviceName = ReadSetting(self.settings).getServiceName()
        self.groupName = ReadSetting(self.settings).getGroupName()
        self.version = ReadSetting(self.settings).getVersion()

    #随机获取一个可用的服务调用地址
    def getRandomNode(self):
        res = self.getAvailableNode()
        node = res[randint(0, len(res) - 1)]
        host = node.split(':')[0]
        port = int(node.split(':')[1])
        return host, port

    # 获取当前服务的所有分组
    def getServiceGroups(self):
        if self.kazooClient.exists('/' + self.serviceName):
            return self.kazooClient.get_children('/' + self.serviceName)
        return []

    #获取当前分组下的所有版本
    def getGroupVersions(self):
        if self.kazooClient.exists('/' + self.serviceName + '/' + self.groupName):
            return self.kazooClient.get_children('/' + self.serviceName + '/' + self.groupName)
        return []

    #获取可用节点列表
    def getAvailableNode(self):
        res = []
        if self.kazooClient.exists('/' + str(self.serviceName) + '/' + str(self.groupName) + '/' + str(self.version)):
            nodeList = self.kazooClient.get_children('/' + str(self.serviceName) + '/' + str(self.groupName) + '/' + str(self.version))
            #检测每个节点可用性
            #print(nodeList)
            for node in nodeList:
                host = str(node.split(":")[0])
                port = int(node.split(":")[1])
                try:
                    socket.create_connection((host, port), 10)
                    res.append(node)
                except Exception as e:
                    self.deleteUselessNode(node)
        return res

    #删除不可用节点
    def deleteUselessNode(self,node):
        nodeFull = '/' + self.serviceName + '/' + self.groupName + '/' + self.version + '/' + node
        self.kazooClient.delete(nodeFull)

class ForServer(object):

    def __init__(self,settings):
        self.settings = settings
        self.kazooClient = KazooClient(hosts=ReadSetting(self.settings).getZkAddress())
        self.kazooClient.start()
        self.serviceName = ReadSetting(self.settings).getServiceName()
        self.groupName = ReadSetting(self.settings).getGroupName()
        self.version = ReadSetting(self.settings).getVersion()
        self.host = SocketInfo().getCurrentHost()
        self.port = SocketInfo().getAvailablePort()


    # 注册到zookeeper上
    def register(self):
        self.createService()
        self.createGroup()
        self.createVersion()
        self.createNode()

    #创建服务信息
    def createService(self):
        if self.kazooClient.exists('/' + self.serviceName):
            pass
        else:
            self.kazooClient.ensure_path('/' + self.serviceName)

    #创建分组信息
    def createGroup(self):
        if self.kazooClient.exists('/' + str(self.serviceName) + '/' + str(self.groupName)):
            pass
        else:
            self.kazooClient.ensure_path('/' + str(self.serviceName) + '/' + str(self.groupName))

    #创建版本信息
    def createVersion(self):
        if self.kazooClient.exists('/' + str(self.serviceName) + '/' + str(self.groupName) + '/' + str(self.version)):
            pass
        else:
            self.kazooClient.ensure_path(
                '/' + str(self.serviceName) + '/' + str(self.groupName) + '/' + str(self.version))

    #创建节点数据
    def createNode(self):
        if self.kazooClient.exists(
                '/' + str(self.serviceName) + '/' + str(self.groupName) + '/' + str(self.version) + '/' + str(
                        self.host) + ':' + str(self.port)):
            pass
        else:
            self.kazooClient.create(
                '/' + str(self.serviceName) + '/' + str(self.groupName) + '/' + str(self.version) + '/' + str(
                    self.host) + ':' + str(self.port))
