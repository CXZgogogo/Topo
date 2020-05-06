import numpy
import logging
from Interface.sharedClass import *
from TopoRecognitionAlgorithm import DataOutPut


logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO, filename='../log/procedure.log', filemode ='w', )

class Tree:
    def __init__(self):
        # 根节点
        # Type:Node
        # Default: None
        self.__root = None

    def setRoot(self, root:Node):
        self.__root = root
    def getRoot(self):
        return self.__root

    def calculateDistance(self):
        """
        计算每个节点与其父节点之间的距离
        """
        root = Node()
        MIN = float(readConfigurationFile("Topo").getCon("min_dely"))
        nodeList = self.preOrderTraverse()
        for node in nodeList:
            # 跳过root节点
            if node.getFather() is None:
                root = node
                continue
            # 根据三个点来算出距离
            # 1、X点：从节点向上依次找其父节点，当节点在该父节点的右树上时，
            #        找到该父节点左树上第一个真实左孩子节点，若父节点为真实节点就直接为父节点
            # 2、Y点：节点左树，第一个真实左孩子节点
            # 3、Z点，节点右树，第一个真实左孩子节点
            if node.getisVirtualNode():
                node_x = root
                # node_x = node.getFather()
                # node_x_child = node
                # while node_x.getisVirtualNode() and node_x.getFirstChild() == node_x_child:
                #     node_x = node_x.getFather()
                #     node_x_child = node_x_child.getFather()
                # while node_x.getisVirtualNode():
                #     node_x = node_x.getFirstChild()
                node_y = node.getFirstChild()
                while node_y.getisVirtualNode():
                    node_y = node_y.getFirstChild()
                node_z = node.getFirstChild().getRightBrother()
                while node_z.getisVirtualNode():
                    node_z = node_z.getFirstChild()

                # 解方程
                y1 = getLength(node_x.getName(), node_y.getName())
                y2 = getLength(node_x.getName(), node_z.getName())
                y3 = getLength(node_y.getName(), node_z.getName())
                matrix_x = sloveEqu([y1, y2, y3])
                if y3 < 30000:
                    x1 = matrix_x[0]
                    x2 = matrix_x[1]
                    x3 = matrix_x[2]
                else:
                    x1 = MIN
                    x2 = y1
                    x3 = y2

                # 由于误差问题，当小于值MIN时，直接设置为MIN
                if node_x is node.getFather():
                    if x1 < MIN:
                        x1 = MIN
                    node.setLength(x1)
                else:
                    l = self.calculateLengthNodeToNode(node_x, node.getFather())
                    length = x1 - l
                    if length < MIN:
                        length = MIN
                    node.setLength(length)
                if node_y is node.getFirstChild():
                    if x2 < MIN:
                        x2 = MIN
                    node_y.setLength(x2)
                if node_z is node.getFirstChild().getRightBrother():
                    if x3 < MIN:
                        x3 = MIN
                    node_z.setLength(x3)
            else:
                continue

    def insertVirtualNode(self):
        """
        在连接好的真实节点之间添加虚拟节点
        :param root: 根节点（根节点已经与真实节点相连）
        """
        root = self.__root
        v = 0
        add_virtual_node_list = []  # 等待添加虚拟节点的节点集合
        add_virtual_node_list.append(root)
        # 遍历集合，使每个节点都添加虚拟节点
        for node in add_virtual_node_list:
            v += 1  # 为了方便比对结果设置
            nodeFirstChild = node.getFirstChild()
            if nodeFirstChild is None:
                continue
            else:
                """
                情况1：节点为root
                   1.1、root只有一个孩子节点
                   1.2、root有不止一个孩子节点
                情况2：节点为虚拟节点
                    2.1、只有一个孩子节点
                    2.2、有两个孩子节点
                    2.3、有多于两个孩子节点
                情况3：节点为真实节点
                    3.1、有一个孩子节点
                    3.2、有两个及以上孩子节点
                """
                nodeSecondChild = nodeFirstChild.getRightBrother()
                # 情况1：节点为root
                if node == root:
                    # 1.1、root只有一个孩子节点：不做处理，直接将其孩子节点添加到待添加集合
                    if nodeSecondChild is None:
                        add_virtual_node_list.append(nodeFirstChild)
                        continue
                    else:
                        # 1.2、root有不止一个孩子节点：增加虚拟节点，孩子节点变为虚拟节点的孩子，将虚拟节点添加到待添加集合
                        virtualNode = Node()
                        virtualNode.setName(str(v))
                        node.setFirstChild(virtualNode)
                        virtualNode.setFather(node)
                        virtualNode.setisVirtualNode(True)
                        virtualNode.setFirstChild(nodeFirstChild)
                        nodeFirstChild.setFather(virtualNode)
                        nodeOtherChild = nodeFirstChild.getRightBrother()
                        while nodeOtherChild is not None:
                            nodeOtherChild.setFather(virtualNode)
                            nodeOtherChild = nodeOtherChild.getRightBrother()
                        add_virtual_node_list.append(virtualNode)
                        continue
                # 情况2：节点为虚拟节点
                elif node.getisVirtualNode():
                    # 2.1、只有一个孩子节点：不做处理，直接将其孩子节点添加到待添加集合
                    if nodeSecondChild is None:
                        add_virtual_node_list.append(nodeFirstChild)
                        continue
                    nodeOtherChild = nodeSecondChild.getRightBrother()
                    # 2.2、有两个孩子节点：不做处理，将其两个孩子节点添加到待添加集合（顺序为先左孩子，后右孩子）
                    if nodeOtherChild is None:
                        add_virtual_node_list.append(nodeFirstChild)
                        add_virtual_node_list.append(nodeSecondChild)
                        continue
                    # 2.3、有多于两个孩子节点：增加虚拟节点，作为该节点的孩子节点，
                    #      该节点第二及以后孩子节点变为虚拟节点的孩子节点。
                    #      将第一孩子节点与虚拟节点添加到待添加集合（考虑顺序）
                    else:
                        virtualNode = Node()
                        virtualNode.setName(str(v))
                        virtualNode.setisVirtualNode(True)
                        nodeFirstChild.setRightBrother(virtualNode)
                        virtualNode.setFather(node)
                        virtualNode.setFirstChild(nodeSecondChild)
                        nodeSecondChild.setFather(virtualNode)
                        while nodeOtherChild is not None:
                            nodeOtherChild.setFather(virtualNode)
                            nodeOtherChild = nodeOtherChild.getRightBrother()
                        add_virtual_node_list.append(nodeFirstChild)
                        add_virtual_node_list.append(virtualNode)
                        continue
                # 情况3：节点为真实节点
                else:
                    nodeFather = node.getFather()
                    # 3.1、有一个孩子节点：增加一个虚拟节点，该节点和孩子节点变为虚拟节点的孩子节点。
                    #      将虚拟节点与第一孩子节点添加到待添加集合（考虑顺序）
                    if nodeSecondChild is None:
                        virtualNode = Node()
                        virtualNode.setName(str(v))
                        virtualNode.setisVirtualNode(True)
                        node.setFirstChild(None)
                        nodeBrother = nodeFather.getFirstChild()
                        if nodeBrother is None:
                            continue
                        elif nodeBrother == node:
                            nodeFather.setFirstChild(virtualNode)
                            virtualNode.setRightBrother(node.getRightBrother())
                        else:
                            while nodeBrother.getRightBrother() != node:
                                print(type(nodeBrother))
                                nodeBrother = nodeBrother.getRightBrother()
                            nodeBrother.setRightBrother(virtualNode)
                            virtualNode.setRightBrother(node.getRightBrother())
                        virtualNode.setFather(nodeFather)
                        virtualNode.setFirstChild(node)
                        node.setFather(virtualNode)
                        node.setRightBrother(nodeFirstChild)
                        nodeFirstChild.setFather(virtualNode)
                        add_virtual_node_list.append(virtualNode)
                        add_virtual_node_list.append(nodeFirstChild)
                        continue
                    else:
                        # 3.2、有两个及以上孩子节点：增加虚拟节点_1，该节点变为节点_1的孩子节点，
                        #      再增加虚拟节点_2，作为节点_1的孩子节点，原节点的孩子节点作为节点_2的孩子，
                        #      将虚拟节点_1与虚拟节点_2添加到待添加集合（考虑顺序）
                        virtualNode_1 = Node()
                        virtualNode_1.setName(str(v))
                        virtualNode_1.setisVirtualNode(True)
                        virtualNode_2 = Node()
                        virtualNode_2.setName(str(v))
                        virtualNode_2.setisVirtualNode(True)
                        # 把node的兄弟设置好
                        nodeBrother = nodeFather.getFirstChild()
                        if nodeBrother == node:
                            nodeFather.setFirstChild(virtualNode_1)
                            virtualNode_1.setRightBrother(node.getRightBrother())
                        else:
                            while nodeBrother.getRightBrother() != node:
                                nodeBrother = nodeBrother.getRightBrother()
                            nodeBrother.setRightBrother(virtualNode_1)
                            virtualNode_1.setRightBrother(node.getRightBrother())
                        virtualNode_1.setFirstChild(node)
                        virtualNode_1.setFather(nodeFather)
                        node.setFather(virtualNode_1)
                        node.setRightBrother(virtualNode_2)
                        node.setFirstChild(None)
                        virtualNode_2.setFather(virtualNode_1)
                        virtualNode_2.setFirstChild(nodeFirstChild)
                        nodeOtherChild = nodeFirstChild
                        while nodeOtherChild is not None:
                            nodeOtherChild.setFather(virtualNode_2)
                            nodeOtherChild = nodeOtherChild.getRightBrother()
                        add_virtual_node_list.append(virtualNode_1)
                        add_virtual_node_list.append(virtualNode_2)
                        continue

    def calculateLengthNodeToNode(self, nodeA:Node, nodeB:Node)->float:
        """
        计算两个节点之间距离
        :param nodeA: 节点A
        :param nodeB: 节点B
        :return: 两个节点之间的时延
        """
        listA_fathers = []
        listB_fathers = []
        first_shared_father = Node()
        l = 0.0
        # 找到A的所有父节点
        while nodeA.getFather() is not None:
            listA_fathers.append(nodeA)
            nodeA = nodeA.getFather()
        #找到B的父节点，在其第一个共享父节点处结束
        while nodeB.getFather() is not None:
            if nodeB in listA_fathers:
                first_shared_father = nodeB
                break
            listB_fathers.append(nodeB)
            nodeB = nodeB.getFather()
        # 计算A到共享父节点之间的距离
        for n in listA_fathers:
            if n == first_shared_father:
                break
            l = l + n.getLength()
        # 计算B到共享父节点之间的距离
        for m in listB_fathers:
            l = l + m.getLength()
        return l

    def insertChild(self, father:Node, child:Node):
        """
        在对真实节点聚类时使用，将待聚类节点与已聚类节点树相连
        :param father:待聚类节点的父节点
        :param child:待聚类节点
        """
        result = 0
        nextChild = Node()
        prevChild = father.getFirstChild()
        while prevChild is not None:
            nextChild = prevChild.getRightBrother()
            length_prev = getLength(father.getName(), prevChild.getName())
            length_this = getLength(father.getName(), child.getName())
            if length_prev > length_this:
                break
            else:
                if nextChild is None:
                    result = -1
                    break
                prevChild = nextChild
                result = result + 1
        if result == 0:
            father.setFirstChild(child)
            if prevChild is not None:
                child.setRightBrother(prevChild)
        elif result == -1:
            prevChild.setRightBrother(child)
        else:
            prevChild.setRightBrother(child)
            child.setRightBrother(nextChild)

    def realNodeConnectWithRoot(self):
        """
        将真实节点与root相连
        :return:
        """
        root = self.__root
        THRESHOLD = float(readConfigurationFile("Topo").getCon("threshold"))
        nodesToClustering = []  # 待聚类节点，存储的是节点名称，字符串
        nodes_in_cluster = []  # 已聚类节点，存储的是节点
        nodesNameInCluster = []  # 已聚类节点名字， 存储的是节点名称，字符串
        nodes_in_cluster.append(root)
        nodesNameInCluster.append(root.getName())
        adjList = getAdjacentNode(root.getName())
        adjList_1 = []
        for n1 in adjList:
            if n1 in nodesNameInCluster:
                continue
            adjList_1.append(n1)
        adjList = adjList_1
        for n2 in adjList:
            nodesToClustering.append(n2)
        while len(nodesToClustering) > 1:
            nodesToClustering = []
            nearstNodeList = []
            for n3 in nodes_in_cluster:
                n3_adj = getAdjacentNode(n3.getName())
                n3_adj_1 = []
                for n3_adj_node in n3_adj:
                    if n3_adj_node[0] in nodesNameInCluster:
                        continue
                    n3_adj_1.append(n3_adj_node)
                n3_adj = n3_adj_1
                for n3_adj_node1 in n3_adj:
                    if n3_adj_node1[0] in nodesToClustering:
                        continue
                    nodesToClustering.append(n3_adj_node1[0])
                if len(n3_adj) > 0:
                    n3_adj.sort(key=lambda x: x[1])
                    # 三元组，第一项为已聚类节点中一个节点，第二项为第一项节点邻接点中最近的点，第三项为距离
                    adj_node = Node()
                    adj_node.setName(n3_adj[0][0])
                    nearst_node = (n3, adj_node, n3_adj[0][1])
                    nearstNodeList.append(nearst_node)
            nearstNodeList.sort(key=lambda x: x[2])
            adjNode = nearstNodeList[0][1]  # 待添加节点
            nearestNode = nearstNodeList[0][0]  # 最近节点
            if nearestNode == root:
                adjNode.setFather(root)
            else:
                nearestFather = nearestNode.getFather()  # 最近节点的父节点
                dis_nearest_to_adj = nearstNodeList[0][2]
                dis_father_to_nearest = getLength(nearestNode.getName(), nearestFather.getName())
                dis_father_to_adj = getLength(nearestFather.getName(), adjNode.getName())
                distance = dis_father_to_adj - (dis_father_to_nearest + dis_nearest_to_adj)
                if abs(distance) < THRESHOLD:
                    adjNode.setFather(nearestNode)
                else:
                    adjNode.setFather(nearestFather)
                # 将此节点插入父节点的兄弟节点中
            self.insertChild(adjNode.getFather(), adjNode)
            nodes_in_cluster.append(adjNode)
            nodesNameInCluster.append(adjNode.getName())
        return

    def preOrderTraverse(self):
        """
        前序遍历树
        :return:树的前序遍历
        """
        root = self.__root
        res = []
        if root is None:
            return res
        stack = []
        stack.append(root)
        while len(stack)>0:
            current = stack.pop()
            res.append(current)
            if current.getFirstChild() is not None:
                if current.getFirstChild().getRightBrother() is not None:
                    stack.append(current.getFirstChild().getRightBrother())
            if current.getFirstChild() is not None:
                stack.append(current.getFirstChild())
        return res

