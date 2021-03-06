
import os
import re
import math
import operator

Queryfilename_list = []
Docfilename_list = []
Querydict_list = []
DocDict_list = []
#ni
QueryAllni_dict = {}
DocAllni_dict = {}
#relevDoc
relevDocdict_list = []
sort_rank_initial = []
def readQuery():
    
    path = "QUERY_WDID_NEW_middle"
    dirs = os.listdir(path)

    for fileName in dirs:
        Queryfilename_list.append(fileName)
        vectorIndex={}
        #print(fileName)
        file = open(path +"/"+ fileName, "r")
        for line in file:
            reline = re.sub(r'\s+-1[\r\n]', " ", line)
            splitWords = reline.split(" ")
            for word in splitWords:
                if(word!="" and word != "-1" and word != "\n"):
                    vectorIndex[word] = vectorIndex.setdefault(word, 0) + 1
                
        Querydict_list.append(vectorIndex)
        file.close()

def readDoc():
    path = "SPLIT_DOC_WDID_NEW"
    dirs = os.listdir(path)
    for fileName in dirs:
        Docfilename_list.append(fileName)
        vectorIndex={}
        count = 0
        #print(fileName)
        file = open(path +"/"+ fileName, "r")
        for line in file:
            count+=1
            if(count >3):
                reline = re.sub(r'\s+-1[\r\n]', " ", line)
                splitWords = reline.split(' ')
                for word in splitWords:
                    if(word!="" and word != "-1"):
                        vectorIndex[word] = vectorIndex.setdefault(word, 0) + 1
        DocDict_list.append(vectorIndex)
        file.close()
    
  
def calculatedictAll():
    for i in range(len(Querydict_list)):
        for key,value in Querydict_list[i].items():
            QueryAllni_dict[key] = QueryAllni_dict.setdefault(key, 0) + 1
    for k in range(len(DocDict_list)):
        for key,value in DocDict_list[k].items():
            DocAllni_dict[key] = DocAllni_dict.setdefault(key, 0) + 1            
        

def calculateQueryTF_IDF():
    
    #calcluate TF*IDF weight
    for k in range(len(Querydict_list)):
        values = [ v for v in Querydict_list[k].values()]
        values.sort(reverse = True)
        maxTF = values[0]
        for key,value in Querydict_list[k].items():
            Querydict_list[k][key] = (0.5 + 0.5*Querydict_list[k][key]/maxTF)*math.log2(len(Queryfilename_list)/QueryAllni_dict[key])
    
    #print(Querydict_list[0])
def calculateDocTF_IDF():
    for k in range(len(DocDict_list)):
        for key,value in DocDict_list[k].items():
            DocDict_list[k][key] = DocDict_list[k][key]*math.log2(len(Docfilename_list)/DocAllni_dict[key])        

def calculateSimilarity(Q_list,relevDocNum):
    f = open('Results/ResultsTrainSet'+str(relevDocNum)+'.txt', 'w', encoding = 'UTF-8') 
    for i in range(len(Q_list)):
        rank = {}  
        #calculate query vector length
        #values_q = [ pow(v,2) for v in Querydict_list[i].values()]
        #length_q = math.sqrt(sum(values_q))
        #calculate doc vector length
        for k in range(len(DocDict_list)):
            values_d = [ pow(v,2) for v in DocDict_list[k].values()]
            length_d = math.sqrt(sum(values_d))
            dotProduct = 0
            for key,value in DocDict_list[k].items():
                if(key in Q_list[i]):
                    dotProduct += (DocDict_list[k][key]*Q_list[i][key])
            #add docname and rank to dict
            rank[Docfilename_list[k]]= dotProduct/(length_d)
        sort_rank = sorted(rank.items(), key=operator.itemgetter(1),reverse = True)
        #save the first result sort_rank_initial contain 16 queries results
        if(relevDocNum == 0):
            revelDoc_dict = {}
            sort_rank_initial.append(sort_rank)
            relevDocdict_list.append(revelDoc_dict)
        #write to file
        f.write('Query '+str(i+1)+" "+str(Queryfilename_list[i])+" "+str(len(rank))+"\n")
        for n in range(len(sort_rank)):
            f.write(str(sort_rank[n][0])+"   "+str(sort_rank[n][1])+"\n")
        f.write("\n")    
        print(Queryfilename_list[i]+" Done")
        rank.clear()
    f.close()
     
     
    for q in range(len(sort_rank_initial)):
        for index in range(len(Docfilename_list)):
            if(sort_rank_initial[q][relevDocNum][0] == Docfilename_list[index]):
                #print(sort_rank_initial[q][revelDocNum][0])
                for key,value in DocDict_list[index].items():
                    #print(DocDict_list[index].keys())
                    #print(len(DocDict_list[index].items()))
                    relevDocdict_list[q][key] = relevDocdict_list[q].setdefault(key, 0) + value
                
    

def relevanceFeedback(relevDocNum):
    NewQuerydict_list = []

    for i in range(len(Querydict_list)):
        NewQuery_dict = {}
        for key,value in Querydict_list[i].items():
            NewQuery_dict[key] = Querydict_list[i][key]
        for key,value in relevDocdict_list[i].items(): 
            if(key in NewQuery_dict.keys()):
                NewQuery_dict[key] += (0.8/relevDocNum)*relevDocdict_list[i][key]
            else:
                NewQuery_dict[key] = relevDocdict_list[i][key]
        NewQuerydict_list.append(NewQuery_dict)
    calculateSimilarity(NewQuerydict_list,relevDocNum)    

def main():    
    readQuery()
    readDoc()
    calculatedictAll()
    calculateQueryTF_IDF() 
    calculateDocTF_IDF()
    calculateSimilarity(Querydict_list,0)
    
    for i in range(10):
        print("------iteration " + str(i+1) + "-------")
        relevanceFeedback(i+1)
    

if __name__ == "__main__":
    main()
