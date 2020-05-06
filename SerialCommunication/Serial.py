import logging
import random
import serial
import threading
import struct
import time
from queue import Queue
import numpy as np
# from Main import sharedClass as sh
from Interface.sharedClass import *
from socket import *


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                           参数设置函数
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
state='Findhead'
state_1='处理帧头'
rec_queue=Queue(maxsize=500)
rec_data=[]
handle_data=[]
head_flag=0
time_flag=0
len_tempdata_old=0
end_flag=0
final_flag=0
count_flag=0

reply_order=bytes([0x68,0x06,0x00,0x0e,0x7c,0x16])     #[0x68,0x00 ,0x06,0x0e,0x00,0x16]
cancelorder=bytes([0x68,0x06,0x00,0x0a,0x78,0x16])    #[0x68,0x00,0x06,0x0a,0x78,0x16]
buildorder=bytes([0x68,0x06,0x00,0x0c,0x7a,0x16])     #上位机查询网络是否建立成功的指令


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                           参数读取函数
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
udpOrserial_flag=int(readConfigurationFile("Serial").getCon("serial_or_udp"))
DATABASE =readConfigurationFile("Database").getCon("database_name")
COM=readConfigurationFile("Serial").getCon("com")
Baudrate=readConfigurationFile("Serial").getCon("baudrate")
TABLE=readConfigurationFile("Database").getCon("table_adjacentNode")
event_analyze=threading.Event()
delayTABLE=readConfigurationFile("Database").getCon("table_delay")
fupinTABLE=readConfigurationFile("Database").getCon("table_fupin")
HOST1 = readConfigurationFile("Serial").getCon("HOST1")
HOST2 = readConfigurationFile("Serial").getCon("HOST2")
PORT1 = readConfigurationFile("Serial").getCon("PORT1")
PORT2 = readConfigurationFile("Serial").getCon("PORT2")
BUFSIZE = readConfigurationFile("Serial").getCon("BUFSIZE")

ADDR1 = (HOST1, int(PORT1))
ADDR2 = (HOST2, int(PORT2))
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO, filename='../log/procedure.log', filemode ='w', )
# logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO,filename='received_information.log',filemode = 'w',)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                            串口初始化函数
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def ser_init():
    global s
    s = serial.Serial(COM, Baudrate)
    # s1 = serial.Serial('com1', 115200)
    # s2 = serial.Serial('com2', 115200)

def udp_init():
    global udpServer
    udpServer = socket(AF_INET, SOCK_DGRAM)
    udpServer.bind(ADDR1)
    logging.info(ADDR1)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                        发送指令及测试回复打包函数
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def fasong():# 全部邻居节点回复打包

    phaseID = 1
    sql="SELECT DISTINCT(phaseID) FROM "+TABLE+"_sourse"
    phaselist=Sqlite().select(sql)
    # print(phaselist)
    node_list=[]
    for id in phaselist:
        sql1 = "SELECT DISTINCT(src),phaseID FROM "+TABLE+"_sourse WHERE phaseID='%s'" % id

        results_phase1=Sqlite().select(sql1)
        # print(results_phase1)
        node_list_1 = [(i[0],i[1]) for i in results_phase1]
        node_list.append(node_list_1)
    # print(results1)
    # print(node_list)
    #
    total_frame = []
    total_frame_bytes = []
    for nodelist in node_list:
        for node in nodelist:

                # sql = "SELECT * FROM adjacentNode_phase WHERE src='%s' AND  phaseID=1"% node
                sql = "SELECT * FROM "+TABLE+"_sourse WHERE src='%s' AND  phaseID='%d'"% (node[0],node[1])
                # cursor.execute(sql)
                # results = cursor.fetchall()
                results=Sqlite().select(sql)
                n=10
                results_1=[results[i:i + n]for i in range(0, len(results), n)]

                i=0
                while i<len(results_1):
                    frame=[]
                    head=0x68
                    frame_length = (1 + 2 + 1 + 6 * 1 + 2 * 1 + 2+(6 + 2 + 2+2+1) * len(results_1[i])+1+1)
                    data_length =  6+2+(6 + 2 + 2+2+1) * len(results_1[i])
                    end=0x16
                    if i==len(results_1)-1:
                        order=0b00000010
                    else:
                        order = 0b10000010
                    sumcheck=0x00
                    src_add=results_1[i][0][0].ljust(6,'0')
                    src_flag=results_1[i][0][0].ljust(2,'0')
                    node_address=[]
                    node_flag=[]
                    length=[]
                    snr=1


                    for tur in results_1[i]:
                        node_address.append(tur[1].ljust(6,'0'))
                        node_flag.append(tur[1].ljust(2, '0'))
                        length.append(tur[2])

                    a=node_address[0].split('0')[0]
                    c=node_flag[0].split('0')[0]
                    # print(a,c)
                    frame.append(head)
                    # frame.append(frame_length[0])
                    # frame.append(frame_length[1])
                    frame.append(frame_length)
                    frame.append(order)
                    frame.append(data_length)
                    frame.append(src_add.encode('utf-8'))
                    frame.append(src_flag.encode('utf-8'))



                    for tur in results_1[i]:
                        frame.append(tur[1].ljust(6,'0').encode('utf-8'))
                        frame.append(tur[1].ljust(2, '0').encode('utf-8'))
                        frame.append(int(snr))
                        frame.append(int(tur[2]*10))  #小数乘10
                        frame.append(int(tur[3]))
                        # frame.append(int(2))



                    # print(sum)
                    fmt_1 = '<BHBH6s2s' + '6s2s2HB' * len(results_1[i])
                    data_1 = struct.pack(fmt_1, *frame)

                    sumcheck=CalculateSumcheck(data_1)
                    frame.append(sumcheck)
                    frame.append(end)
                    total_frame.append(frame)
                    fmt='<BHBH6s2s'+'6s2s2HB'*len(results_1[i])+'2B'
                    data=struct.pack(fmt, *frame)
                    total_frame_bytes.append(data)
                    i=i+1

    # print(total_frame)

    i=0
    end_reply = [0x68, 0x06, 0x00, 0x0F, 0x7D, 0x16]  # 全部节点测量完毕回复 2.2.13
    if udpOrserial_flag == 0:
        # udpServer.sendto(data, ADDR2)
        while i <len(total_frame_bytes):
            try:
                udpServer.sendto(total_frame_bytes[i], ADDR2)
                # s.write(total_frame_bytes[i])
                # print('fachuqule')
                logging.info("发送成功")
                i=i+1
                time.sleep(0.005)
                # time.sleep(0.1)
            except:
                # print('排队中')
                logging.warning("排队中")
                time.sleep(0.05)
                i = i + 1
        # end_reply = [0x68, 0x06, 0x00, 0x0F, 0x7D, 0x16]  #全部节点测量完毕回复 2.2.13
        # s.write(bytes(end_reply))
        udpServer.sendto(bytes(end_reply), ADDR2)
        # udpClient.sendto(data, ADDR)
    else:

        while i <len(total_frame_bytes):
            try:
                s.write(total_frame_bytes[i])
                # print('fachuqule')
                logging.info("发送成功")
                i=i+1
                # time.sleep(0.1)
            except:
                # print('排队中')
                logging.warning("排队中")
                time.sleep(0.05)
                i = i + 1
        # end_reply = [0x68, 0x06, 0x00, 0x0F, 0x7D, 0x16]  #全部节点测量完毕回复 2.2.13
        s.write(bytes(end_reply))

def build_send():#上位机查询网络是否建立成功的命令   2.2.10
    global  udpOrserial_flag
    # build_order=bytes([0x68,0x00,0x06,0x0c,0x7a,0x16])
    buildorder = bytes([0x68, 0x06, 0x00, 0x0c, 0x7a, 0x16])
    buildorder_1 = [0x68, 0x0006, 0x0c, 0x7a, 0x16]
    # global buildorder

    fmt='<BHB2B'
    data = struct.pack(fmt, *buildorder_1)
    try:
        if udpOrserial_flag==0:
            udpServer.sendto(data, ADDR2)
            # udpClient.sendto(data, ADDR)
        else:
            s.write(data)
        # s.write(buildorder)

    except:
        # print("错误")
        logging.info("错误")

def build_reply():#模拟回复网络是否建立成功的命令  仅测试用 2.2.11
    global  udpOrserial_flag
    # buildreply_1=bytes([0x68,0x09,0x00,0x0D,0x00,0x00,0x00,0x7e,0x16])#模拟建立失败
    sql="SELECT DISTINCT(src),phaseID FROM "+TABLE
    # sql="SELECT DISTINCT(src),phaseID FROM "+TABLE+"_sourse"
    count=len(Sqlite().select(sql))
    # print(count)
    count_low=count%256
    count_high=int(count/256)%256
    buildreply_2 = [0x68, 0x09, 0x00, 0x0D, 0x01, 0x00, 0x00, 0x00, 0x16]
    buildreply_2[5]=count_low
    buildreply_2[6]=count_high
    buildreply_2[-2]=CalculateSumcheck(bytes(buildreply_2[0:-2]))
    # global build_order
    try:
        if udpOrserial_flag==0:
            # udpClient.sendto(bytes([0x68, 0x08, 0x00, 0x09, 0x00, 0x00, 0x79, 0x16]), ADDR2)
            udpServer.sendto(bytes([0x68, 0x08, 0x00, 0x09, 0x00, 0x00, 0x79, 0x16]), ADDR2)
            time.sleep(0.05)
            # udpClient.sendto(bytes(buildreply_2), ADDR2)
            udpServer.sendto(bytes(buildreply_2), ADDR2)
        else:

            s.write(bytes([0x68, 0x08, 0x00, 0x09, 0x00, 0x00, 0x79, 0x16]))#空闲
            # s.write(bytes([0x68, 0x00, 0x08, 0x09, 0xFF, 0x00, 0x78, 0x16]))#繁忙
            s.write(bytes(buildreply_2)) #建立成功回复
            # s.write(buildreply_1) #建立失败回复
    except:
        # print("错误")
        logging.error("错误")


def cancel_send():#上位机取消操作 2.2.8
    global cancelorder
    try:
        if udpOrserial_flag==0:
            udpServer.sendto(cancelorder,ADDR2)
        else:
            s.write(cancelorder)
    except:
        # print("错误")
        logging.error("错误")



def pack_send_delay(node1,node2): #时延指令打包  2.2.5
    frame = []
    head = 0x68
    frame_length = 0x0012
    end = 0x16
    order = 0x07
    sumcheck = 0x00

    src_add1 = node1.ljust(6, '0')
    src_add2 = node2.ljust(6, '0')

    frame.append(head)
    frame.append(frame_length)
    frame.append(order)
    frame.append(src_add1.encode('utf-8'))
    frame.append(src_add2.encode('utf-8'))

    fmt_1 = '<BHB6s6s'
    data_1 = struct.pack(fmt_1, *frame)

    sumcheck=CalculateSumcheck(data_1)

    frame.append(sumcheck)
    frame.append(end)

    print(frame,len(frame))


    fmt = '<BHB6s6s2B'
    data = struct.pack(fmt, *frame)
    try:
        s.write(data)
    except:
        # print("错误")
        logging.error("错误")

def pack_send_delay_order(node1, node2): #时延指令打包  2.2.5
    frame = []

    head = 0x68
    frame_length = 0x0012
    end = 0x16
    order = 0x07
    sumcheck = 0x00


    frame.append(head)
    frame.append(frame_length)
    frame.append(order)

    for arr in range(len(node1), 0, -2):
        frame.append(int((node1[arr-2:arr]), 16))

    for arr in range(len(node2), 0, -2):
        frame.append(int((node2[arr-2:arr]), 16))

    fmt_1 = '<BHB12B'
    data_1 = struct.pack(fmt_1, *frame)
    sumcheck=CalculateSumcheck(data_1)
    frame.append(sumcheck)
    frame.append(end)

    # print(frame,len(frame))
    fmt = '<BHB12B2B'
    data = struct.pack(fmt, *frame)
    try:
        if udpOrserial_flag==0:
            udpServer.sendto(data,ADDR2)
        else:
            s.write(data)
    except:
        # print("错误")
        logging.error("错误")


def pack_send_am(node1,node2): #幅频指令打包   2.2.3
    frame = []
    head = 0x68
    frame_length = 0x0012
    end = 0x16
    order = 0x05
    sumcheck = 0x00
    src_add1 = node1.ljust(6, '0')
    src_add2 = node2.ljust(6, '0')

    frame.append(head)
    frame.append(frame_length)
    frame.append(order)
    frame.append(src_add1.encode('utf-8'))
    frame.append(src_add2.encode('utf-8'))

    fmt_1 = '<BHB6s6s'
    data_1 = struct.pack(fmt_1, *frame)
    sumcheck=CalculateSumcheck(data_1)

    frame.append(sumcheck)
    frame.append(end)

    fmt = '<BHB6s6s2B'
    data = struct.pack(fmt, *frame)
    try:
        s.write(data)
    except:
        # pass
        logging.error("错误")

