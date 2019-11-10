
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

# data = pd.read_csv("D:\dataset_textmining\dataset.csv", encoding = "ISO-8859-1")
data = pd.read_csv("E:\Programming\Python\Text Mining\document-classifier-naive-bayes\dataset.csv", encoding = "ISO-8859-1")


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

def getConditionalProb(wordset, wordset_unique, count, verbs):
    #TODO: calculate conditional probability for each words
    sentences = []
    words = []
    freqs = []
    count_words = []
    conditionalProbs = []

    for i, val in enumerate(wordset):
        sentences.append(val)

    for i, val in enumerate(sentences):
        words.append(sentences[i].split())
    
    for i, val in enumerate(sentences):    
        freqs.append(getFreq(dict.fromkeys(wordset_unique, 0), menstem(words[i])))
        
    for dic in freqs:
        for val in dic.values():
            count_words.append(val)
    
    for i, val in enumerate(count_words):
        conditionalProbs.append((count_words[i] + 1) / (count + verbs))
        
    return conditionalProbs
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

#pre processing kata dalam kategori positif
dataset = data.loc[:, ["Komentar","Hasil Akhir"]]
df = pd.DataFrame(dataset)
dataset_positif = df.loc[df["Hasil Akhir"] == "Positif"]["Komentar"].values.tolist()

for i, val in enumerate(dataset_positif):
    dataset_positif[i] = (
        val.replace(";", "")
        .replace(",", "")
        .replace(".", "")
        .replace("?", "")
        .replace("-", " ")
        .replace("/", " ")
        .replace("(", "")
        .replace(")", "")
    )

word_tokenized_positif = tokenisasi_kata(dataset_positif)
filtered_word_positif = memfilter(word_tokenized_positif)
wordset_positif = menstem((word_tokenized_positif))
count_positif = len(wordset_positif)
print(count_positif)
#pre processing kata dalam kategori negatif
dataset_negatif = df.loc[df["Hasil Akhir"] == "Negatif"]["Komentar"].values.tolist()
for i, val in enumerate(dataset_negatif):
    dataset_negatif[i] = (
        val.replace(";", "")
        .replace(",", "")
        .replace(".", "")
        .replace("?", "")
        .replace("-", " ")
        .replace("/", " ")
        .replace("(", "")
        .replace(")", "")
    )

word_tokenized_negatif = tokenisasi_kata(dataset_negatif)
filtered_word_negatif = memfilter(word_tokenized_negatif)
wordset_negatif = menstem((word_tokenized_negatif))
count_negatif = len(wordset_negatif)
print(count_negatif)

#menghitung conditional probability pada masing-masing term
conditionalProbPositif = getConditionalProb(dataset_positif, wordset, count_positif, verbs)
conditionalProbNegatif = getConditionalProb(dataset_negatif, wordset, count_negatif, verbs)

print("Conditional Probability pada Kategori Positif")
for i, val in enumerate(conditionalProbPositif):
    cpp = pd.DataFrame([conditionalProbPositif[i
    ]])
cpp = pd.DataFrame(conditionalProbPositif)
print(cpp)
print('\n')

print("Conditional Probability pada Kategori Negatif")
for i, val in enumerate(conditionalProbNegatif):
    cpn = pd.DataFrame([conditionalProbNegatif[i
    ]])
cpn = pd.DataFrame(conditionalProbNegatif)
print(cpn)
print('\n')