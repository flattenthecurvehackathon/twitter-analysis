import pandas as pd
import os
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt
plt.style.use("dark_background")


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
    path_to_data = "./sample_data"
    path_to_plots = "./plots"

    train = pd.read_csv(os.path.join(path_to_data, "train.csv"))
    test = pd.read_csv(os.path.join(path_to_data, "test.csv"))

    print(train.info())
    print(test.info())

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
    fig.savefig(os.path.join(path_to_plots, "sentiment_proportion.jpg"), dpi=300)

    # get preds
    for i in range(len(train)):
        train["prediction"] = get_class(TextBlob(train["sentiment"][i]).polarity, labels=True)

    fig, ax = plt.subplots()
    ax.pie([len(np.where(train["prediction"] == "negative")[0]),
            len(np.where(train["prediction"] == "neutral")[0]),
            len(np.where(train["prediction"] == "positive")[0])]
           , labels=["Negative", "Neutral", "Positive"]
           , explode=(0, 0.1, 0)
           , autopct='%1.1f%%'
           , colors=["#5597E7", "#587196", "#6A59DC"])
    ax.set_title("Data Proportion Predictions")
    fig.savefig(os.path.join(path_to_plots, "sentiment_prediction_proportion.jpg"), dpi=300)

    train.to_csv(os.path.join(path_to_data, "predictions.csv"))
    print(train.info())