def pack_send_am_order(node1, node2): #幅频指令打包   2.2.3
    frame = []
    head = 0x68
    frame_length = 0x0012
    end = 0x16
    order = 0x05
    sumcheck = 0x00

    frame.append(head)
    frame.append(frame_length)
    frame.append(order)

    for arr in range(len(node1) , 0, -2):
        frame.append(int((node1[arr-2:arr]), 16))

    for arr in range(len(node2), 0, -2):
        frame.append(int((node2[arr-2:arr]), 16))

    fmt_1 = '<BHB12B'
    data_1 = struct.pack(fmt_1, *frame)

    sumcheck=CalculateSumcheck(data_1)

    frame.append(sumcheck)
    frame.append(end)

    fmt = '<BHB12B2B'
    data = struct.pack(fmt, *frame)
    try:
        if udpOrserial_flag == 0:
            udpServer.sendto(data, ADDR2)
        else:
            s.write(data)
    except:
        # print("错误")
        logging.error("错误")

def pack_start(par):  #启动测量 2.2.9


    frame = []

    head = 0x68
    frame_length = 18

    end = 0x16
    order = 0x0b
    sumcheck = 0x00

    timeout=par[0]
    replytimes=par[1]
    right_time=par[2]
    aver_delay_times=par[3]
    aver_am_times=par[4]

    beiyong=[0x00,0x00,0x00,0x00,0x00,0x00]

    frame.append(head)
    frame.append(frame_length)
    frame.append(order)
    frame.append(timeout)
    frame.append(replytimes)
    frame.append(right_time)
    frame.append(aver_delay_times)
    frame.append(aver_am_times)
    for arr in beiyong:
        frame.append(arr)


    fmt_1 = '<BHBH10B'
    data_1 = struct.pack(fmt_1, *frame)
    sumcheck=CalculateSumcheck(data_1)
    frame.append(sumcheck)
    frame.append(end)

    fmt = '<BHBH12B'
    data = struct.pack(fmt, *frame)
    # print(data)
    try:
        if udpOrserial_flag == 0:
            udpServer.sendto(data, ADDR2)
        else:
            s.write(data)

    except:
        # print("错误")
        logging.error("错误")


def pack_send_adj(node):  #邻居节点测量指令打包  2.2.1
    frame = []
    head = 0x68
    frame_length = 12
    end = 0x16
    order = 0b00000001
    sumcheck = 0x00
    src_add = node.ljust(6, '0')

    frame.append(head)
    frame.append(frame_length)
    frame.append(order)
    frame.append(src_add.encode('utf-8'))

    fmt_1 = '<BHB6s'
    data_1 = struct.pack(fmt_1, *frame)

    sumcheck=CalculateSumcheck(data_1)
    frame.append(sumcheck)
    frame.append(end)
    fmt = '<BHB6s2B'
    data = struct.pack(fmt, *frame)
    try:
        s.write(data)
    except:
        # print("错误")
        logging.error("错误")

def pack_send_adj_order(node):  #邻居节点测量指令打包  2.2.1
    frame = []
    head = 0x68
    frame_length = 12
    end = 0x16
    order = 0b00000001
    sumcheck = 0x00

    frame.append(head)
    # frame.append(frame_length[0])
    # frame.append(frame_length[1])
    frame.append(frame_length)
    frame.append(order)


    for arr in range(len(node) , 0, -2):
        frame.append(int((node[arr-2:arr]), 16))

    fmt_1 = '<BHB6B'
    data_1 = struct.pack(fmt_1, *frame)
    sumcheck=CalculateSumcheck(data_1)

    frame.append(sumcheck)
    frame.append(end)

    fmt = '<BHB6B2B'
    data = struct.pack(fmt, *frame)
    try:
        if udpOrserial_flag == 0:
            udpServer.sendto(data, ADDR2)


        else:
            # s.write(data)
            s.write(data)
            # end_reply = [0x68, 0x06, 0x00, 0x0F, 0x7D, 0x16]  # 全部节点测量完毕回复 2.2.13
            # s.write(bytes(end_reply))
    except:
        # print("错误")
        logging.error("错误")


def pack_delay_reply(node1,node2): #时延回复打包 仅测试 2.2.6

    # sql = "SELECT length FROM adjacentNode_phase_test WHERE src='%s'and node='%s'" % (node1, node2)
    sql = "SELECT length FROM adjacentNode_1 WHERE src='%s'and node='%s'" % (node1, node2)
    results=Sqlite().select(sql)
    if len(results) == 0:
        delay = 0xffff
    # print(results[0][0])
    else:
        delay = results[0][0]*10
    frame = []

    head = 0x68
    frame_length = 1+2+1+2+6+2+6+2+2+1+1

    end = 0x16

    order = 0x08

    sumcheck = 0x00
    node1_add = node1.ljust(6, '0')
    node1_flag = node1.ljust(2, '0')
    node2_add = node2.ljust(6, '0')
    node2_flag = node2.ljust(2, '0')

    frame.append(head)
    # frame.append(frame_length[0])
    # frame.append(frame_length[1])
    frame.append(frame_length)
    frame.append(order)
    frame.append(2+6+2+6+2+2)

    for arr in range(len(node1) , 0, -2):
        frame.append(int((node1[arr-2:arr]), 16))
    # print(temp)
    frame.append(node1_flag.encode('utf-8'))

    for arr in range(len(node2), 0, -2):
        frame.append(int((node2[arr-2:arr]), 16))

    frame.append(node2_flag.encode('utf-8'))
    frame.append(int(delay))


    fmt_1 = '<BHBH6B2s6B2sH'
    data_1 = struct.pack(fmt_1, *frame)
    sumcheck=CalculateSumcheck(data_1)

    frame.append(sumcheck)
    frame.append(end)


    fmt = '<BHBH6B2s6B2sH2B'
    data = struct.pack(fmt, *frame)

    try:
        if udpOrserial_flag==0:
            udpServer.sendto(data,ADDR2)
        else:
            s.write(data)

    except:
        logging.error("错误")

def pack_am_reply(node1,node2): #幅频回复打包   仅测试 2.2.4
    frame = []

    head = 0x68
    frame_length = 1+2+1+2+2+6+2+6+2+136
    end = 0x16
    order = 0x06
    sumcheck = 0x00
    # node1_add = node1.ljust(6, '0')
    node1_flag = node1.ljust(2, '0')
    # node2_add = node2.ljust(6, '0')
    node2_flag = node2.ljust(2, '0')

    frame.append(head)
    frame.append(frame_length)
    frame.append(order)
    frame.append(2+6+2+6+2+136)
    for arr in range(len(node1), 0, -2):
        frame.append(int((node1[arr - 2:arr]), 16))
    frame.append(node1_flag.encode('utf-8'))

    for arr in range(len(node2), 0, -2):
        frame.append(int((node2[arr - 2:arr]), 16))

    frame.append(node2_flag.encode('utf-8'))
    for i in range(0, 136):
        frame.append(random.randint(0,10))

    fmt_1 = '<BHBH6B2s6B2s136B'
    data_1 = struct.pack(fmt_1, *frame)
    sumcheck=CalculateSumcheck(data_1)

    frame.append(sumcheck)
    frame.append(end)

    fmt = '<BHBH6B2s6B2s136B2B'
    data = struct.pack(fmt, *frame)
    try:
        if udpOrserial_flag == 0:
            udpServer.sendto(data, ADDR2)
        else:
            s.write(data)

    except:
        # print("错误")
        logging.error("错误")


