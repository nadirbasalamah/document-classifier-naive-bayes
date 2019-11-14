# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 07:15:43 2019

@author: Nadir Basalamah
"""
#import pandas as pd

#data = pd.read_csv("D:\dataset_textmining\dataset.csv", encoding = "ISO-8859-1")

#dataset = data.loc[:, ["Komentar","Hasil Akhir"]]
#df = pd.DataFrame(dataset)

#print(df.loc[df["Hasil Akhir"] == "Positif"])
#dataset_positif = df.loc[df["Hasil Akhir"] == "Positif"]["Komentar"].values.tolist()

#dataset_negatif = df.loc[df["Hasil Akhir"] == "Negatif"]["Komentar"].values.tolist()

#print(len(dataset_positif))
#print(len(dataset_negatif))
#test = 0
#dataList = [{'a': 1}, {'b': 3}, {'c': 5},{'a': 6}]
#for dic in dataList:
#    for keys in dic.keys():
#        if 'a' in dic.keys():
#            for val in dic.values():
#                test += val
#            
#print(test)
#from operator import itemgetter 
#
def getCountWord(word, freqs):
    items = []
    count = 0
    words = [items[word] for items in freqs if word in items]
    
    
    for val in words:
        count += val
    
    return count

def getCountWord2(word, freqs):
    count = 0
    for dic in freqs:
        for keys in dic.keys():
            if word in dic.keys():
                for val in dic.values():
                    count += val
    
    return count

def getCountWord3(word, freqs):
    test = []
    for i in range(len(freqs) - 1):
        test.append(freqs[word][i])
    return test
#
#test = []
freqs = [{"a" : 1},{"b" : 2},{"c" : 3},{"a" : 5},{"b" : 6}]
test_list = [{'gfg' : 1, 'is' : 2, 'good' : 3},{'gfg' : 2}, {'best' : 3, 'gfg' : 4}]
word = {"a","b","c","d","e"}
#
#for x in word:
#    test.append(getCountWord(x,freqs))
#
#print(test)
#y = []
#tes = 0
#test = [y['b'] for y in freqs if 'b' in y]
#print(test)
#y.append(test[0])
#print(y)
#coba = []
#for x in word:
#    coba.append(getCountWord(x,freqs))
#
#
#print(coba)
test = []
for w in sorted(word):
    print(w)
    test.append(getCountWord2(w,freqs))
    
print(test)
print(getCountWord3("a",freqs))
