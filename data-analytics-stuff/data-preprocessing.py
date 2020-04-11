import tensorflow.keras as K
import nltk
import pandas as pd
import os
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt
import re
plt.style.use("dark_background")


def clean_data(sentence):
    strip_special_chars = re.compile("[^A-Za-z0-9 ]+")

    string = sentence.lower().replace("<br />", " ")
    string = re.sub(r'@\w+','',string)                                      # Delete @* references
    string = re.sub(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',' ', string)  # Delete http(s):// links
    string = re.sub(r'\.+',' ', string)                                     # Replace ... with ' '
    return re.sub(strip_special_chars, "", string.lower().strip())


def process_text(train):
    # process train text
    train.insert(loc=len(train.columns), column="processed", value="")
    train.dropna(axis=0, inplace=True)
    test.dropna(axis=0, inplace=True)
    tokenizer = nltk.TweetTokenizer(preserve_case=False)
    lemmatizer = nltk.stem.WordNetLemmatizer()
    stemmer = nltk.stem.PorterStemmer()
    stopwords = []
    try:
        with open(os.path.join(path_to_data, "stopwords.txt"), 'r') as f:
            stopwords = f.readlines()
    except Exception as e:
        print(e)
    for i in range(len(train)):
        tokens = tokenizer.tokenize(clean_data(train.iloc[i]["text"]))
        train["processed"].iloc[i] = " ".join([stemmer.stem(lemmatizer.lemmatize(t)) for t in tokens
                                          if t not in stopwords])
    return train


def get_class(polarity, labels=True):
    """
    Get senitment class based on polarity values
    :param polarity:
    :return:
    """
    classes = ["negative", "neutral", "positive"]
    val = None
    if -0.25 <= polarity <= 0.25:
        val = 1
    elif polarity > 0.25:
        val = 2
    else:
        val = 0
    if labels:
        return classes[val]
    return val


if __name__ == '__main__':
    print(K.__version__)

    path_to_data = "./sample_data"
    path_to_plots = "./plots"

    train = pd.read_csv(os.path.join(path_to_data, "train.csv"))
    test = pd.read_csv(os.path.join(path_to_data, "test.csv"))

    train = process_text(train)
    train.dropna(inplace=True)
    train.to_csv(os.path.join(path_to_data, "train_processed.csv"), index=False)

    test = process_text(test)
    test.dropna(inplace=True)
    test.to_csv(os.path.join(path_to_data, "test_processed.csv"), index=False)

    # data exploration
    fig, ax = plt.subplots()
    ax.pie([len(np.where(train["sentiment"] == "negative")[0]),
            len(np.where(train["sentiment"] == "neutral")[0]),
            len(np.where(train["sentiment"] == "positive")[0])]
           , labels=["Negative", "Neutral", "Positive"]
           , explode=(0, 0.1, 0)
           , autopct='%1.1f%%'
           , colors=["#5597E7", "#587196", "#6A59DC"])
    ax.set_title("Data Proportion")
    fig.savefig(os.path.join(path_to_plots, "sentiment_proportion.png"), dpi=300)