def pack_reply(node):# 邻居节点回复打包 仅测试 2.2.2
    total_frame = []
    total_frame_bytes = []

    # sql = "SELECT * FROM adjacentNode_phase_test WHERE src='%s'" % node
    sql = "SELECT * FROM adjacentNode_1 WHERE src='%s'" % node

    results = Sqlite().select(sql)
    n = 10
    results_1 = [results[i:i + n] for i in range(0, len(results), n)]
    print(results_1,len(results_1))
    #
    i = 0
    while i < len(results_1):
        frame = []

        head = 0x68
        frame_length = (1 + 2 + 1 + 6 * 1 + 2 * 1 + 2 + (6 + 2 + 2 + 2 + 1) * len(results_1[i]) + 1 + 1)
        data_length = 6 + 2 + (6 + 2 + 2 + 2 + 1) * len(results_1[i])
        end = 0x16
        if i == len(results_1) - 1:
            order = 0b00000010
        else:
            order = 0b10000010
        sumcheck = 0x00
        src_add = results_1[i][0][0]
        src_flag = results_1[i][0][0].ljust(2, '0')
        node_address = []
        node_flag = []
        length = []
        snr = 1

        for tur in results_1[i]:
            node_address.append(tur[1].ljust(6, '0'))
            node_flag.append(tur[1].ljust(2, '0'))
            length.append(tur[2]*10)

        frame.append(head)
        frame.append(frame_length)
        frame.append(order)
        frame.append(data_length)

        for arr in range(len(src_add), 0, -2):
            frame.append(int((src_add[arr - 2:arr]), 16))
        frame.append(src_flag.encode('utf-8'))

        for tur in results_1[i]:
            # frame.append(tur[1].ljust(6,'0').encode('utf-8'))
            for arr in range(len(tur[1]), 0, -2):
                frame.append(int((tur[1][arr - 2:arr]), 16))
            frame.append(tur[1].ljust(2, '0').encode('utf-8'))
            frame.append(int(snr))
            frame.append(int(tur[2]*10))
            frame.append(int(1))

        # print(sum)
        fmt_1 = '<BHBH6B2s' + '6B2s2HB' * len(results_1[i])
        data_1 = struct.pack(fmt_1, *frame)

        sumcheck = CalculateSumcheck(data_1)
        frame.append(sumcheck)
        frame.append(end)

        total_frame.append(frame)
        print(frame)

        fmt = '<BHBH6B2s' + '6B2s2HB' * len(results_1[i]) + '2B'
        data = struct.pack(fmt, *frame)
        total_frame_bytes.append(data)
        # print(data)
        i = i + 1

    # print(total_frame)
    try:
        if udpOrserial_flag == 0:
            for array in total_frame_bytes:
                udpServer.sendto(array, ADDR2)
                time.sleep(0.005)
            end_reply = [0x68, 0x06, 0x00, 0x0F, 0x7D, 0x16]  # 全部节点测量完毕回复 2.2.13
            udpServer.sendto(bytes(end_reply), ADDR2)

        else:
            for array in total_frame_bytes:
                s.write(array)
                time.sleep(0.005)
            end_reply = [0x68, 0x06, 0x00, 0x0F, 0x7D, 0x16]  # 全部节点测量完毕回复 2.2.13
            s.write(bytes(end_reply))
    except:
        logging.error("错误")



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                        校验和计算
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def CalculateSumcheck(arr):
    len_data = len(arr)
    sumcheck=0
    for a in range(0, len_data):
        sumcheck = sumcheck + int.from_bytes(arr[a:a + 1], byteorder='little', signed=False)
        sumcheck &= 0xFF
    return sumcheck


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                        帧接收函数
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def receive():#串口接收函数，将接收到的数据存入缓冲区
    global final_flag
    while 1:
        if final_flag != 0:
            sys.exit()
        n=s.inWaiting()
        if n>0:
            data1=s.read(n)
            for arr in data1:
                if rec_queue.full():#队列
                    time.sleep(0.01)
                else:
                    rec_queue.put(arr)

def UDPservice_receive():
    global  BUFSIZE
    global final_flag
    while 1:
        if final_flag != 0:
            sys.exit()
        # time.sleep(2)
        try:
            data,addr= udpServer.recvfrom(int(BUFSIZE))
            # logging.info(data)
            for arr in data:
                    if rec_queue.full():  # 队列
                        time.sleep(0.01)
                    else:
                        rec_queue.put(arr)
            logging.info('接收成功')
        except:
            logging.info("接收结束")
        # time.sleep(0.05)

