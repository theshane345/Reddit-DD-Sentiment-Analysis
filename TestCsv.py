import csv
import pandas as pd
import itertools


list1 =[]
with open('Ticker/amex.csv','rt')as f:
    for row in f:
        list1.append(row.split(',')[0])
res = list1[1:]  
#print(str(res))

list2 =[]
with open('Ticker/nyse.csv','rt')as f:
    for row in f:
        list2.append(row.split(',')[0])
res2 = list2[1:]  
#print(str(res2))

list3 =[]
with open('Ticker/nasdaq.csv','rt')as f:
    for row in f:
        list3.append(row.split(',')[0])
res3 = list3[1:]  
#print(str(res3[1]))

suprList=str(res)+str(res2)+str(res3)

print(suprList[908])



# f=open('output.txt','w')
# for ele in list1:
#     f.write(ele+'\n')
# for ele in list2:
#     f.write(ele+'\n')
# for ele in list3:
#     f.write(ele+'\n')

# f.close()

# lst6=[]
# f=open('output.txt','r')

# for line in f:
#     result = f.readlines()
#     test = str(result).replace('\\n', '')
#     lst6.append(test)
# print (lst6[0])