# -*- coding: cp936 -*-
import xlwt
from Interface.sharedClass import Sqlite

def getNode():
    select = "SELECT DISTINCT(node) from adjacentNode"
    res = Sqlite().select(select)
    list = []
    for r in res:
        list.append(r[0])
    list.sort()

    return list

def getDelayAndSNR(nodeA:str, nodeB:str):
    select = "select length, snr from adjacentNode where src='" + nodeA + "' and node='"+ nodeB + "'"
    res = Sqlite().select(select)
    return res

def main(sheetName:str, fileName:str):
    book = xlwt.Workbook()
    sheet = book.add_sheet(sheetName, cell_overwrite_ok=True)
    nodes = getNode()
    nodesDic = {}
    index = 2
    for node in nodes:
        nodesDic[node] = index
        index = index+1

    for node in nodes:
        sheet.write(1, nodesDic.get(node), str(node[8:12]))
        sheet.write(nodesDic.get(node), 1, str(node[8:12]))

    for nodeA in nodes:
        for nodeB in nodes:
            if nodeA == nodeB:
                continue
            res = getDelayAndSNR(nodeA, nodeB)
            if len(res) > 0:
                delay = res[0][0]
                snr = res[0][1]
                result = str(int(delay)) + " (" + str(snr) + ")"
                sheet.write(nodesDic.get(nodeA), nodesDic.get(nodeB), result)
    book.save(fileName)

if __name__ == '__main__':
    main("shell", "../log/0415_11点.xls")