# def UDPclient_receive():
#     global BUFSIZE
#     global final_flag
#     while 1:
#         # ADDR=1
#         if final_flag != 0:
#             sys.exit()
#         data,addr = udpClient.recvfrom(BUFSIZE)
#         logging.info(data)
#         for arr in data:
#             if rec_queue.full():  # 队列
#                 time.sleep(0.01)
#             else:
#                 rec_queue.put(arr)
#         # print(rec_queue.queue)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                        帧寻找函数
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def findframe(): #以状态机的过程处理缓冲区的数据，以获取完整的数据帧，
  global final_flag,head_flag, time_flag, time1, len_tempdata_old,state
  while 1:
    if final_flag!=0:
        sys.exit()

    len_tempdata = rec_queue.qsize()

    if len_tempdata-len_tempdata_old>0:
        time_flag=0

    while len_tempdata>0:
        if state == 'Findhead':
            # print(rec_queue.queue)
            # print(len_tempdata)

            if rec_queue.queue[0] == 0x68:
                state = 'Findend'

            else:
                rec_queue.get()
                len_tempdata=len_tempdata-1
                # print('未匹配帧头，已删除')

        elif state == 'Findend':
            if  2< len_tempdata:

                arr=[]
                arr.append(rec_queue.queue[1])
                arr.append(rec_queue.queue[2])
                fmt='<H'
                len_1=struct.unpack(fmt,bytearray(arr))[0]

                if len_1 <= len_tempdata:
                    check_end = rec_queue.queue[len_1 - 1]
                    # print(check_end)
                    if check_end == 0x16:

                        temp = [rec_queue.get() for c in range(0, len_1)]
                        handle_data.append(temp)
                        # print('aaaaa%s'%(handle_data))
                        time.sleep(0.005)
                        event_analyze.set()
                        len_tempdata=len_tempdata-len_1
                        state = 'Findhead'
                    else:
                        # print('Error:帧尾不匹配，收到错误帧，已丢弃帧头\n')
                        logging.error("Error:帧尾不匹配，收到错误帧，已丢弃帧头")

                        rec_queue.get()
                        len_tempdata = len_tempdata - 1

                        state = 'Findhead'

                else:
                    # print('Warning:数据不够等待下次接收')
                    if time_flag==0:
                        time1=time.time()
                        time_flag=1
                    time_count=time.time()-time1
                    if time_count>100:
                        print(rec_queue.queue)
                        # print('timeout!time:%f s\n'%time_count)
                        logging.warning('timeout!time:%f s\n'%time_count)

                        while not rec_queue.empty():
                            rec_queue.get()
                            len_tempdata = len_tempdata - 1
                        # print('清空缓冲区！\n')
                        logging.info('清空缓冲区！\n')
                        time_flag = 0
                    time.sleep(0.005)
                    len_tempdata_old=len_tempdata
                    break
            else:
                # print('Warning:数据不够等待下次接收')
                if time_flag == 0:
                    time1 = time.time()
                    time_flag = 1
                time_count = time.time() - time1
                if time_count > 100:
                    # print('timeout!time:%f s\n'%time_count)
                    logging.warning('timeout!time:%f s\n' % time_count)
                    # del rec_data[0:len_tempdata]
                    print(rec_queue.queue)
                    while not rec_queue.empty():
                        rec_queue.get()
                        len_tempdata = len_tempdata - 1
                    # print('清空缓冲区！\n')
                    logging.info('清空缓冲区！\n')
                    final_flag=2
                    time_flag = 0
                time.sleep(0.005)
                len_tempdata_old = len_tempdata
                break



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                          帧解析函数
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def analyzeframe():#处理传过来的完整数据帧进行解析，以状态机的过程
  global state_1, end_flag, final_flag, count_flag
  endtime=0
  first_flag = 0

  while 1:
    if final_flag!=0:
        # udpServer.shutdown(SHUT_RDWR)
        if(udpOrserial_flag==0):
            udpServer.close()
        sys.exit()
    if not(event_analyze.is_set()):
        event_analyze.wait()
    if  first_flag>=2:#判断是不是第二次以上接收到完整的数据包，在第二次接收到之前不会计时，如果不是第一次接收，会不断计时超时（第一次接收为ok回复）
        if end_flag == 0:
            endtime = time.time()
            end_flag = 1
        time_count = time.time() - endtime
        if time_count > 300:
            logging.info('上传结束:%f s\n' % time_count)
            # print('上传结束:%f s\n' % time_count)
            end_flag = 0
            final_flag=1
            first_flag=0
            # break
            sys.exit()

    while len(handle_data)>0:

            end_flag=0
            first_flag = first_flag + 1
            arr=handle_data[0]
            data_len = len(arr)
            i = 0
            while (i < data_len):
              if state_1=='处理帧头':
                if (arr[i] == 0x68):
                    b = struct.unpack('<H', bytearray(arr[i + 1:i + 3]))[0]
                    state_1 = '处理帧尾'

                else:
                    # i = i + 1
                    state_1 = '错误'

              elif state_1 == '处理帧尾':          # print(data_bytes[i + b-1])
                    if (arr[i + b-1] ==0x16):
                        state_1 = '和校验'
                    else:
                        # i=i+1
                        state_1 = '错误'

              elif state_1 == '和校验':
                        datasum = np.sum(arr[i:i+b - 2]) % 256
                        if datasum == arr[i+b- 2]:  # 校验通过
                            state_1 = '处理数据'
                            logging.info('和校验：校验成功\n')
                            # print('和校验：校验成功\n')
                        else:
                            # print('和校验：校验错误\n')
                            logging.info('和校验：校验错误\n')
                            print(arr[i:i + b])
                            state_1 = '错误'

              elif state_1 == '处理数据':
                            if (arr[i + 3] == 0b00000010 or arr[i + 3] == 0b10000010):

                                b = struct.unpack('<H',  bytearray(arr[i + 1:i + 3]))[0]
                                c = struct.unpack('<H',  bytearray(arr[i + 4:i + 6]))[0]

                                fmt = '<BHBH6s2s' + '6s2s2HB' * int((c-8)/13) + '2B'
                                frame_data = struct.unpack(fmt,  bytearray(arr[i:i + b]))
                                    # fmt1='>6s4s' + '6s4sH' * len(results)
                                fmt1 = '>6s2s' + '6s2sH' * int((c-8)/10)
                                fmt1 = '<6s2s' + '6s2s2HB' * int((c-8)/13)
                                real_data=struct.unpack(fmt1,  bytearray(arr[i+6:i+6+c]))

                                # print('解析的数据包：%s' % (frame_data,))
                                logging.info('接收的数据包:%s'%(handle_data[0],))
                                # logging.info('解析的数据包：%s' % (frame_data,))
                                # print('解析的数据段：%s\n'%(real_data,))
                                logging.info('解析的数据段：%s\n'%(real_data,))
                                # print(frame_data)

                                real_data_adj=real_data[2:len(real_data)]
                                real_data_adjnode=[]
                                n = 5
                                for j in range(0, len(real_data_adj), n):
                                    node_add = int.from_bytes(real_data_adj[j], byteorder='little')
                                    node_str_add = str(hex(node_add)).split('x')[1].rjust(12, '0')
                                    real_data_adjnode.append(node_str_add)

                                    node_flag = int.from_bytes(real_data[2], byteorder='little')
                                    node_str_flag = str(hex(node_flag)).split('x')[1].rjust(4, '0')
                                    real_data_adjnode.append(node_str_flag)


                                    # real_data_adjnode.append(float(real_data_adj[j + 2]))
                                    real_data_adjnode.append(real_data_adj[j + 2])
                                    real_data_adjnode.append(float(real_data_adj[j+3]))  #除以10是10ns等于1m/20200119xiugia
                                    real_data_adjnode.append(real_data_adj[j + 4])

                                real_data_src=[]

                                for arr1 in real_data[0:2]:
                                    # real_data_src.append(arr1.decode('utf-8').split('0')[0])#自发自收取消注解
                                    node_add = int.from_bytes(arr1, byteorder='little')
                                    node_str_add = str(hex(node_add)).split('x')[1].rjust(12, '0')
                                    real_data_src.append(node_str_add)


                                adj_list = []             #fangan1
                                adj_list_full = []
                                n=5
                                for j in range(0, len(real_data_adjnode), n):
                                    adj_list_full.append([real_data_src[0:2],real_data_adjnode[j:j + n]])
                                    # adj_list.append((real_data_src[0], real_data_adjnode[j], real_data_adjnode[j + 3]))
                                    adj_list.append((real_data_src[0], real_data_adjnode[j],real_data_adjnode[j+2],real_data_adjnode[j+3],real_data_adjnode[j+4]))
                                    # adj_list.append((real_data_src[0], real_data_adjnode[j],real_data_adjnode[j+3],real_data_adjnode[j+4]))

                                sql2 = "replace INTO "+TABLE+"(src,node,snr,length,phaseID)VALUES (?,?,?,?,?)"

                                flag=SqlUpdate(sql2,adj_list)
                                if flag==1:
                                    count_flag = count_flag + 1
                                    state_1 = '回复'
                                else:
                                    state_1 = '错误'
                                        # db.rollback()
                                # # i = i + b
                                # state_1='回复'



                            elif (arr[i + 3] == 0b00000100 or arr[i + 3] == 0b10000100):

                                    b = struct.unpack('<H', bytearray(arr[i + 1:i + 3]))[0]
                                    c = struct.unpack('>H', bytearray(arr[i + 4:i + 6]))[0]
                                    fmt = '>BHBH6s2s' + '6s2sH' * int((c - 8) / 10) + '2B'
                                    frame_data = struct.unpack(fmt, bytearray(arr[i:i + b]))
                                    # fmt1='>6s4s' + '6s4sH' * len(results)
                                    fmt1 = '>6s2s' + '6s2sH' * int((c - 8) / 10)
                                    real_data = struct.unpack(fmt1, bytearray(arr[i + 6:i + 6 + c]))
                                    logging.info('解析的数据包：%s' % (frame_data,))
                                    logging.info('解析的数据段：%s\n' % (real_data,))
                                    # print(frame_data)
                                    # i=i+b
                                    state_1='回复'

                            elif (arr[i+3]==0b00000001):
                                b = struct.unpack('<H', bytearray(arr[i + 1:i + 3]))[0]
                                fmt = '<BHB6s2B'
                                frame_data = struct.unpack(fmt, bytearray(arr[i:i + b]))
                                # print(frame_data)
                                # fmt1='>6s4s' + '6s4sH' * len(results)
                                fmt1 = '<6s'
                                real_data = struct.unpack(fmt1, bytearray(arr[i + 4:i +10]))

                                logging.info('解析的数据包：%s' % (frame_data,))
                                logging.info('解析的数据段：%s\n' % real_data)
                                # node=real_data[0].decode('utf-8').split('0')[0]
                                node1_add = int.from_bytes(real_data[0], byteorder='little')
                                node1_str_add = str(hex(node1_add)).split('x')[1].rjust(12, '0')

                                logging.info(node1_str_add)
                                pack_reply(node1_str_add)

                                # i = i + b
                                i = i + b
                                state_1 = '处理帧头'

                            elif(arr[i+3]==0x07):
                                b = struct.unpack('<H', bytearray(arr[i + 1:i + 3]))[0]
                                fmt = '<BHB6s6s2B'
                                frame_data = struct.unpack(fmt, bytearray(arr[i:i + b]))

                                fmt1 = '<6s6s'
                                real_data = struct.unpack(fmt1, bytearray(arr[i + 4:-2]))

                                logging.info('解析的数据包：%s' % (frame_data,))
                                logging.info('解析的数据段：%s\n' % (real_data,))

                                node1_add = int.from_bytes(real_data[0], byteorder='little')
                                node1_str_add = str(hex(node1_add)).split('x')[1].rjust(12, '0')
                                node2_add = int.from_bytes(real_data[1], byteorder='little')
                                node2_str_add = str(hex(node2_add)).split('x')[1].rjust(12, '0')


                                logging.info(node1_str_add)
                                logging.info(node2_str_add)
                                # pack_delay_reply(node1,node2)
                                pack_delay_reply(node1_str_add, node2_str_add)

                                # i = i + b
                                i = i + b
                                state_1 = '处理帧头'

                            elif (arr[i + 3] == 0x05):
                                b = struct.unpack('>H', bytearray(arr[i + 1:i + 3]))[0]
                                fmt = '<BHB6s6s2B'
                                frame_data = struct.unpack(fmt, bytearray(arr[i:i + b]))

                                fmt1 = '<6s6s'
                                real_data = struct.unpack(fmt1, bytearray(arr[i + 4:-2]))


                                logging.info('解析的数据包：%s' % (frame_data,))
                                logging.info('解析的数据段：%s\n' % (real_data,))


                                node1_add = int.from_bytes(real_data[0], byteorder='little')
                                node1_str_add = str(hex(node1_add)).split('x')[1].rjust(12, '0')
                                node2_add = int.from_bytes(real_data[1], byteorder='little')
                                node2_str_add = str(hex(node2_add)).split('x')[1].rjust(12, '0')

                                logging.info(node1_str_add)
                                logging.info(node2_str_add)

                                pack_am_reply(node1_str_add, node2_str_add)

                                # i = i + b
                                i = i + b
                                state_1 = '处理帧头'

                            elif (arr[i + 3] == 0x06):
                                b = struct.unpack('<H', bytearray(arr[i + 1:i + 3]))[0]
                                fmt = '<BHBH6s2s6s2s136B2B'
                                frame_data = struct.unpack(fmt, bytearray(arr[i:i + b]))
                                # print(frame_data)
                                # fmt1='>6s4s' + '6s4sH' * len(results)
                                fmt1 = '<H6s2s6s2s136B'
                                real_data = struct.unpack(fmt1, bytearray(arr[i + 4:-2]))
                                # print(1)
                                # print(real_data)
                                # node1 = real_data[0].decode('utf-8').split('0')
                                # print(node1)
                                logging.info('解析的数据包：%s' % (frame_data,))
                                logging.info('解析的数据段：%s\n' % (real_data,))

                                node1_add = int.from_bytes(real_data[1], byteorder='little')
                                node1_str_add = str(hex(node1_add)).split('x')[1].rjust(12, '0')
                                node2_add = int.from_bytes(real_data[3], byteorder='little')
                                node2_str_add = str(hex(node2_add)).split('x')[1].rjust(12, '0')

                                am=real_data[5:]
                                am_str = ','.join(str(i) for i in am)
                                temp = []
                                # temp.append((node1, node2, am_str))#自发自收取消注解
                                temp.append((node1_str_add, node2_str_add, am_str))

                                # sql2 = "replace INTO fupin(src, node, fupin)VALUES (%s, %s, %s)"
                                sql2 = "replace INTO "+fupinTABLE+"(src, node, fupin)VALUES (?, ?, ?)"

                                flag=SqlUpdate(sql2,temp)
                                if flag==1:
                                    final_flag = 1
                                else:
                                    final_flag=2

                                state_1 = '回复'

                            elif(arr[i+3]== 0x08):
                                b = struct.unpack('<H', bytearray(arr[i + 1:i + 3]))[0]
                                fmt = '<BHBH6s2s6s2sH2B'
                                frame_data = struct.unpack(fmt, bytearray(arr[i:i + b]))

                                fmt1 = '<H6s2s6s2sH'
                                real_data = struct.unpack(fmt1, bytearray(arr[i + 4:-2]))

                                logging.info('解析的数据包：%s' % (frame_data,))
                                logging.info('解析的数据段：%s\n' % (real_data,))

                                # node2 = real_data[2].decode('utf-8').split('0')[0]
                                # print(real_data[1])
                                node1_add = int.from_bytes(real_data[1], byteorder='little')
                                node1_flag = int.from_bytes(real_data[2], byteorder='little')
                                node1_str_add = str(hex(node1_add)).split('x')[1].rjust(12, '0')
                                node1_str_flag = str(hex(node1_flag)).split('x')[1].rjust(4, '0')
                                node2_add = int.from_bytes(real_data[3], byteorder='little')

                                node2_flag = int.from_bytes(real_data[4], byteorder='little')
                                node2_str_add = str(hex(node2_add)).split('x')[1].rjust(12, '0')
                                node2_str_flag = str(hex(node2_flag)).split('x')[1].rjust(4, '0')

                                length=float(real_data[5])  #10ns等于1m
                                temp=[]
                                temp.append((node1_str_add,node2_str_add,length))

                                sql2 = "replace INTO "+delayTABLE+"(src,node, length)VALUES (?, ?, ?)"

                                flag = SqlUpdate(sql2, temp)
                                if flag == 1:
                                    final_flag = 1
                                else:
                                    final_flag = 2

                                # i = i + b
                                state_1='回复'
                                # print(state_1)

                            elif (arr[i + 3] == 0x09):
                                b = struct.unpack('<H', bytearray(arr[i + 1:i + 3]))[0]
                                fmt = '>BHB2B2B'
                                fmt = '<BHB2B2B'
                                frame_data = struct.unpack(fmt, bytearray(arr[i:i + b]))
                                # print(frame_data)
                                # fmt1='>6s4s' + '6s4sH' * len(results)
                                fmt1 = '2B'
                                real_data = struct.unpack(fmt1, bytearray(arr[i + 4:-2]))
                                # print(real_data)

                                logging.info('解析的数据包：%s' % (frame_data,))
                                logging.info('解析的数据段：%s\n' % (real_data,))
                                if real_data[0]==0x00:
                                    logging.info('系统空闲')

                                elif real_data[0]==0xFF:
                                    logging.info('系统繁忙')  #上位机需要重新下达该指令，才能确保指令被执行，或者下达“取消当前操作的命令”，强行中断当前操作
                                    final_flag=-1
                                    sys.exit()

                                i = i + b
                                state_1 = '处理帧头'
                            elif (arr[i + 3] == 0x0B):
                                b = struct.unpack('<H', bytearray(arr[i + 1:i + 3]))[0]
                                fmt = '<BHBH12B'
                                frame_data = struct.unpack(fmt, bytearray(arr[i:i + b]))
                                logging.info('解析的数据包：%s' % (frame_data,))
                                fasong()
                                i = i + b
                                state_1 = '处理帧头'

                            elif (arr[i + 3] == 0x0C):
                                b = struct.unpack('<H', bytearray(arr[i + 1:i + 3]))[0]
                                fmt = '<BHB2B'
                                frame_data = struct.unpack(fmt, bytearray(arr[i:i + b]))
                                # print(frame_data)
                                logging.info('解析的数据包：%s' % (frame_data,))
                                build_reply()
                                i = i + b
                                state_1 = '处理帧头'

                            elif (arr[i + 3] == 0x0D):
                                b = struct.unpack('<H', bytearray(arr[i + 1:i + 3]))[0]
                                fmt = '<BHBBH2B'
                                frame_data = struct.unpack(fmt, bytearray(arr[i:i + b]))
                                # print(frame_data)
                                fmt1 = '<BH'
                                real_data = struct.unpack(fmt1, bytearray(arr[i + 4:-2]))
                                logging.info('解析的数据包：%s' % (frame_data,))
                                logging.info('解析的数据段：%s\n' % (real_data,))
                                if real_data[0]==0x01:
                                    logging.info('网络建立成功')
                                    global node_num
                                    node_num=real_data[1]
                                    final_flag = 1

                                if real_data[0]==0x00:
                                    logging.info('网络建立失败')  #
                                    final_flag = 2
                                state_1 = '回复'

                            elif (arr[i + 3] == 0x0F):
                                b = struct.unpack('<H', bytearray(arr[i + 1:i + 3]))[0]
                                fmt = '<BHB2B'
                                frame_data = struct.unpack(fmt, bytearray(arr[i:i + b]))
                                # print(frame_data)
                                logging.info('解析的数据包：%s' % (frame_data,))
                                logging.info('全部节点测量结束\n')
                                final_flag = 1
                                state_1 = '回复'

                            else:
                                state_1 = '错误'

              elif state_1=='回复':
                  try:
                    if udpOrserial_flag==0:
                        udpServer.sendto(reply_order, ADDR1)
                    else:
                        s.write(reply_order)   #2.2.12 发送已收到ok指令
                    logging.info('已回复')
                    i = i + b
                    state_1 = '处理帧头'

                  except:
                      logging.error('回复失败')
                      # state_1 = '错误'
                      # pass



              elif state_1 == '错误':
                  i = i + b
                  state_1 = '处理帧头'
                  break

            del handle_data[0]

            # print('处理区数据：%s'%handle_data)#剩余待处理数据：bytearray(b'hh\x00\x1e\x82\x00\x16O20000O200O10000O100\x00\x04\x00\x16h\x00~\x82\x00vP10000P1h\x00~\x82\x00vP10000P100D10000D100\x03\xf3E10000E100\x03\xf0F10000F100\x03
            # print('缓冲区数据：%s\n' % rec_queue.queue)
    event_analyze.clear()



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                            数据库函数
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def SqlUpdate(sql,list):

        # 执行sql语句
        logging.info(
            '------------------------- %s正在上传数据库 -------------------------------' %
            list[0][0])
        # cursor.executemany(sql2,temp)
        #     # 提交到数据库执行
        # db.commit()
        flag=Sqlite().insertmany(sql, list)
        logging.info(list)
        if flag==1:
            logging.info('--------------------------- %s上传成功 -----------------------------------\n' %
                  list[0][0])
        else:
        # Rollback in case there is any error
            logging.error('--------------------------- %s上传失败 -----------------------------------\n' %
                  list[0][0])
        return flag




