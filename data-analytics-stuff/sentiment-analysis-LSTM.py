"""
This script uses LSTM model to train sentiment analyser using TF >= 2.0

"""
# coding: utf-8
import pandas as pd
import datetime
import tensorflow.keras as K
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras.datasets import imdb
import time
from datetime import datetime as dt
import os
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
plt.style.use("dark_background")


class CallbackTimeHistory(K.callbacks.Callback):
    """
    Create callback to track time taken for every epoch from training start.
    """
    def __init__(self):
        self.time_per_epoch_history = []
        self.train_start = 0

    def on_train_begin(self, logs={}):
        self.time_per_epoch_history = []
        self.train_start = time.time()

    def on_epoch_end(self, batch, logs={}):
        self.time_per_epoch_history.append(time.time() - self.train_start)


def visualize_training(history, time_per_epoch):
    """
    Visualize training information
    :param history: history object returned by model.fit
    :return: None
    """
    # plot loss over epochs
    fig, ax = plt.subplots(1, 2, constrained_layout=True)
    ax[0].plot(time_per_epoch, history.history['loss'], "#6A59DC", label='Train loss')
    ax[0].plot(time_per_epoch, history.history['val_loss'], "#5597E7", label='Val loss')
    ax[0].set_xlabel('Time (in seconds)')
    ax[0].legend()

    ax[1].plot(time_per_epoch, history.history['accuracy'], "#6A59DC", label='Train Acc')
    ax[1].plot(time_per_epoch, history.history['val_accuracy'], "#5597E7", label='Val Acc')
    ax[1].set_xlabel('Time (in seconds)')
    ax[1].legend()

    plt.title("Training History")
    plt.savefig(os.path.join(path_to_plots, "training.png"), dpi=300)


if __name__ == '__main__':
    # config
    path_to_data = "./sample_data"
    path_to_model = './model'
    path_to_plots = "./plots"
    num_epochs = 3
    lr = 0.01

    # load data
    train_data = pd.read_csv(os.path.join(path_to_data, 'train_processed.csv'))
    test_data = pd.read_csv(os.path.join(path_to_data, 'test_processed.csv'))

    # combine data
    data = train_data.append(test_data, ignore_index=True)
    data = data[~data["processed"].isna()]
    data.reset_index()

    # one hot encoding
    y = pd.get_dummies(data['sentiment'])

    # convert data to matrix
    tokenizer = K.preprocessing.text.Tokenizer(num_words=20000)
    tokenizer.fit_on_texts(data["processed"])
    embedded_tweets = tokenizer.texts_to_matrix(data["processed"], mode='count')

    # 80-20 split
    x_train = embedded_tweets[:int(len(data) * .8)]
    x_test = embedded_tweets[-(len(data) - int(len(data) * .8)):]

    # shorten seq (can be removed later)
    x_train = sequence.pad_sequences(x_train, maxlen=100)
    x_test = sequence.pad_sequences(x_test, maxlen=100)

    y_train = y[:int(len(data) * .8)].values
    y_test = y[-(len(data) - int(len(data) * .8)):].values

    # set training config
    optimizer = K.optimizers.Adam(learning_rate=lr, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False)
    time_callback = CallbackTimeHistory()

    # define network
    model = Sequential()
    model.add(Embedding(20000, 128))
    model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(3, activation='sigmoid'))

    # model config
    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])

    # train model
    history = model.fit(x_train, y_train, batch_size=32, epochs=num_epochs, verbose=3, validation_data=(x_test, y_test)
                        , callbacks=[time_callback])

    # log events to console
    print("\n --- HyperParameters ---")
    print('Learning rate:', lr)
    print('Epochs:', num_epochs)
    print('Optimizer:', optimizer.__class__)

    print('\n --- Training ---')
    print('Training: Loss ({0}) Accuracy ({1})'.format(history.history['loss'][-1], history.history['accuracy'][-1]))
    print('Val: Loss ({0}) Accuracy ({1})'.format(history.history['val_loss'][-1], history.history['val_accuracy'][-1]))

    visualize_training(history, time_callback.time_per_epoch_history)

    # evaluate model
    score, acc = model.evaluate(x_test, y_test,
                                batch_size=32,
                                verbose=2)
    print('Test score:', score)
    print('Test accuracy:', acc)

    # save model
    model_path = os.path.join(path_to_model, 'model_{0}.h5'.format(dt.timestamp(dt.now())))
    model.save(model_path)

    print('Model saved successfully at ', model_path)