import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib
plt.style.use("dark_background")
import numpy as np


if __name__ == '__main__':
    path_to_data = "./sample_data"
    path_to_plots = "./plots"

    train = pd.read_csv(os.path.join(path_to_data, "train.csv"))
    test = pd.read_csv(os.path.join(path_to_data, "test.csv"))
    print()

    # data exploration
    plt.pie([len(np.where(train["sentiment"] == "negative")[0]),
             len(np.where(train["sentiment"] == "neutral")[0]),
             len(np.where(train["sentiment"] == "positive")[0])]
            , labels=["Negative", "Neutral", "Positive"]
            , explode=(0, 0.1, 0)
            , autopct='%1.1f%%'
            , colors=["#5597E7", "#587196", "#6A59DC"]
            )
    plt.title("Data Proportion")
    plt.show()
    plt.savefig(os.path.join(path_to_plots, "sentiment_proportion.jpg"), dpi=300)

