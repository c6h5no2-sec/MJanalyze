from time import time
import pandas as pd
import os
import csv
import numpy as np

def readCsv(path):
    #读取账单文件
    data = pd.read_csv(path,encoding = 'utf-8',header=None,error_bad_lines = False)
    data = pd.DataFrame(data)
    return data

def userName(data):
    #获得该账单用户名
    username = data.iloc[1,0][6:-1]
    return username

def getWechatRedPacket(username,data,path):
    #获得清洗后的账单,去除私发红包
    data = pd.read_csv(path,encoding = 'utf-8',skiprows = range(16),error_bad_lines = False)
    data['交易时间'] = pd.to_datetime(data['交易时间'],format=("%Y-%m-%d"))
    data.insert(loc=0,column='当前用户',value=username)
    table = data.loc[(data['交易类型'].str.contains('微信红包')) & (data['交易类型'].str.contains('单发') == False)]
    #table = data[data['交易类型'].isin(['微信红包','微信红包（群红包）'])]
    #isin参数是list
    return table

def rangePacket(table):
    time = table['交易时间']
    print(time[1]+5)
    for i in time:
        pass
        #因为账单本身有从大到小的顺序，如果上减下大于时间范围，则指针往后移动一位再与下一位比，如果小于，则存储，并且再拿下一个与下下一个比，也就是说，如果上减下，小于，存上，继续


class UnionFindSet():
    def __init__(self, data_list):
        # 初始化两个字典，分别保存节点的父节点（并查集）和保存父节点的大小
        self.father_dict = {}  # father_dict[i]表示节点i的父节点
        self.size_dict = {}  # size_dict[i]表示节点i的后代节点个数'
        self.father_time = {} # father_time表示节点i的父节点所存的时间
        # 初始化节点，将节点的父节点设为自身，size设为1
        for node in data_list:
            self.father_dict[node] = node
            self.size_dict[node] = 1
            #self.father_time[node] = node[2]
        print("初始化完毕")
 
    # 递归查找根节点（父节点是自己的节点）
    def find(self, node):
        # 获取节点的父节点
        father = self.father_dict[node]
        #print(father)
        #time = self.father_time[node]
        # 查找当前节点的父节点，直到父节点是其自己
        if(node != father):
            # 在降低树高优化时，确保父节点大小字典正确
            if father != self.father_dict[father]:
                self.size_dict[father] -= 1
            # 递归查找节点的父节点，直到根节点
            father = self.find(father)
        # 在查找父节点的时候，顺便把当前节点移动到父节点上面（优化操作）
        self.father_dict[node] = father
        #self.father_time[node] = father[2]
        return father
 
    # 查看两个节点是不是在一个集合里面
    def is_same_set(self, node_a, node_b):
        # 获取两个节点的父节点并比较父节点是否是同一个
        return self.find(node_a) == self.find(node_b)
 
    # 将两个集合合并在一起（只需合并根节点），size_dict大吃小（尽可能降低树高）
    def union(self, node_a, node_b):
        if node_a is None or node_b is None:
            print('wrong')
            return
        # 找到两个节点各自的根节点
        a_root = self.find(node_a)
        b_root = self.find(node_b)
 
        # 两个节点不在同一集合中，则合并两个集合
        if(a_root != b_root):
            # 获取两个集合根节点的大小
            a_set_size = self.size_dict[a_root]
            b_set_size = self.size_dict[b_root]
            # 判断两个集合根节点大小，并进行合并（大吃小）
            if(a_set_size >= b_set_size):
                # 合并集合
                self.father_dict[b_root] = a_root
                # 更新大小
                self.size_dict[a_root] = a_set_size + b_set_size
            else:
                # 合并集合
                self.father_dict[a_root] = b_root
                # 更新大小
                self.size_dict[b_root] = a_set_size + b_set_size


