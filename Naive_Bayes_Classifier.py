
# coding: utf-8

# In[73]:

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import math
import re
import pandas as pd


# In[74]:

stemm = StemmerFactory()
stemmer = stemm.create_stemmer()
stop = StopWordRemoverFactory()
stopwords = stop.get_stop_words()


# In[75]:

data = pd.read_csv("D:\dataset_textmining\dataset.csv", encoding = "ISO-8859-1")


# ### Get komentar

# In[76]:

desc = data.loc[:,'Komentar']


# ### Menghapus berbagai simbol pada kata

# In[77]:

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


# ### Tokenisasi

# In[79]:

word_tokenized = tokenisasi_kata(desc)
print("Tokenizing :", word_tokenized, "\n")


# ### Filtering stop words

# In[80]:

print("filtering : ", memfilter(word_tokenized), "\n")


# ### Stemming + filter stop words. Sisa kata unik

# In[81]:

wordset = set(menstem((word_tokenized)))
print("stemming : ", wordset, "\n")


# In[82]:

sorted(wordset)


# ## Mencari TF

# ### Mengumpulkan seluruh kata dalam kalimat pada list

# In[83]:

sentences = []
words = []
freqs = []

for i, val in enumerate(desc):
    sentences.append(val)

for i, val in enumerate(sentences):
    words.append(sentences[i].split())


# ### Menghitung frekuensi kata unik pada dokumen

# In[84]:

for i, val in enumerate(sentences):    
    freqs.append(getFreq(dict.fromkeys(wordset, 0), menstem(words[i])))


# ### TF Tables

# In[88]:

print("TF")
for i, val in enumerate(freqs):
    tf = pd.DataFrame([freqs[i
    ]])
tf = pd.DataFrame(freqs)
print(tf)
print('\n')
# print(tf.columns.values)


# ### Menghitung nilai |V| dan jumlah seluruh kata pada kategori positif dan negatif

# In[86]:

verbs = len(wordset)
# desc1 = data.loc[:,['Komentar','Hasil Akhir']]
# print(desc1)

