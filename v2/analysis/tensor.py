import tensorflow_datasets as tfd
import matplotlib.pyplot as plt
import tensorflow_text
import tensorflow_hub as hub
import load
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pprocess
import numpy as np
from tqdm import tqdm

data_train = load.DataLoader().download_data()
data_full = load.DataLoader().download_all_data()

processor = pprocess.preprocessing()
tensors, labels = processor.spacy(data_train, "text")

labels = np.array(labels)
sequences_for_train = [data_train[w]['text'] for w in data_train.keys()]


training_size = int(len(sequences_for_train) * .75)
training_sentences = sequences_for_train[0: training_size]
test_sentences = sequences_for_train[training_size:]
training_labels = labels[0:training_size]
test_labels = labels[training_size:]

tokenizer = Tokenizer(oov_token='<OOV>')
tokenizer.fit_on_texts(training_sentences)
print(len(tokenizer.word_index))

training_sequences = tokenizer.texts_to_sequences(training_sentences)
training_padded = pad_sequences(training_sequences, maxlen=len(
    training_sequences[0]), truncating='post')

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, maxlen=len(
    training_sequences[0]), truncating='post')

vocab_size = len(tokenizer.word_index) + 1


from sklearn.svm import LinearSVC, SVC
import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier

classifier = make_pipeline(StandardScaler(), OneVsRestClassifier(SVC(kernel="rbf", max_iter=-1, C=1, random_state=42, break_ties=True), n_jobs=4), verbose=True)
# classifier = make_pipeline(StandardScaler(), OneVsRestClassifier(KNeighborsClassifier(algorithm='kd_tree'), n_jobs=4), verbose=True)
classifier.fit(training_padded, training_labels)
print(classifier.classes_)


print("Score test SVM with ovr: ", classifier.score(test_padded, test_labels))

sequences = [data_full[w]['text'] for w in data_full.keys()]
print('Tamanho sequencias dados completos: ', len(sequences))

sequences = tokenizer.texts_to_sequences(sequences)
padded = pad_sequences(sequences, maxlen=len(
    training_sequences[0]), truncating='post')

results = classifier.predict(padded)
print(results[:200])
# for i in results:
#     if i != 1 and i != 0:
#         print("Diferente class")
# print(list(classifier.predict(padded)[:2000]))
