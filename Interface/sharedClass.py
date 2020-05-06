import configparser
import sqlite3
import os
import sys

# 定义类，读取配置文件
class readConfigurationFile:
    def __init__(self, section:str):
        self.__section = section

    def getCon(self, valueName:str):
        """
        获取对应字段的值
        :param valueName: 字段名称
        :return: 字段值
        """
        cf = configparser.ConfigParser()
        # path=os.path.abspath(os.path.dirname(sys.argv[0]))
        # file=os.path.abspath(os.path.join(os.getcwd(),'..','Main','config.ini'))
        # cf.read("config.ini")
        # cf.read(file)
        cf.read('../config/config.ini')
        return cf.get(self.__section, valueName)
    def setCon(self, valueName:str,value:str):
        """
        获取对应字段的值
        :param valueName: 字段名称
        :param:value: 字段值
        """
        cf = configparser.ConfigParser()
        file='../config/config.ini'
        cf.read(file)
        cf.set(self.__section, valueName, value)
        cf.write(open(file, "w+"))


# 定义Sqlite类
class Sqlite:
    def __init__(self):
        self.__database = readConfigurationFile("Database").getCon("database_name")
        # print(self.__database)

    def insert(self, write:str):
        """
        往数据库中插入一条新数据
        :param write: 插入语句
        """
        # 连接到SQlite数据库
        # file = os.path.abspath(os.path.join(os.getcwd(), '..', 'Main', self.__database))
        conn = sqlite3.connect(self.__database)
        # conn = sqlite3.connect(file)
        # 创建一个cursor：
        cursor = conn.cursor()
        cursor.execute(write)
        conn.commit()
        cursor.close()
        conn.close()

    def insertmany(self, write:str,arr):
        """
        往数据库中插入一条新数据
        :param write: 插入语句
        """
        # 连接到SQlite数据库
        conn = sqlite3.connect(self.__database)
        # 创建一个cursor：
        cursor = conn.cursor()
        try:
            cursor.executemany(write,arr)
            conn.commit()
            # cursor.close()
            # conn.close()
            return 1
        except:
            print(1)
            conn.rollback()
            return 0

    def delete(self, delect:str):
        """
        删除数据
        :param delect: 删除语句
        """
        # 连接到SQlite数据库
        conn = sqlite3.connect(self.__database)
        # 创建一个cursor：
        cursor = conn.cursor()
        # 定义要执行的sql语句
        cursor.execute(delect)
        conn.commit()
        cursor.close()
        conn.close()

    def update(self, write:str):
        """
        更新数据库
        :param write: 更新语句
        """
        # 连接到SQlite数据库
        conn = sqlite3.connect(self.__database)
        # 创建一个cursor：
        cursor = conn.cursor()
        cursor.execute(write)
        conn.commit()
        cursor.close()
        conn.close()

    def select(self, select:str):
        """
        查询数据库
        :param select: 查询语句
        :return: 查询结果
        """
        # 连接到SQlite数据库
        conn = sqlite3.connect(self.__database)
        # 创建一个cursor：
        cursor = conn.cursor()
        cursor.execute(select)
        results = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return results

# 定义节点类
class Node:
    def __init__(self):
        # name
        # Type:String
        # Default:""
        # Note: Node name, Unique ID, VirtualNode has no name
        self.__name = ""

        # father
        # Type:Pointer
        # Default: None
        # Note: Pointer to the Father of the tree
        self.__father = None

        # length
        # Type:float
        # Default: -1/None
        # Note: Distance to Father node, -1 indicate can not reach
        self.__length = None

        # firstChild
        # Type:Pointer
        # Default: None
        # Note: Pointer to the First Child of the tree
        self.__firstChild = None

        # rightBrother
        # Type:Pointer
        # Default: None
        # Note: Pointer to the rightBrother of the tree
        self.__rightBrother = None

        # isVirtualNode
        # Type:bool
        # Default: False
        # Note: if the Node is Virtual
        self.__isVirtualNode = False

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getFather(self):
        return self.__father

    def setFather(self, father):
        self.__father = father

    def getLength(self):
        return self.__length

    def setLength(self, length):
        self.__length = length

    def getFirstChild(self):
        return self.__firstChild

    def setFirstChild(self, firstChild):
        self.__firstChild = firstChild

    def getRightBrother(self):
        return self.__rightBrother

    def setRightBrother(self, rightBrother):
        self.__rightBrother = rightBrother

    def getisVirtualNode(self):
        return self.__isVirtualNode

    def setisVirtualNode(self, isVirtualNode):
        self.__isVirtualNode = isVirtualNode


# a = Sqlite().select("select length from adjacentNode_1 where src ='A' and node = 'B'")
# l = a[0][0]
# print(l)
#
# b = readConfigurationFile("Database").getCon("database_name")
# print(type(b))
# print(b)