def table1(path):
    #######
    #单表合并
    a = 1
    data = readCsv(path)
    username = userName(data)
    #itertuples遍历每行为一个命名元组
    table = getWechatRedPacket(username,data,path).itertuples()
    table2 = getWechatRedPacket(username,data,path).itertuples()
    table3 = getWechatRedPacket(username,data,path).itertuples()
    #rangePacket(table)
    # 并查集
    modle = UnionFindSet(table)
    print("开始合并")
    for i in table2:
        #为什么会这样我也不懂，操
        #目的是找到间隔时间小的，合并在一起
        #print(i)
        if a == 1:
            a+=1
            temp = i
            continue
        #间隔时间差
        #print(str(temp[2])+"-"+str(i[2]))
        duration = abs((temp[2] - i[2])).seconds/60
        if duration <= 5:
            #print(str(temp[0])+"与" + str(i[0]))
            node1, node2 = temp, i
            modle.union(node1, node2)
        a+=1
        temp = i
    """
    #遍历查询该表中的结果 
    for i in table3:
        #i为原始数据
        #father为合并后的数据
        father = modle.find(i)
        #print(father)
        #print(i)
        print("当前用户为:{},账单序号为:{}；时间是:{},基础时间：{}；组局编号：{}".format(father[1],i[0],i[2],father[2],father[0]))
    """
    return modle

def test23():
    """
    path = 'D:\\win\\Desktop\\test\\微信支付账单(20220912-202209191).csv'
    path2 = 'D:\\win\\Desktop\\test\\test.csv'
    data = readCsv(path)
    data2 = readCsv(path2)
    username = userName(data)
    username2 = userName(data2)
    #itertuples遍历每行为一个命名元组
    table = getWechatRedPacket(username,data,path)
    table2 = getWechatRedPacket(username2,data2,path2)
    table3 = pd.concat([table,table2],axis=0,ignore_index = True).sort_values(by='交易时间',ascending=False).itertuples()
    table4 = pd.concat([table,table2],axis=0,ignore_index = True).sort_values(by='交易时间',ascending=False).itertuples()
    table5 = pd.concat([table,table2],axis=0,ignore_index = True).sort_values(by='交易时间',ascending=False).itertuples()
    #print(table3)
    """
    # 将该文件夹下的所有文件名存入列表
    csv_name_list = os.listdir('D:\\win\\Desktop\\test')
    # 获取列表的长度
    length = len(csv_name_list)

    # 循环遍历列表中各个CSV文件名，并完成文件拼接
    all_data_frames = []
    for csv in csv_name_list:
        rootPath = "D:\\win\\Desktop\\test\\"
        #csv ='微信支付账单(20220310-20220320).csv'
        path = rootPath + csv
        data_frame = readCsv(path)
        username = userName(data_frame) 
        data = getWechatRedPacket(username,data_frame,path) 
        all_data_frames.append(data)
    data_frame_concat = pd.concat(all_data_frames,axis=0,ignore_index=True).sort_values(by='交易时间',ascending=False)
    data_frame_concat.to_csv('server_csvfile.csv',index=False)
    print("已按照顺序生成出总表")
    table = data_frame_concat.itertuples()
    table2 = data_frame_concat.itertuples()
    table3 = data_frame_concat.itertuples()
    modle = UnionFindSet(table)
    print("开始合并")
    a=1
    for i in table2:
        #为什么会这样我也不懂，操
        #目的是找到间隔时间小的，合并在一起
        #print(i)
        if a == 1:
            a+=1
            temp = i
            continue
        #间隔时间差
        #print(str(temp[2])+"-"+str(i[2]))
        duration = abs((temp[2] - i[2])).seconds/60
        if duration <= 5:
            #print(str(temp[0])+"与" + str(i[0]))
            node1, node2 = temp, i
            modle.union(node1, node2)
        a+=1
        temp = i
    #遍历查询该表中的结果 
    for i in table3:
        #i为原始数据
        #father为合并后的数据
        father = modle.find(i)
        #print(father)
        #print(i)
        print("当前用户为:{};账单序号为:{}；时间是:{},基础时间：{}；交易对象：{}；收支类型：{}；涉及金额：{};组局编号：{};".format(i[1],i[0],i[2],father[2],i[4],i[6],i[7],father[0]))
    return modle


if __name__=="__main__":
    test23()
    """
    path = 'D:\\win\\Desktop\\test\\微信支付账单(20220912-202209191).csv'
    path2 = 'D:\\win\\Desktop\\test\\test.csv'
    modle1 = table1(path)
    data = readCsv(path)
    username = userName(data)
    table3 = getWechatRedPacket(username,data,path).itertuples()
    for i in table3:
        #i为原始数据
        #father为合并后的数据
        father = modle1.find(i)
        #print(father)
        #print(i)
        print("当前用户为:{},账单序号为:{}；时间是:{},基础时间：{}；组局编号：{}".format(father[1],i[0],i[2],father[2],father[0]))
    """