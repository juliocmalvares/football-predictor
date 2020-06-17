from sklearn.model_selection import train_test_split
import load
import numpy as np
import pprocess
import matplotlib.pyplot as plt

data = load.DataLoader().download_data()
proc = pprocess.preprocessing()
tfidf, classes = proc.tfidf(data, "text")
class_names = ["positiva", "negativa", "nfutebol", "neutra"]
for i in range(len(classes)):
    if classes[i] == 'neutra':
        classes[i] = 0
    if classes[i] == "positiva":
        classes[i] = 1
    if classes[i] == "negativa":
        classes[i] = 2
    if classes[i] == "nfutebol":
        classes[i] = 3

data_train, data_test, y_train, y_test = train_test_split(tfidf, classes, test_size=0.1)

import tensorflow as tf
import matplotlib.pyplot as plt

def plot_graphs(history, metric):
  plt.plot(history.history[metric])
  plt.plot(history.history['val_'+metric], '')
  plt.xlabel("Epochs")
  plt.ylabel(metric)
  plt.legend([metric, 'val_'+metric])
  plt.show()


model = tf.keras.Sequential([
    tf.keras.layers.Embedding(10000, 64),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

history = model.fit(data_train, epochs=10,
                    validation_data=data_test, 
                    validation_steps=30)

test_loss, test_acc = model.evaluate(data_test)

print('Test Loss: {}'.format(test_loss))
print('Test Accuracy: {}'.format(test_acc))



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


