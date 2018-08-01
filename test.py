#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from multiprocessing import Pool
import os
import time
import random

def worker(msg):
	t_start=time.time() #记录从1970.0.0到现在的秒数
	print("%s 开始执行，进程号为%d"%(msg,os.getpid()))
	#random.random()随机生成0~1之间的浮点数
	time.sleep(random.random()*2)
	t_stop=time.time()
	print(msg,"执行完毕，耗时%0.2f"%(t_stop-t_start))

if __name__=="__main__":
	po=Pool(9) #定义一个进程池，最大进程数3
	for i in range(0,10):
		po.apply_async(worker,(i,))
	print("---start---")
	po.close()#关闭进程池，关闭后po不再接受新的请求
	po.join()#等待po中所有子进程执行完成，必须放在close后
	print("-----------end----------")
'''
---start---
0 开始执行，进程号为11856
0 执行完毕，耗时1.19
4 开始执行，进程号为11856
4 执行完毕，耗时1.97
2 开始执行，进程号为12104
2 执行完毕，耗时0.73
3 开始执行，进程号为12104
3 执行完毕，耗时0.63
6 开始执行，进程号为12104
6 执行完毕，耗时1.86
1 开始执行，进程号为10656
1 执行完毕，耗时1.38
5 开始执行，进程号为10656
5 执行完毕，耗时0.36
7 开始执行，进程号为10656
7 执行完毕，耗时0.76
8 开始执行，进程号为10656
8 执行完毕，耗时0.15
9 开始执行，进程号为10656
9 执行完毕，耗时1.98
-----------end----------
'''