"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                            线程函数
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def StartThread(fct_a, a_args, fct_b, b_args, fct_c, c_args, fct_d, d_args):
    t1=threading.Thread(target=fct_a,args=a_args)
    t2=threading.Thread(target=fct_b,args=b_args)
    t3=threading.Thread(target=fct_c,args=c_args)
    t4=threading.Thread(target=fct_d,args=d_args)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    logging.info('线程1%s'%(t1.is_alive()))
    logging.info('线程2%s'%(t2.is_alive()))
    logging.info('线程3%s'%(t3.is_alive()))
    logging.info('线程4%s'%(t4.is_alive()))



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                        指令函数
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def adj_measure_order(node):#邻居节点测试用例，输入：节点标志 ，传给发送函数进行串口指令打包发送 2.2.1
    global final_flag,udpOrserial_flag
    udpOrserial_flag = int(readConfigurationFile("Serial").getCon("serial_or_udp"))
    if (udpOrserial_flag == 0):
        udp_init()
        StartThread(pack_send_adj_order, (node, ), UDPservice_receive, (), findframe, (), analyzeframe, ())

    else:
        ser_init()
        StartThread(pack_send_adj_order, (node,), receive, (), findframe, (), analyzeframe, ())
        s.close()
    # ser_init()
    # StartThread(pack_send_adj_order, (node,), receive, (), findframe, (), analyzeframe, ())
    # s.close()
    if final_flag == 1:#通过全局变量控制线程关闭
            logging.info('邻居节点信息上传数据库完成')
            return_flag = final_flag
            final_flag = 0
            s.close()
            return return_flag

    elif final_flag == -1:
            logging.warning('繁忙')
            return_flag = final_flag
            final_flag = 0
            return return_flag


