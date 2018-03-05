# django-zk-thrift
在django框架中引入thrift实现rpc框架，同时加入zookeeper实现服务管理
我不是代码的生产者，只是代码的搬运工
本项目整合这三个项目：
参考项目：https://github.com/dstarner/django_thrift
参考项目：https://github.com/eleme/thriftpy
参考项目：https://github.com/python-zk/kazoo

## Installation

安装.
1.下载附件中的代码到本地环境，解压，cp -r django_mt_thrift/dango-thrift  /usr/local/lib/python3.6/site-packages/  (系统环境请根据实际情况而定)
2.新建一个django工程
3.新建一个应用

## 配置

配置应用, 需要添加 `django_thrift` 到你的setting文件，添加 `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...  # 其他默认安装的组件.
    'django_thrift',
]

THRIFT = {
    "FILE": "{APPname}/ProjectService.thrift",
    "SERVICE": "ProjectService",
    "GROUPNAME":"test",
    "VERSION":"v1"
}
  
ZK = {"HOST":"{ZKADDRESS}","PORT":"2181"}
```

## 将thrift方法和django方法做映射

为了将thrift方法映射到django方法, 需要使用 *Service Handler*. 在 `service.py` 中的方法.
注意框架加载了service.py为方法集合，文件名如果不对，将无法加载。

```python
from django_thrift.handler import create_handler


handler = create_handler() 


@handler.map_function("doSearchProjectList")  
# 将方法 `doSearchProjectList_version1` 绑定到thrift接口的 `doSearchProjectList`
def doSearchProjectList_version1():
    return {"a":"bb"}
```

ps:如果你的thrift接口定义了参数 和 数据格式，你直接在service方法中使用一致的参数和数据格式，这样才可以调用到。

## 启动zk

macos下直接使用brew安装zk即可

```python
zkServer start
```

## 启动django

直接运行下面命令启动django服务，实现方法地址注册到zookeeper上，同时完成方法启动

```bash
./manange.py runrpcserver
```


## thrift文件

```python
#文件名 ： ProjectService.thrift
service ProjectService {
    /*
     *  查询所有项目，返回pkey,pname字典
     */
    map<string,string> doSearchProjectList(),
}
```

