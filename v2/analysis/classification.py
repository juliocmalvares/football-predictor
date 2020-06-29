from torchnlp.encoders.text import SpacyEncoder, pad_tensor
from sklearn.model_selection import train_test_split
import load
import numpy as np
import pprocess
import matplotlib.pyplot as plt
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from sklearn.svm import LinearSVC, SVC
import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


data_train = load.DataLoader().download_data()
data_full = load.DataLoader().download_all_data()

# encoder = SpacyEncoder([data_full[i]['text'] for i in data_full.keys()])


processor = pprocess.preprocessing()
tensors, labels = processor.spacy(data_train, "text")
ftensors, flabels = processor.spacy(data_full, 'text')

dados = [np.array(tensor) for tensor in tensors]
fdados = [np.array(tensor) for tensor in ftensors]

#normalizaçao de shape
maior = 0
print("Verificando maior tamanho nos dados de treino")
for i in tqdm(range(len(dados))):
    if len(dados[i]) > maior:
        maior = len(dados[i])
print("Verificando maior tamanho nos dados totais")
for i in tqdm(range(len(fdados))):
    if len(fdados[i]) > maior:
        maior = len(fdados[i])

print("Refatorando shape dos dados de treino")
for i in tqdm(range(len(dados))):
    if len(dados[i]) < maior:
        dados[i] = np.concatenate((dados[i], np.zeros((maior-len(dados[i])), dtype=int)))
        dados[i].reshape(-1,1)
print("Refatorando shape dos dados totais")
for i in tqdm(range(len(fdados))):
    if len(fdados[i]) < maior:
        fdados[i] = np.concatenate((fdados[i], np.zeros((maior-len(fdados[i])), dtype=int)))
        fdados[i].reshape(-1,1)

# print("Size fdados: ", len( [w[0] for w in fdados] ), len([w[1] for w in fdados]))

print("Maior size:", maior)
print("Iniciando processo de treino")

data_train, data_test, y_train, y_test = train_test_split(dados, labels, test_size=0.05)


classifier = make_pipeline(StandardScaler(), SVC(kernel="rbf", max_iter=-1, C=0.1, random_state=42, break_ties=True), verbose=True)
classifier.fit(data_train, y_train)
classifier.decision_function(data_train)

print("Score test SVM with ovr: ", classifier.score(data_test, y_test))

print(fdados[:5])

labels_final = []
print("Iniciando processo de classificação")
for i in tqdm(range(len(fdados))):
    labels_final.append(classifier.predict([fdados[i]]))

# print(labels_final[:100])

results = [int(w) for w in labels_final]


def make_axis(data):
    x = []
    y = []
    for w in data:
        x.append(w.min())
        y.append(w.max())
    return np.log(np.array(x)), np.log(np.array(y))

X, Y = make_axis(fdados)



plt.scatter(X, Y, c=results, cmap=plt.cm.Paired, edgecolors='k')
plt.axis('tight')
plt.show()


from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, random_state=2, verbose=True)
outputs = tsne.fit_transform(fdados)
x_cords = outputs[:][0]
y_cords = outputs[:][1]

print(x_cords[:10], y_cords[:10])
plt.scatter(x_cords, y_cords, c=results, cmap=plt.cm.Paired, edgecolors='k')
plt.axis("tight")
plt.show()





# print(texts)

# encoder = SpacyEncoder(texts)
# encoded_text = []
# for i in tqdm(range(len(texts))):
#     encoded_text.append(encoder.encode(texts[i]))
# print(type(encoded_text[0]))




# print(encoder.vocab_size)

# lengths = [len(i) for i in tqdm(encoded_text)]
# length_as_series = pd.Series(lengths)
# plt.title("Probability Density Function for text lengths")
# sns.distplot(length_as_series)

# max_pad_length = length_as_series.quantile(0.9)
# print(max_pad_length)
# plt.show()


# proc = pprocess.preprocessing()
# tfidf, labels = proc.tfidf(data, "text")
# class_names = ["positiva", "negativa", "nfutebol", "neutra"]
# for i in range(len(labels)):
#     if labels[i] == 'neutra':
#         labels[i] = 0
#     if labels[i] == "positiva":
#         labels[i] = 1
#     if labels[i] == "negativa":
#         labels[i] = 2
#     if labels[i] == "nfutebol":
#         labels[i] = 3


# reviews = []
# flabels = []
# for i in tqdm(range(len(encoded_text))):
#     if len(encoded_text[i]) < max_pad_length:
#         reviews.append(encoded_text[i])
#         flabels.append(labels[i])

# padded_dataset = []
# for i in tqdm(range(len(reviews))):
#     padded_dataset.append(pad_tensor(reviews[i], int(max_pad_length)))

# X = torch.stack(padded_dataset)
# y = torch.tensor(flabels)

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25)
# X_train, y_train = torch.tensor(X_train), torch.tensor(y_train)
# X_test, y_test = torch.tensor(X_test), torch.tensor(y_test)


# class Net(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.embedding = nn.Embedding(len(encoder.vocab)+1, 32)
#         self.lstm = nn.LSTM(32, 32, batch_first=True)
#         self.fc1 = nn.Linear(32, 4)
        