def delay_measure_order(node1,node2):#时延测试用例  输入：两个节点的标志 2.2.5
    global final_flag,udpOrserial_flag
    udpOrserial_flag = int(readConfigurationFile("Serial").getCon("serial_or_udp"))
    if(udpOrserial_flag==0):
        udp_init()
        StartThread(pack_send_delay_order, (node1, node2), UDPservice_receive, (), findframe, (), analyzeframe, ())

    else:
        ser_init()
        StartThread(pack_send_delay_order, (node1, node2), receive, (), findframe, (), analyzeframe, ())
        s.close()

    if final_flag == 1:
            logging.info('时延信息测量成功')
            return_flag = final_flag
            final_flag = 0
            return return_flag

    elif final_flag == -1:
            logging.warning('繁忙')
            return_flag = final_flag
            final_flag = 0
            return return_flag

    else:
            logging.error('错误')
            return_flag = final_flag
            final_flag = 0
            return return_flag

def am_measure_order(node1,node2):#幅频测试用例  输入：两个节点的标志 2.2.3
    global final_flag,udpOrserial_flag
    udpOrserial_flag = int(readConfigurationFile("Serial").getCon("serial_or_udp"))
    if (udpOrserial_flag == 0):
        udp_init()
        StartThread(pack_send_am_order, (node1, node2), UDPservice_receive, (), findframe, (), analyzeframe, ())

    else:
        ser_init()
        StartThread(pack_send_am_order, (node1, node2), receive, (), findframe, (), analyzeframe, ())
        s.close()
    # ser_init()
    # StartThread(pack_send_am_order, (node1, node2), receive, (), findframe, (), analyzeframe, ())
    # s.close()

    if final_flag == 1:
            logging.info('幅频信息测量成功')
            return_flag = final_flag
            final_flag = 0
            return return_flag
            # time.sleep(0.5)
    elif final_flag == -1:
            logging.warning('繁忙')
            return_flag = final_flag
            final_flag = 0
            return return_flag

