# -*- coding: cp936 -*-
import xlwt
from Interface.sharedClass import *
import datetime

def getNode():
    select = "SELECT DISTINCT(node) from adjacentNode where phaseID = '"+ str(PHASE_ID) +"'"
    res = Sqlite().select(select)
    list = []
    for r in res:
        list.append(r[0])
    list.sort()

    return list

def getDelayAndSNR(nodeA:str, nodeB:str):
    select = "select length, snr from adjacentNode where src='" + nodeA + "' and node='"+ nodeB + "' and phaseID = '"+ str(PHASE_ID) +"'"
    res = Sqlite().select(select)
    return res

def getPhase()->list:
    """
    ��ȡ���������е���λ
    :param rootAddress:root�ڵ�ĵ�ַ
    :return:��λ���б�
    """
    select = "SELECT DISTINCT(phaseID) from adjacentNode"
    res = Sqlite().select(select)
    list = []
    for r in res:
        list.append(r[0])
    list.sort()

    return list

def trans(fileName:str):
    book = xlwt.Workbook()
    sheet = book.add_sheet("sheet", cell_overwrite_ok=True)
    Y_axis = 0
    global PHASE_ID
    phaseIDList = getPhase()
    for phase in phaseIDList:
        PHASE_ID = phase
        nodes = getNode()
        nodesDic = {}
        index = 1
        for node in nodes:
            nodesDic[node] = index
            index = index + 1


        for node in nodes:
            sheet.write(Y_axis, nodesDic.get(node), str(node[8:12])) # ��
            sheet.write(nodesDic.get(node) + Y_axis, 0, str(node[8:12])) # ��

        for nodeA in nodes:
            for nodeB in nodes:
                if nodeA == nodeB:
                    continue
                res = getDelayAndSNR(nodeA, nodeB)
                if len(res) > 0:
                    delay = res[0][0]
                    snr = res[0][1]
                    result = str(int(delay)) + " (" + str(snr) + ")"
                    sheet.write(nodesDic.get(nodeA)+ Y_axis, nodesDic.get(nodeB), result)

        Y_axis = Y_axis+index + 1
    book.save(fileName)


def dataOutPut():
    cur_time = datetime.datetime.now()

    time = str(cur_time.strftime('%Y%m%d-%H_%M_%S'))
    path = "../backup/transData/" + time + ".xls"
    trans(path)


if __name__ == '__main__':
    dataOutPut()




