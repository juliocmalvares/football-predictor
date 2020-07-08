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
# print(data_train)
sequences_for_train = [data_train[w]['text'] for w in data_train.keys()]
sequences_for_train = processor.applystw(sequences_for_train)
sequences_for_train = processor.applystem(sequences_for_train)


encoder = tfd.features.text.SubwordTextEncoder.build_from_corpus(
    sequences_for_train, target_vocab_size=2**15)
print(encoder)
print(encoder.encode(sequences_for_train[0]))


training_size = int(len(sequences_for_train) * .8)
training_sentences = sequences_for_train[0: training_size]
test_sentences = sequences_for_train[training_size:]
training_labels = labels[0:training_size]
test_labels = labels[training_size:]


training_sequences = [encoder.encode(w) for w in tqdm(training_sentences)]

test_sequences = [encoder.encode(w) for w in tqdm(training_sentences)]
# tokenizer = Tokenizer(oov_token='<OOV>')
# tokenizer.fit_on_texts(training_sentences)
# print(len(tokenizer.word_index))

# training_sequences = tokenizer.texts_to_sequences(training_sentences)
training_padded = pad_sequences(training_sequences, maxlen=len(
    training_sequences[0]), truncating='post')

# test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, maxlen=len(
    training_sequences[0]), truncating='post')

vocab_size = encoder.vocab_size


print(training_padded.shape)
# training_padded.padded_batch(256)
# test_padded.padded_batch(256)

model = tf.keras.Sequential([
    # input_length=len(training_sequences[0])),
    tf.keras.layers.Embedding(vocab_size, 256),
    # tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(256)),
    # tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dense(units=256, activation='relu'),
    tf.keras.layers.Dense(1)#4, activation='softmax')
])
print(model.summary())
model.compile(loss=tf.losses.BinaryCrossentropy(),
              optimizer=tf.keras.optimizers.Adam(1e-4), metrics=['accuracy'])

num_epochs = 50

history = model.fit(training_padded, training_labels, epochs=num_epochs,
                    validation_data=(test_padded, test_labels), verbose=1)

print(model.evaluate(training_padded, training_labels))
# print(model.summary())

input()
history_dict = history.history
acc = history_dict['accuracy']
val_acc = history_dict['val_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(acc) + 1)

# "bo" is for "blue dot"
plt.plot(epochs, loss, 'bo', label='Training loss')
# b is for "solid blue line"
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()

plt.clf()   # clear figure

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()
sequences = [data_full[w]['text'] for w in data_full.keys()]
print('Tamanho sequencias dados completos: ', len(sequences))
sequences = processor.applystw(sequences)
sequences = processor.applystem(sequences)

sequences = tokenizer.texts_to_sequences(sequences)
padded = pad_sequences(sequences, maxlen=len(
    training_sequences[0]), truncating='post')

print(model.predict(padded)[:50])


# tokenizer = Tokenizer(oov_token="<OOV>")
# tokenizer.fit_on_texts(sequences_for_train)
# word_index = tokenizer.word_index

# sequences_by_tokenizer = tokenizer.texts_to_sequences(sequences_for_train)
# padded_sequences_train = pad_sequences(sequences_by_tokenizer, padding='post')

# # print(padded_sequences_train[0])
# # print(padded_sequences_train.shape)

# training_size = (len(padded_sequences_train)*.8)

# training_sentences = padded_sequences_train[ 0:  training_size]
# test_sentences = padded_sequences_train[training_size : ]
# training_labels = labels[0:training_size]
# test_labels = labels[training_size:]