def sloveEqu(y):
    """
    解方程
    :param y:
    :return:
    """
    try:
        A = numpy.array([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
        Y = numpy.array(y)
        result = numpy.linalg.solve(A, Y)
        return result
    except Exception as e:
        logging.exception(e)

def getLength(src:str, node:str)->float:
    """
    获取两点之间长度，不可达返回65536
    :param src:源节点地址
    :param node:目的节点地址
    :return:两个节点之间时延
    """
    l = 65536
    table_adjacentNode = readConfigurationFile("Database").getCon("table_adjacentNode")
    get_length1 = "select length from " + table_adjacentNode + " where src='" + str(src) + "' and node='" + str(node) + "'"
    result1 = Sqlite().select(get_length1)
    get_length2 = "select length from " + table_adjacentNode + " where src='" + str(node) + "' and node='" + str(src) + "'"
    result2 = Sqlite().select(get_length2)
    l1 = 65535
    l2 = 65535
    try:
        l1 = result1[0][0]
    except:
        pass
    try:
        l2 = result2[0][0]
    except:
        pass
    if l1 > 60000:
        if l2 > 60000:
            l = l1
        else:
            l = l2
    else:
        if l2 > 60000:
            l = l1
        else:
            l = (l1+l2)/2

    return l

def getAdjacentNode(node:str)->list:
    """
    获取节点邻接表
    :param node: 节点的地址
    :return: list，list中的元素为2元组，
             其中2元组第一项是node的邻接点的地址，第二项是node和邻接点之间时延，且list根据时延从小到大排序
    """
    adjacentNodeList = []
    list = {}
    nodeList = []
    table_adjacentNode = readConfigurationFile("Database").getCon("table_adjacentNode")
    resultsSRC = Sqlite().select("select node, length from " + table_adjacentNode + " where src='"+ node +"' and phaseID = '"+ str(PHASE_ID) +"'")
    resultsNODE = Sqlite().select("select src, length from " + table_adjacentNode + " where node='"+ node +"' and phaseID = '"+ str(PHASE_ID) +"'")
    for row in resultsSRC:
        node = row[0]
        length = row[1]
        nodeList.append(node)
        list[node] = length
    for row in resultsNODE:
        node = row[0]
        length = row[1]
        if node in list:
            if list.get(node) >= 65000 and length < 65000:
                list[node] = length
            elif list.get(node) < 65000 and length < 65000:
                l1 = list.get(node)
                l = (l1 + length) / 2
                list[node] = l
    for adjacentNode in list.items():
        adjacentNodeList.append(adjacentNode)
    sList = sorted(adjacentNodeList)
    if sList is None:
        logging.info("no adjacentNode")
    return sList

def getPhase(rootAddress:str)->list:
    """
    获取网络中所有的相位
    :param rootAddress:root节点的地址
    :return:相位的列表
    """
    phaseIDList = []
    table_adjacentNode = readConfigurationFile("Database").getCon("table_adjacentNode")
    results = Sqlite().select("SELECT DISTINCT(phaseID) FROM " + table_adjacentNode + " where src='"+ rootAddress +"'")
    for row in results:
        phaseIDList.append(row[0])
    return phaseIDList

def insertInto(id, isVirtual, table):
    """
    在表中插入一条新数据
    :param id: 要更新的数据的ID
    :param isVirtual: 虚拟节点标识
    :param table: 表名称
    """
    # 定义要执行的sql语句
    write = "INSERT  INTO "+ table +"(ID, isVirtual) VALUES (" + str(id) + "," + str(isVirtual) + ")"
    try:
        Sqlite().insert(write)
    except:
        logging.info("写入错误，已存在节点")

def delData(table):
    """
    删除表中的数据
    :param table: 表名
    """
    # 定义要执行的sql语句
    delete = "delete from " + table
    Sqlite().delete(delete)

def copyData(TargetTable, SourceTable):
    """
    复制表中的数据到另一张表
    :param TargetTable: 目标表
    :param SourceTable: 源表
    """
    # 定义要执行的sql语句
    write = "INSERT INTO " + str(TargetTable) + " SELECT * FROM " + str(SourceTable)
    try:
        Sqlite().update(write)
    except:
        logging.info("复制不成功")

def updateData(field, date, id, table):
    """
    更新表中的数据
    :param field: 要更新的字段名
    :param date: 要更新的内容
    :param id: 要更新的数据的ID
    :param table: 要更新的表名
    """
    # 定义要执行的sql语句
    write = "UPDATE "+ table +" SET " + str(field) + " = \'" + str(date) + "\' WHERE ID = " + str(id)
    try:
        Sqlite().update(write)
    except:
        logging.info("数据更新不成功")

def delDataBeforeStart():
    """
    测量开始前先删去历史数据
    """
    datebaseList = {}
    datebaseList[1] = (readConfigurationFile("Database").getCon("table_oldTopo_in_phase_A"),
                       readConfigurationFile("Database").getCon("table_newTopo_in_phase_A"))
    datebaseList[2] = (readConfigurationFile("Database").getCon("table_oldTopo_in_phase_B"),
                       readConfigurationFile("Database").getCon("table_newTopo_in_phase_B"))
    datebaseList[3] = (readConfigurationFile("Database").getCon("table_oldTopo_in_phase_C"),
                       readConfigurationFile("Database").getCon("table_newTopo_in_phase_C"))
    for i in range(1, 4):
        oldTopo = datebaseList.get(i)[0]
        newTopo = datebaseList.get(i)[1]
        delData(oldTopo)
        copyData(oldTopo, newTopo)
        delData(newTopo)

def writeDatabase(nodeList:list):
    """
    将节点信息写入数据库中
    :param nodeList: 节点列表
    """
    datebaseList = {}
    datebaseList[1] = readConfigurationFile("Database").getCon("table_newTopo_in_phase_A")
    datebaseList[2] = readConfigurationFile("Database").getCon("table_newTopo_in_phase_B")
    datebaseList[3] = readConfigurationFile("Database").getCon("table_newTopo_in_phase_C")
    newTopo = datebaseList.get(PHASE_ID)
    IDList = {}
    id = 1
    for node in nodeList:
        IDList[node] = id
        id += 1
    for node in nodeList:
        ID = IDList.get(node)
        isVirtual = 0
        if node.getisVirtualNode():
            isVirtual = 1
        insertInto(ID, isVirtual, newTopo)
        if node.getName() != None:
            updateData("name", node.getName(), ID, newTopo)
        if node.getFather() != None:
            updateData("father", IDList.get(node.getFather()), ID, newTopo)
            updateData("length", round(node.getLength(), 2), ID, newTopo)
        if node.getFirstChild() != None:
            updateData("firstChild", IDList.get(node.getFirstChild()), ID, newTopo)
        if node.getRightBrother() != None:
            updateData("rightBrother", IDList.get(node.getRightBrother()), ID, newTopo)

count = 0

def getTopo(rootAddress:str):
    """
    拓扑发现算法
    :param rootAddress: root节点的地址
    :return: 拓扑发现结束标识
    """
    DataOutPut.dataOutPut()
    delDataBeforeStart()
    try:
        global PHASE_ID
        global count

        phaseIDList = getPhase(rootAddress)
        for phase in phaseIDList:
            # 设置相位
            PHASE_ID = phase
            #设置根节点，为了显示方便，每个相位根节点分开
            root = Node()
            root.setName(rootAddress)
            topo = Tree()
            topo.setRoot(root)
            topo.realNodeConnectWithRoot()
            count+=1
            topo.insertVirtualNode()
            count += 1
            topo.calculateDistance()
            count += 1
            nodeList = topo.preOrderTraverse()
            count += 1
            writeDatabase(nodeList)
            count += 1
        return 1    #返回结束标识
    except Exception:
        return 0    #返回错误标识

if __name__ == '__main__':
    # a = getTopo("R")
    a = getTopo("000000000000")
    print(a)