import matplotlib
matplotlib.use("Qt5Agg")
from Interface.sharedClass import *
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import (QColor,QPixmap)
from PyQt5.QtCore import ( QRectF, Qt, QObject)
# 自定义虚拟节点的QGraphicsItem
class Virtual_Node(QGraphicsItem):

    def __init__(self):
        super(Virtual_Node, self).__init__()
        self.sequence = 0
        self.setCursor(Qt.OpenHandCursor)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsMovable)
    def boundingRect(self):  ##这个纯虚函数将图元的外边界定义为矩形; 所有绘画必须限制在图元的边界矩形内。
        return QRectF(-10, -10, 10, 10)
    def paint(self):
        painter.setPen(QColor(166, 66, 250))  ##.NoPen)
        painter.setBrush(Qt.red)  ##.darkGray)
        painter.drawRect(-5, -5, 240, 100)
        return
# 自定义真实节点的QGraphicsItem
class Nomal_Node(QObject,QGraphicsItem):

    def __init__(self):
        super(Nomal_Node, self).__init__()
        self.sequence = 0
        self.setCursor(Qt.OpenHandCursor)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.pixmap = QPixmap()
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsMovable)

    def boundingRect(self):  ##这个纯虚函数将图元的外边界定义为矩形; 所有绘画必须限制在图元的边界矩形内。
        return QRectF(-10, -10, 10, 10)

    def paint(self):
        self.pixmap=QPixmap()
        return
class topo_picture():
    def count_node_childs(self, node: Node):
        count = 0
        node_nc = node.getFirstChild()
        if node_nc is not None:
            while node_nc is not None:
                count = count + self.count_node_childs(node_nc)
                node_nc = node_nc.getRightBrother()
        else:
            count = 1
        return count

    def icon_locate(self, node: Node, scale, iconsize, originx, originy):
        locatex = 0
        locatey = 0
        if node.getFather() is None:
            locatex = originx
            locatey = originy
        else:
            node_father = node.getFather()
            # node_brother = node_father.getFirstChild()
            # node_brother_branchNum = self.count_node_childs(node_brother)
            father_location = self.icon_locate(node_father, scale, iconsize, originx, originy)
            if node.getisVirtualNode():
                node_brother = node_father.getFirstChild()
                node_brother_branchNum = self.count_node_childs(node_brother)
                if node_brother.getName() == node.getName():
                    locatex = father_location[0] + iconsize + scale
                    locatey = father_location[1]
                else:
                    locatex = father_location[0]
                    locatey = father_location[1]
                    # if vitual node has three or more child locatex need to increase
                    if node_brother.getRightBrother() is not None:
                        # node_brother_rightbrother = self.search_rightbrother()
                        if (node_brother.getRightBrother()).getRightBrother() is not None:
                            locatex = locatex + iconsize + scale
                    while node_brother is not None:
                        if node.getName() == node_brother.getName():
                            break
                        else:
                            locatey = locatey + (iconsize + scale) * node_brother_branchNum
                            # print("N",node.getName(),node_brother.getName(),node_brother.getBranchNum())
                            node_brother = node_brother.getRightBrother()
            else:
                node_brother = node_father.getFirstChild()
                node_brother_branchNum = self.count_node_childs(node_brother)
                locatex = father_location[0] + scale
                locatey = father_location[1]
                while node_brother is not None:
                    if node == node_brother:
                        break
                    else:
                        locatey = locatey + (iconsize + scale) * node_brother_branchNum
                        node_brother = node_brother.getRightBrother()
        return ((locatex, locatey))
