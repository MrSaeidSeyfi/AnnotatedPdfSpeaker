# -*- coding: utf-8 -*-
Automatically generated by Colaboratory.

 

import urllib.request
import io
with urllib.request.urlopen("https://link.springer.com/content/pdf/10.1007/s11634-020-00415-6.pdf") as url:
    s = url.read() 

b = io.BytesIO(s)

!pip install PyPDF2
# importing all the required modules
import PyPDF2
import urllib  # the lib that handles the url stuff

# creating an object 
# file = open('https://link.springer.com/content/pdf/10.1007/s11634-020-00415-6.pdf', 'rb')

# file = urllib.request.urlopen('https://link.springer.com/content/pdf/10.1007/s11634-020-00415-6.pdf')
# creating a pdf reader object
fileReader = PyPDF2.PdfFileReader(b)

# print the number of pages in pdf file
print(fileReader.numPages)

text = ""
for page in fileReader.pages:
    text += page.extract_text() + "\n"

import re
import gensim, pprint
from nltk.tokenize.treebank import TreebankWordDetokenizer
def depure_data(data):
    
    #Removing URLs with a regular expression
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    data = url_pattern.sub(r'', data)

    # Remove Emails
    data = re.sub('\S*@\S*\s?', '', data)

    # Remove new line characters
    data = re.sub('\s+', ' ', data)

    # Remove distracting single quotes
    data = re.sub("\'", "", data)
        
    return data

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

def detokenize(text):
    return TreebankWordDetokenizer().detokenize(text)

temp = []
#Splitting pd.Series to list
data_to_list = text.split(".")
for i in range(len(data_to_list)):
    temp.append(depure_data(data_to_list[i]))
data_words = list(sent_to_words(temp)) 
sentences = []
for i in range(len(data_words)):
    sentences.append(detokenize(data_words[i]))
print(sentences[:2])

import numpy as np
import pandas as pd
import nltk
nltk.download('punkt') # one time execution
import re

# remove punctuations, numbers and special characters
text = text.replace("[^a-zA-Z]", " ")

# make alphabets lowercase
# clean_sentences = [s.lower() for s in clean_sentences]
text=text.lower()

from nltk.corpus import stopwords
stop_words = stopwords.words('english')

# function to remove stopwords
def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

# remove stopwords from the sentences
clean_sentences = [remove_stopwords(r.split()) for r in sentences]

# Extract word vectors
word_embeddings = {}
f = open('glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

sentence_vectors = []
for i in clean_sentences:
  if len(i) != 0:
    v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
  else:
    v = np.zeros((100,))
  sentence_vectors.append(v)

# similarity matrix
sim_mat = np.zeros([len(sentences), len(sentences)])

# We will use Cosine Similarity to compute the similarity between a pair of sentences.

from sklearn.metrics.pairwise import cosine_similarity

# And initialize the matrix with cosine similarity scores.

for i in range(len(sentences)):
  for j in range(len(sentences)):
    if i != j:
      sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]

 
# Applying PageRank Algorithm

import networkx as nx

nx_graph = nx.from_numpy_array(sim_mat)
scores = nx.pagerank(nx_graph)

ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
summery = ""
# Extract top 3 sentences as the summary
for i in range(3):
  summery += ranked_sentences[i][1] + " "

from IPython.display import Audio, display
from gtts import gTTS 
  
language = 'en'
 
fileobj = gTTS(text=summery, lang=language, slow=False)
fileobj.save("summery.mp3")
 

display(Audio('summery.mp3', autoplay=True))