def start_measure_order(par):#启动测量用例   2.2.9
    global final_flag,count_flag,udpOrserial_flag
    count_flag=0

    #20200120 测量前清除数据库！
    sql = "DELETE FROM "+TABLE+" WHERE 1 = 1"
    Sqlite().delete(sql)
    logging.info( "database has been cleared!")
    # ser_init()
    # StartThread(pack_start, (par,), receive, (), findframe, (), analyzeframe, ())
    # s.close()
    udpOrserial_flag = int(readConfigurationFile("Serial").getCon("serial_or_udp"))
    if (udpOrserial_flag == 0):
        udp_init()
        StartThread(pack_start, (par, ), UDPservice_receive, (), findframe, (), analyzeframe, ())

    else:
        ser_init()
        StartThread(pack_start, (par,), receive, (), findframe, (), analyzeframe, ())
        s.close()

    if final_flag == 1:
            logging.info('时延信息测量成功')
            return_flag = final_flag
            final_flag = 0
            return return_flag
            # time.sleep(0.5)
    elif final_flag == -1:
            logging.warning('繁忙')
            return_flag = final_flag
            final_flag = 0
            return return_flag

def build_order():#上位机查询网络是否建立成功 2.2.10
    global final_flag,udpOrserial_flag
    # ser_init()
    # StartThread(build_send, (), receive, (), findframe, (), analyzeframe, ())
    # s.close()
    udpOrserial_flag = int(readConfigurationFile("Serial").getCon("serial_or_udp"))
    if (udpOrserial_flag == 0):
        udp_init()
        StartThread(build_send, (), UDPservice_receive, (), findframe, (), analyzeframe, ())

    else:
        ser_init()
        StartThread(build_send, (), receive, (), findframe, (), analyzeframe, ())
        s.close()
    if final_flag == 1:
            logging.info('连接建立成功')
            return_flag = final_flag
            final_flag = 0
            return return_flag,node_num
            # time.sleep(0.5)
    elif final_flag == -1:
            logging.warning('繁忙')
            return_flag = final_flag
            final_flag = 0
            return return_flag,0

    elif final_flag == 2:
            logging.error('建立失败')
            return_flag = final_flag
            final_flag = 0
            return return_flag, 0

def cancel_order():#上位机进行取消操作  2.2.8
    global final_flag
    ser_init()
    StartThread(cancel_send, (), receive, (), findframe, (), analyzeframe, ())
    s.close()

    if final_flag == 1:
            logging.info('已发送取消指令')
            return_flag=final_flag
            final_flag = 0
            return  return_flag
            # time.sleep(0.5)
    elif final_flag == -1:
            logging.warning('繁忙')
            return_flag = final_flag
            final_flag = 0
            return return_flag

def build_udp():
    udp_init()
    t1 = threading.Thread(target=build_send)
    # t2 = threading.Thread(target=UDPclient_receive)
    t3 = threading.Thread(target=UDPservice_receive)
    t4 = threading.Thread(target=analyzeframe)
    t5 = threading.Thread(target=findframe)

    t1.start()
    # t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    # t2.join()
    t3.join()
    t4.join()
    t5.join()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                                            测试指令
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':
    logging.info("Begin")
    #  测试指令
    # a,b=build_order()
    # print(a,b)
    # cancel_order()
    # start_measure_order([2000,3,20,10,4])
    # adj_measure_order('000000000003')
    # adj_measure_order('303030303052')
    # delay_measure_order('000000000000','000000000003')
    # am_measure_order('000000000000','000000000003')
    # build_udp()
    logging.info("Finished")
