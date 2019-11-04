
# coding: utf-8

# In[15]:

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import math
import re
import pandas as pd


# In[16]:

stemm = StemmerFactory()
stemmer = stemm.create_stemmer()
stop = StopWordRemoverFactory()
stopwords = stop.get_stop_words()


# In[17]:

data = pd.read_csv("D:\dataset_textmining\dataset.csv", encoding = "ISO-8859-1")


# ### Get sinopsis

# In[18]:

desc = data.loc[:, "Komentar"]


# ### Filtering kata simbol

# In[19]:

for i, val in enumerate(desc):
    desc[i] = (
        val.replace(";", "")
        .replace(",", "")
        .replace(".", "")
        .replace("?", "")
        .replace("-", " ")
        .replace("/", " ")
        .replace("(", "")
        .replace(")", "")
    )


# ### Functions

# In[20]:

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

# def hitungIDF(listdoc):
#     idDict={}
#     N = len(listdoc)
#     idDict = dict.fromkeys(listdoc[0].keys(),0)
#     for doc in listdoc:
#         for word, freq in doc.items():
#             if freq >0:
#                 idDict[word]+=1
#     for word, freq in idDict.items():
#         idDict[word] = math.log(N/float(freq))
    
#     return idDict

# def hitungTFIDF(tf,idfs):
#     tfidf={}
#     for word, freq in tf.items():
#         tfidf[word]= freq * idfs[word]
#     return tfidf


# ### Tokenisasi

# In[21]:

word_tokenized = tokenisasi_kata(desc)
print("Tokenizing :", word_tokenized, "\n")


# ### Filtering stop words

# In[22]:

print("filtering : ", memfilter(word_tokenized), "\n")


# ### Stemming + filter stop words. Sisa kata unik

# In[23]:

wordset = set(menstem((word_tokenized)))
print("stemming : ", wordset, "\n")


# In[24]:

sorted(wordset)


# ## Mencari TF

# ### Mengumpulkan seluruh kata dalam kalimat pada list

# In[25]:

sentences = []
words = []
freqs = []

for i, val in enumerate(desc):
    sentences.append(val)

for i, val in enumerate(sentences):
    words.append(sentences[i].split())


# ### Menghitung frekuensi kata unik pada dokumen

# In[26]:

for i, val in enumerate(sentences):    
    freqs.append(getFreq(dict.fromkeys(wordset, 0), menstem(words[i])))


# ### TF Tables

# In[27]:

print("TF")
for i, val in enumerate(freqs):
    tf = pd.DataFrame([freqs[i
    ]])
tf = pd.DataFrame(freqs)
print(tf)
print('\n')


# ## Menghitung IDF

# In[28]:

# idfs = hitungIDF(freqs)


# In[29]:

# print('IDF', idfs)


# ## Menghitung TFIDF

# In[30]:

# tfidf = []

# for i, val in enumerate(freqs):
#     tfidf.append(hitungTFIDF(freqs[i], idfs))


# In[31]:

# pd.DataFrame(tfidf)


# In[ ]:



