# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 12:27:47 2019

@author: Nadir Basalamah
"""


# coding: utf-8

# In[73]:

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import pandas as pd


# In[74]:

stemm = StemmerFactory()
stemmer = stemm.create_stemmer()
stop = StopWordRemoverFactory()
stopwords = stop.get_stop_words()


# In[75]:

data = pd.read_csv("D:\dataset_textmining\dataset1.csv", encoding = "ISO-8859-1")
dataset_uji = pd.read_csv("D:\dataset_textmining\datauji1.csv", encoding = "ISO-8859-1")


# ### Get komentar

# In[76]:

desc = data.loc[:,'Komentar']
dataset = data.loc[:, ["Komentar","Hasil Akhir"]]
data_uji = dataset_uji.loc[:,'Komentar']

df = pd.DataFrame(dataset)
datalist = pd.DataFrame(desc)    
testdata = pd.DataFrame(data_uji)

list_data = datalist.values.tolist()
list_data_uji = testdata.values.tolist()

dataset_positif = df.loc[df["Hasil Akhir"] == "Positif"]["Komentar"].values.tolist()
dataset_negatif = df.loc[df["Hasil Akhir"] == "Negatif"]["Komentar"].values.tolist()

jumlah_dok_total = len(desc)
jumlah_dok_positif = len(dataset_positif)
jumlah_dok_negatif = len(dataset_negatif)


# ### Menghapus berbagai simbol pada kata

# In[77]:

for i, val in enumerate(desc):
    desc[i] = (
        val.replace(";", "")
        .replace(",", "")
        .replace(".", " ")
        .replace("?", "")
        .replace("-", " ")
        .replace("/", " ")
        .replace("(", "")
        .replace(")", "")
    )

for i, val in enumerate(dataset_positif):
    dataset_positif[i] = (
        val.replace(";", "")
        .replace(",", "")
        .replace(".", " ")
        .replace("?", "")
        .replace("-", " ")
        .replace("/", " ")
        .replace("(", "")
        .replace(")", "")
    )

for i, val in enumerate(dataset_negatif):
    dataset_negatif[i] = (
        val.replace(";", "")
        .replace(",", "")
        .replace(".", " ")
        .replace("?", "")
        .replace("-", " ")
        .replace("/", " ")
        .replace("(", "")
        .replace(")", "")
    )
# ### Functions

# In[78]:

def tokenisasi_kata(sentences):
    tokenizing = []
    for val in sentences:
        for value in val.split():
            tokenizing.append(value)

    return tokenizing

def memfilter(doc):
    filtering = []
    for i in doc:
        if i not in stopwords:
            filtering.append(i)

    filtering = list((filtering))
    return filtering

def menstem(doc1):
    stemming = []
    for i in memfilter(doc1):
        stemming.append(stemmer.stem(i))

    stemming = list((stemming))
    return stemming

def getFreq(dicti, word):
    for word in word:
        if word not in dicti:
            continue
        dicti[word] += 1

    return dicti

def getCountWord(word, freqs):
    res = 0
    for i in range(len(freqs)):
        res += freqs[word][i]
    return res


def getAllFreq(doc):
    sentences = []
    words = []
    freqs = []

    for i, val in enumerate(doc):
        sentences.append(val)

    for i, val in enumerate(sentences):
        words.append(sentences[i].split())
    
    for i, val in enumerate(sentences):    
        freqs.append(getFreq(dict.fromkeys(wordset, 0), menstem(words[i])))
    
    return freqs

def getConditionalProb(wordset, wordset_unique, count, verbs):
    sentences = []
    words = []
    freqs = []
    count_words = []
    conditionalProbs = []
    sorted_wordset = sorted(wordset_unique)

    for i, val in enumerate(sorted(wordset)):
        sentences.append(val)

    for i, val in enumerate(sentences):
        words.append(sentences[i].split())
    
    for i, val in enumerate(sentences):    
        freqs.append(getFreq(dict.fromkeys(wordset_unique, 0), menstem(words[i])))
    
    for i, val in enumerate(freqs):
        tf = pd.DataFrame([freqs[i]])
        tf = pd.DataFrame(freqs)
                
    for val in sorted_wordset:
        count_words.append(getCountWord(val,tf))
        
    for i, val in enumerate(count_words):
        conditionalProbs.append((count_words[i] + 1) / (count + verbs))
    
    result = dict(zip(sorted_wordset,conditionalProbs))
        
    return result

def preprocessing(doc):
    for i in range(len(doc) - 1):
        doc[i] = str(doc[i])
    for i, val in enumerate(doc):
        doc[i] = (
        val.replace(";", "")
        .replace(",", "")
        .replace(".", " ")
        .replace("?", "")
        .replace("-", " ")
        .replace("/", " ")
        .replace("(", "")
        .replace(")", "")
        )
    word_tokenized = tokenisasi_kata(doc)
    filtered = memfilter(word_tokenized)
    wordset = set(menstem((filtered)))
    
    return wordset

# ### Tokenisasi

# In[79]:

word_tokenized = tokenisasi_kata(desc)
word_tokenized_positif = tokenisasi_kata(dataset_positif)
word_tokenized_negatif = tokenisasi_kata(dataset_negatif)
print("Tokenizing :", word_tokenized, "\n")


# ### Filtering stop words

# In[80]:

print("filtering : ", memfilter(word_tokenized), "\n")
filtered_word_positif = memfilter(word_tokenized_positif)
filtered_word_negatif = memfilter(word_tokenized_negatif)

# ### Stemming + filter stop words. Sisa kata unik

# In[81]:

wordset = set(menstem((word_tokenized)))
print("stemming : ", wordset, "\n")
wordset_positif = menstem((word_tokenized_positif))
wordset_negatif = menstem((word_tokenized_negatif))
# In[82]:

sorted(wordset)


# ## Mencari TF



# In[83]:

# ### Menghitung frekuensi kata unik pada dokumen

# In[84]:

freqs = []
freqs = getAllFreq(desc)


# ### TF Tables

# In[88]:

print("TF")
for i, val in enumerate(freqs):
    tf = pd.DataFrame([freqs[i
    ]])
tf = pd.DataFrame(freqs)
print(tf)
print('\n')

# ### Menghitung nilai |V| dan jumlah seluruh kata pada kategori positif dan negatif

# In[86]:

verbs = len(wordset)
print("Jumlah seluruh kata yang unik (|V|) : " + str(verbs))
#print(wordset)
#menghitung jumlah seluruh kata pada kategori positif
count_positif = len(wordset_positif)
print("Jumlah seluruh kata pada kategori positif : " + str(count_positif))

#menghitung jumlah seluruh kata pada kategori negatif
count_negatif = len(wordset_negatif)
print("Jumlah seluruh kata pada kategori negatif : " + str(count_negatif))

#Prior Probability pada kategori positif
pp_positif = jumlah_dok_positif / jumlah_dok_total
print("Prior Probability pada kategori positif : " + str(pp_positif))
#Prior Probability pada kategori negatif
pp_negatif = jumlah_dok_negatif / jumlah_dok_total
print("Prior Probability pada kategori negatif : " + str(pp_negatif))

#menghitung conditional probability pada masing-masing term
conditionalProbPositif = getConditionalProb(dataset_positif, wordset, count_positif, verbs)
conditionalProbNegatif = getConditionalProb(dataset_negatif, wordset, count_negatif, verbs)

print("Conditional Probability pada Kategori Positif")
cpp = pd.DataFrame.from_dict(conditionalProbPositif, orient='index')
print(cpp)
print('\n')

print("Conditional Probability pada Kategori Negatif")
cpn = pd.DataFrame.from_dict(conditionalProbNegatif, orient='index')
print(cpn)
print('\n')

#Data Testing
origin_data = ["Positif","Positif","Positif","Negatif","Negatif","Negatif"]
test_data = []
test_results = []
n_data = 0
res1 = pp_positif
res2 = pp_negatif

for i in range(len(list_data_uji)):
    test_data.append(preprocessing(list_data_uji[i]))

for i in range(len(test_data)):
    word_data = [] 
    for val in test_data[i]:
        if val in wordset:
            word_data.append(val)
    for val in word_data:
        res1 *= cpp[0][val]
        res2 *= cpn[0][val]
    if(res1 > res2):
        test_results.append("Positif")
    else:
        test_results.append("Negatif")
    print(res1)
    print(res2)

for i in range(len(test_results)):
    if(test_results[i] == origin_data[i]):
        n_data += 1

print(test_results)
accuracy = round((n_data / len(test_results)) * 100,2) 
print("Accuracy (%) : " + str(accuracy))    