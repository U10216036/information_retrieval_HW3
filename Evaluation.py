# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 16:24:44 2018

@author: owner
"""
import pandas as pd
import numpy as np
#import seaborn as sns 
import re
#import math
#import matplotlib.pyplot as plt

percision_final = [0,0,0,0,0,0,0,0,0,0,0]
APList = []
#DCG_List = [0]*2265
#IDCG_List = [0]*2265
#NDCG_List = []

def getNumofResultsTrainSetQuery(path,startRow):
    ResultsTrainSet = pd.read_csv(path,sep = '\n',encoding = 'utf-8',skiprows = startRow,nrows = 0)
    str = list(ResultsTrainSet.columns.values)
    ReStr = re.sub(r'\s+', " ", str[0])
    items = ReStr.strip().split(' ')
    numOfResultsQuery = items[3]
    #print (numOfResultsQuery)    
    return int(numOfResultsQuery)
def readResultsTrainSetQuery(path,startRow,numofRows):
    ResultsTrainSet = pd.read_csv(path,sep = '\s+',encoding = 'utf-8',skiprows = startRow ,nrows = numofRows)
    QRlist = np.array(ResultsTrainSet.iloc[:, [0]])
    #print(QRlist.size)
    return QRlist
    
   
    
def getNumofAssessmentTrainSet(path,startRow):
    AssessmentTrainSet = pd.read_csv(path,sep = '\n',encoding = 'utf-8',skiprows = startRow,nrows = 0)
    strR = list(AssessmentTrainSet.columns.values)
    ReStr = re.sub(r'\s+', ' ', strR[0])
    itemsR = ReStr.strip().split(' ')
    numOfAssessmentQuery = itemsR[3]
    #print (numOfAssessmentQuery)  
    return int(numOfAssessmentQuery)

def readNumofAssessmentTrainSet(path,startRow,numofRows):
    AssessmentTrainSet = pd.read_csv(path,sep = '\s+',encoding = 'utf-8',skiprows = startRow ,nrows = numofRows)
    QAlist = np.array(AssessmentTrainSet.iloc[:, [0]])
    #print(QAlist.size)
    return QAlist
'''
def compare(percision_List,recall_List):
    recall = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1]
    sort_List = []
    percision_tmp = []
    #print(len(recall))
    for i in range(len(recall) -1):
        for k in range(len(recall_List)):
            if(recall_List[k]>=recall[i]) and (recall_List[k]<recall[i+1]) :
                sort_List.append(percision_List[k])
            else:
                sort_List.append(0)
        sort_List.sort(reverse=True)
        #print(i,sort_List)
        percision_tmp.append(sort_List[0])
        #print(percision_tmp) 
        sort_List.clear()
    clearZero(percision_tmp)
        
                 
def clearZero(percision_tmp):
    zero_list =[]
    for i in range(len(percision_tmp)):
        if(percision_tmp[i] == 0):
            zero_list.append(i) 
        elif(percision_tmp[i] != 0):
            #print(len(zero_list))
            for k in range(len(zero_list)):
                percision_tmp[zero_list[k]] = percision_tmp[i]
            zero_list.clear()               
    #print(percision_tmp)  
    addToFinalPercisionList(percision_tmp)
    
def addToFinalPercisionList(percision_tmp):
    for i in range(len(percision_final)):
        percision_final[i]+=percision_tmp[i]
    #print(percision_final)  
'''  
'''
def plot():
    sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
    for i in range(len(percision_final)):
        percision_final[i]= (percision_final[i]/16)*100
    print(percision_final)
    recall = [0,10,20,30,40,50,60,70,80,90,100]
    query_df = pd.DataFrame(
        {"Recall": recall,
         "Percision": percision_final
        }
    )
    sns.factorplot(data = query_df, x="Recall", y="Percision", ci = None,color="#5599FF")
    plt.show()               
'''                 
def calculateAP(percision_List):
    sum = 0
    count = 0
    for i in range(len(percision_List)):
        sum += percision_List[i]
        count+=1
    #print(count)
    APList.append(sum/count)
    
'''
def calculateDCGandIDCG(gain_List):
    DCG_List_tmp = gain_List[:]
    IDCG_List_tmp = gain_List[:]
    IDCG_List_tmp.sort(reverse = True)
    
    for i in range(1,len(IDCG_List_tmp)):
        if(i==1):
            DCG_List_tmp[i]+=DCG_List_tmp[i-1]
            IDCG_List_tmp[i]+=IDCG_List_tmp[i-1]
        else:
            DCG_List_tmp[i]+=(DCG_List_tmp[i]/math.log2(i)+DCG_List_tmp[i-1])
            IDCG_List_tmp[i]+=(IDCG_List_tmp[i]/math.log2(i)+IDCG_List_tmp[i-1])
    for k in range(len(DCG_List_tmp)):
        DCG_List[k] += DCG_List_tmp[k]
        IDCG_List[k]+= IDCG_List_tmp[k]
'''    
'''    
def plotNDCG():
    for i in range(len(DCG_List)):
        NDCG_List.append(DCG_List[i]/IDCG_List[i])
    sns.set(style="darkgrid")
    docNum = range(2265)
    df = pd.DataFrame.from_dict(
        {"docNum": docNum,
         "NDCG": NDCG_List
        }
    )
    plt.plot( 'docNum', 'NDCG', data=df, color='mediumvioletred')
    plt.show()
'''    
    
def printMAP(numofresult):
    #print("AP",APList)
    sum = 0
    count = 0
    for i in range(len(APList)):
        sum += APList[i]
        count +=1
    print("Result "+str(numofresult)+" MAP is :",sum/count)

def readFile(numofResult):
    startRowR = 0
    startRowA = 0
    for count in range(0, 16):
        numOfResultsQuery = getNumofResultsTrainSetQuery('Results/ResultsTrainSet'+str(numofResult)+'.txt',startRowR)
        numOfAssessmentQuery = getNumofAssessmentTrainSet('AssessmentTrainSet.txt',startRowA)
        qrList = readResultsTrainSetQuery('Results/ResultsTrainSet'+str(numofResult)+'.txt',startRowR,numOfResultsQuery)
        qaList = readNumofAssessmentTrainSet('AssessmentTrainSet.txt',startRowA,numOfAssessmentQuery)
        count = 0
        percision_List = []
        recall_List = []
        #gain_list is for ndcg
        #gain_List = []
        for i in range(qrList.size):
            #gain_List.append(0)
            for k in range(qaList.size):
                if(qrList[i]==qaList[k]):
                    #print(qrList[i])
                    #gain_list is for ndcg
                    #gain_List[i] = 1
                    count=count + 1
                    num = i+1
                    percision_List.append(count/num)
                    recall_List.append(count/numOfAssessmentQuery)
                    #print("percision:",count/num) 
                    #print("recall:",count/numOfAssessmentQuery)
        #compare is for             
        #compare(percision_List,recall_List)
        calculateAP(percision_List)
        #calculateDCGandIDCG(gain_List)
        startRowR += (numOfResultsQuery + 2)
        startRowA += (numOfAssessmentQuery + 2)


def main():
    for i in range(11):    
        readFile(i)
        #plot()
        printMAP(i)
        APList.clear()
        #plotNDCG()


if __name__ == "__main__":
    main()

