# -*- coding: utf-8 -*-
"""AtividadeDeepLearning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c7ReweWrv5XpQ1cvtUdsClL2XiDsII-M
"""

# Carregando os dados
import tensorflow as tf
import matplotlib.pyplot as plt
(xTreino, yTreino), (xTeste, yTeste) = tf.keras.datasets.fashion_mnist.load_data()
# Visualização dos dados
for i in range(5):
  plt.subplot(1, 5, i+1)
  plt.subplot(1, 5, i+1)
  plt.imshow(xTreino[i].reshape(28, 28))
  plt.title('Rótulo:{}'.format(yTreino[i]))
  plt.xticks([])
  plt.yticks([])
plt.show()

# Explorar o dataset
# Divindo o dataset
import numpy as np
from sklearn.preprocessing import LabelBinarizer
 
qtde = 55000
xValidacao = xTreino[qtde:, ..., np.newaxis]
yValidacao = yTreino[qtde:]
xTreino = xTreino[:qtde, ..., np.newaxis]
yTreino = yTreino[:qtde]
 
xTeste =  xTeste[..., np.newaxis]

# Preparando os dados - 28 pixels de largura e altura - Normalização
xTreino = xTreino.reshape(xTreino.shape[0], 28 * 28 * 1)
xTreino = xTreino.astype('float32') / 255.0

xTeste = xTeste.reshape(xTeste.shape[0], 28 * 28 * 1)
xTeste = xTeste.astype('float32') / 255.0

# Binarização - Método usado para regularizar as classes do modelo
lb = LabelBinarizer()
yTreino = lb.fit_transform(yTreino)
yTeste = lb.transform(yTeste)

# Modelo de Classificação
# Rede FeedForward - Criação das camadas
# Camada densa: cada neurônio de uma camada se conecta com todos da próxima camada
# Base de construção de camadas
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()
model.add(Dense(256, input_shape=(784,), activation='sigmoid'))
model.add(Dense(128, activation='sigmoid'))
model.add(Dense(10, activation='softmax'))

# Criando o otimizador do gradiente descendente tradicional
from tensorflow.keras.optimizers import SGD

sgd = SGD(0.01)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
H = model.fit(xTreino, yTreino, validation_split=0.1,epochs=100, batch_size=128)
# H = model.fit(xTreino, yTreino, validation_data=(xValidacao, yValidacao), epochs=100, batch_size=128)

# Predição
from sklearn.metrics import classification_report

predictions = model.predict(xTeste, batch_size=128)
print(classification_report(yTeste.argmax(axis=1), predictions.argmax(axis=1), target_names= [str(x) for x in lb.classes_]))

# Plotar o gráfico
plt.style.use('ggplot')
plt.figure()
plt.plot(np.arange(0, 100), H.history['loss'], label='train_loss')
plt.plot(np.arange(0, 100), H.history['val_loss'], label='val_loss')
plt.plot(np.arange(0, 100), H.history['accuracy'], label='train_acc')
plt.plot(np.arange(0, 100), H.history['val_accuracy'], label='val_acc')
plt.title('Treinamento Função de perda e Acurácia')
plt.xlabel('Época #')
plt.ylabel('Perda/Acurárcia')
plt.legend()