#     def forward(self, x):
#         x_ = self.embedding(x)
#         x_, (h_n, c_n) = self.lstm(x_)
#         x_ = (x_[:, -1, :])
#         x_ = self.fc1(x_)
#         return x_

# ds_train = torch.utils.data.TensorDataset(X_train, y_train)
# train_loader = torch.utils.data.DataLoader(ds_train, batch_size=64, shuffle=True)

# ds_test = torch.utils.data.TensorDataset(X_test, y_test)
# test_loader = torch.utils.data.DataLoader(ds_test, batch_size=64, shuffle=True)

# classifier = Net()
# device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# print("Cuda available:", torch.cuda.is_available()  )
# optimizer = optim.Adam(classifier.parameters(), lr=.002)
# criterion = nn.CrossEntropyLoss()
# epoch_bar = tqdm(range(10),
#                  desc="Training",
#                  position=0,
#                  total=2)

# acc = 0

# for epoch in epoch_bar:
#     batch_bar = tqdm(enumerate(train_loader),
#                      desc="Epoch: {}".format(str(epoch)),
#                      position=1,
#                      total=len(train_loader))
    
#     for i, (datapoints, labels) in batch_bar:
        
#         optimizer.zero_grad()
        
#         preds = classifier(datapoints.long())
#         loss = criterion(preds, labels)
#         loss.backward()
#         optimizer.step()
    
#         if (i + 1) % 500 == 0:
            
#             preds = classifier(X_test)
#             acc = (preds.argmax(dim=1) == y_test).float().mean().cpu().item()

#         batch_bar.set_postfix(loss=loss.cpu().item(),
#                               accuracy="{:.2f}".format(acc),
#                               epoch=epoch)
#         batch_bar.update()

        
#     epoch_bar.set_postfix(loss=loss.cpu().item(),
#                           accuracy="{:.2f}".format(acc),
#                           epoch=epoch)
#     epoch_bar.update()

# print(X, y)

# data_train, data_test, y_train, y_test = train_test_split(tfidf, labels, test_size=0.1)

# import tensorflow as tf
# import matplotlib.pyplot as plt

# def plot_graphs(history, metric):
#   plt.plot(history.history[metric])
#   plt.plot(history.history['val_'+metric], '')
#   plt.xlabel("Epochs")
#   plt.ylabel(metric)
#   plt.legend([metric, 'val_'+metric])
#   plt.show()


# model = tf.keras.Sequential([
#     tf.keras.layers.Embedding(10000, 64),
#     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(1)
# ])

# model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
#               optimizer=tf.keras.optimizers.Adam(1e-4),
#               metrics=['accuracy'])

# history = model.fit(data_train, epochs=10,
#                     validation_data=data_test,
#                     validation_steps=30)

# test_loss, test_acc = model.evaluate(data_test)

# print('Test Loss: {}'.format(test_loss))
# print('Test Accuracy: {}'.format(test_acc))


# from sklearn.svm import SVC

# #model_svm = LinearSVC(multi_class="crammer_singer", max_iter=7600)
# model_svm = SVC(max_iter=7600)
# model_svm.fit(data_train, y_train)

# print("Score test SVM with crammer_singer: ", model_svm.score(data_test, y_test))

# #model_svm2 = LinearSVC(multi_class="ovr", max_iter=7600)
# model_svm2 = SVC(max_iter=7600)
# model_svm2.fit(data_train, y_train)

# print("Score test SVM with ovr: ", model_svm2.score(data_test, y_test))


# from sklearn.neural_network import MLPClassifier

# model_mlp = MLPClassifier(max_iter=1000, n_iter_no_change=50)
# model_mlp.fit(data_train, y_train)
# print("Score test MLP: ", model_mlp.score(data_test, y_test))

# from sklearn.ensemble import RandomForestClassifier
# model_rf = RandomForestClassifier(max_depth=1000, n_jobs=4, n_estimators=1000)
# model_rf.fit(data_train, y_train)
# print("Score test RandomForest: ", model_rf.score(data_test, y_test))

# from sklearn.naive_bayes import GaussianNB
# model_gnb = GaussianNB()
# model_gnb.fit(data_train.toarray(), y_train)
# print("Score test GaussianNB: ", model_gnb.score(data_test.toarray(), y_test))

# from sklearn.naive_bayes import BernoulliNB
# model_bnb = BernoulliNB()
# model_bnb.fit(data_train, y_train)
# print("Score test RandomForest: ", model_bnb.score(data_test, y_test))


# from sklearn.multiclass import OneVsRestClassifier
# model_onr = OneVsRestClassifier(model_svm2).fit(data_train, y_train)
# print("Score ONRC SVM ovr:", model_onr.score(data_test, y_test))

# from sklearn.cluster import KMeans, MeanShift
# means = KMeans(n_clusters=4).fit(tfidf)

# results = means.fit_predict(data_test)
# print(results)
# print(y_test)

# cont = 0
# for i in range(len(results)):
#     if results[i] == y_test[i]:
#         cont += 1

# print("Acurácia: ", cont / len(results))
