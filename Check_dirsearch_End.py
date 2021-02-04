#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author:zjj
@file:ClearMydic.py
@time:2021/01/22
"""
import os
import requests
import time
import re
import urllib.request
from threading import Thread
import sys


def new_mydic(filename1):
	if os.access("mydic_end.txt",os.F_OK):
		return
	else:
		f1 = open(filename1,'r+',encoding='gb18030',errors='ignore')
		f2 = open('mydic_end.txt','w+')
		for line1 in f1.readlines():
			line2 = line1.strip()+',0'+'\n'
			f2.write(line2)
		
def deal_result(filename):
	result=[]
	count=[]
	with open('mydic_end.txt','r') as f: #读取权值文件的域名和权值，格式为xxx,1
		for line in f:
			tmp = line.split(",")
			result.append(tmp[0])
			count.append(int(tmp[1].strip()))
	with open(filename,'r') as all_re: #读取爆破结果，更新权值
		for line in all_re:
			try:
				if line.startswith('200'):
					newline = re.findall('http.*',line)
					newdic1 = re.findall(':\d\d.*/.*',newline[0])		
					newdic2 = re.findall('/.*', newdic1[0])
					alph = newdic2[0][1:]
					result1 = set(result)
					if alph in result1:
						count[result.index(alph)] +=1
					else:
						f3 = open('mydic.txt','a')
						f3.write(alph+'\n')
						f4 = open('mydic_end.txt','a')
						f4.write(alph+',1\n')
						count[result.index(alph)] +=1
			except ValueError:
				print("当前路径字典中不存在，已成功写入字典")
	dic ={}
	for i in range(len(result)): #写进字典并排序，便于更新字典权值文件
		dic[result[i]] = count[i]
	dic_r = sorted(dic.items(), key=lambda x:x[1],reverse=True)
	f = open('mydic_end.txt','w') # 更新权值文件
	for i in dic_r:
		st = i[0] + ',' + str(i[1]) + "\n"
		#st = i[0] + "\n" #生成无权置新字典
		f.write(st)
	f.close()

def check_record_file():
	if os.path.exists("record_num.txt"): #如果记录文件存在，将存储的值+1
		print("[+] Record exists.")
		with open("record_num.txt",'r') as f :
			num = f.read().strip()
		with open("record_num.txt",'w') as f :
			f.write(str(int(num)+1)+"\n")
	else:
		f = open("record_num.txt","w") #记录文件不存在，说明是第一次爆破
		f.write("1"+"\n")
		f.close()

def check_if_update():
	with open("record_num.txt",'r') as f : #打开record_num文件读取已运行次数
		num = int(f.read().strip())
	if num < 5: #如果小于20次，则不更新
		return
	else: #如果等于20次则更新
		os.system("del /a /f /s /q record_num.txt") # 删除记录文件，下次运行时生成新的
		print("[+] Update data")
		result = []
		count = 0
		for index, line in enumerate(open("mydic_end.txt",'r')):
			count += 1
		record_i = 0.0
		with open("mydic_end.txt",'r') as f: #读取权值前80%的记录
			for line in f:
				record_i=record_i+1
				tmp = line.split(",")
				result.append(tmp[0])
				if record_i/count >= 0.9:
					break
		with open("newdic.txt","r") as f : #读取词频分析的结果文件记录，总数为源文件的30%
			for line in f:
				tmp = line.split(",")
				if tmp[0] in result: #若有重复，则跳过该记录
					#print(tmp)
					continue
				else:
					record_i = record_i + 1
					result.append(tmp[0].rstrip("\n"))
					#print(result)
					#exit()
					if record_i/count >= 1.0:
						break
		f = open('mydic_new.txt','w') #更新权值文件
		for i in result:
			#st = i + ",0\n"
			st = i + "\n" #生成根据权值排序的新字典
			f.write(st)
		f.close()

new_mydic('mydic.txt')     #为字典加上权重

deal_result('log.txt') #设置权值
		
check_record_file() #检测记录文件

check_if_update()

