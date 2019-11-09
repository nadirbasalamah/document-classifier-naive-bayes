# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 07:15:43 2019

@author: Nadir Basalamah
"""
import pandas as pd

data = pd.read_csv("D:\dataset_textmining\dataset.csv", encoding = "ISO-8859-1")

dataset = data.loc[:, ["Komentar","Hasil Akhir"]]
df = pd.DataFrame(dataset)

#print(df.loc[df["Hasil Akhir"] == "Positif"])
dataset_positif = df.loc[df["Hasil Akhir"] == "Positif"]["Komentar"].values.tolist()

dataset_negatif = df.loc[df["Hasil Akhir"] == "Negatif"]["Komentar"].values.tolist()

print(len(dataset_positif))
print(len(dataset_negatif))

dataList = [{'a': 1}, {'b': 3}, {'c': 5}]
for dic in dataList:
    for val in dic.values():
        print(val)