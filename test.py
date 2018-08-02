# -*- encoding: utf-8 -*-
import pickle
# from powerline.segments.vim import tab
table = {'a':[1,2,3],'b':[5,6,7],'c':['e','r','t']}
# table =[1,2,3]
print (type(table))
mydb = open('ttt','rb')
# pickle.dump(table,mydb)
print pickle.load(mydb)