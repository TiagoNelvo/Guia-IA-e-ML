import tensorflow as tf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn

tf.__version__

dataset = pd.read_csv('personagens.csv')

dataset.shape
dataset.head()
dataset.tail()

sns.countplot(x = 'classe', data=dataset)

#sns.heatmap(dataset.corr(), annot=True)

X = dataset.iloc[:, 0:6].values

X

y = dataset.iloc[:, 6].values

y

y = (y == 'Bart')
y

from sklearn.model_selection import train_test_split

X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(X, y, test_size= 0.2)

X_treinamento.shape, y_treinamento.shape

X_teste.shape, y_teste.shape

# (entradas + saídas) / 2
# CAMARDAS 6 -> 4 -> 4 -> 4 -> 1

rede_neural = tf.keras.models.Sequential()
rede_neural.add(tf.keras.layers.Dense(units=4, activation='relu', input_shape=(6,)))
rede_neural.add(tf.keras.layers.Dense(units=4, activation='relu'))
rede_neural.add(tf.keras.layers.Dense(units=4, activation='relu'))
rede_neural.add(tf.keras.layers.Dense(units=1, activation='relu'))

rede_neural.summary()

rede_neural.compile(optimizer='Adam', loss='binary_crossentropy', metrics = ['accuracy'])

historico = rede_neural.fit(X_treinamento, y_treinamento, epochs=50, validation_split=0.1)

historico.history.keys()

plt.plot(historico.history['val_loss'])

plt.plot(historico.history['val_accuracy'])

previsoes = rede_neural.predict(X_teste)

previsoes

# 1 True- Bart
# 2 False - Homer

previsoes = (previsoes > 0.5)
previsoes

from sklearn.metrics import accuracy_score
accuracy_score(previsoes, y_teste)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_teste, previsoes)
cm

sns.heatmap(cm, annot=True)

