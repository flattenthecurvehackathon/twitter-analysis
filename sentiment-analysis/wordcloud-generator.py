
# coding: utf-8

# In[1]:

import re
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import string
import nltk
import warnings 
warnings.filterwarnings("ignore", category=DeprecationWarning)

get_ipython().magic('matplotlib inline')
df = pd.read_csv("/Users/amritaparab/Desktop/ACS/train.csv")


# In[2]:

df.info()


# In[3]:

df['sentiment'].unique()


# In[4]:

df.selected_text = df.selected_text.astype(str)


# In[5]:

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
        
    return input_txt   


# In[6]:

# remove twitter handles (@user)
df['tidy_tweet'] = np.vectorize(remove_pattern)(df['selected_text'], "@[\w]*")


# In[7]:

# remove special characters, numbers, punctuations
df['tidy_tweet'] = df['selected_text'].str.replace("[^a-zA-Z#]", " ")


# In[8]:

df['tidy_tweet'] = df['tidy_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))


# In[9]:

tokenized_tweet = df['tidy_tweet'].apply(lambda x: x.split())


# In[10]:

import nltk
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 
tokenized_tweet = tokenized_tweet.apply(lambda x: [lemmatizer.lemmatize(i) for i in x])


# In[11]:

for i in range(len(tokenized_tweet)):
    tokenized_tweet[i] = ' '.join(tokenized_tweet[i])

df['tidy_tweet'] = tokenized_tweet


# In[12]:

stopwords1= ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", 'covid','coronavirus','coronaviru','coronavirusau','http',"too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


# In[18]:

all_words = ' '.join([text for text in df['tidy_tweet'][df['sentiment'] == 'negative']])
from wordcloud import WordCloud
wordcloud = WordCloud(width=800, height=500, colormap='inferno',stopwords=stopwords1, background_color='white', random_state=21, max_font_size=110).generate(all_words)
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.savefig("aust_negative.png")
plt.show()


# In[15]:

all_words = ' '.join([text for text in df['tidy_tweet'][df['sentiment'] == 'positive']])
from wordcloud import WordCloud
wordcloud = WordCloud(width=800, height=500,colormap='ocean',stopwords=stopwords1, background_color='white', random_state=21, max_font_size=110).generate(all_words)
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.savefig("aust_positive.png")
plt.show()


# In[ ]:

all_words = ' '.join([text for text in df['tidy_tweet'][df['sentiment'] == 'neutral']])
from wordcloud import WordCloud
wordcloud = WordCloud(width=800, height=500,colormap='ocean',stopwords=stopwords1, background_color='white', random_state=21, max_font_size=110).generate(all_words)
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.savefig("aust_positive.png")
plt.show()

