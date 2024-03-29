# -*- coding: utf-8 -*-
"""pratica3RNN_PLN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZNKgMfHKJVrcVlEisTM2rME0ICRccR2x
"""

# Carregar os dados
import tensorflow as tf
import tensorflow_datasets as tfds
 
dataset, info = tfds.load('imdb_reviews/subwords8k', 
                             with_info=True, 
                             as_supervised=True)
print('info: {}'.format(info))

# Separação de dados
dataset_treino, dataset_teste = dataset['train'], dataset['test']

# Tratamento dos dados: aumentar a aleatoriedade e fazer um preenchimento dos dados para que as sequências tenham o mesmo comprimento.
BUFFER_SIZE = 10000
BATCH_SIZE = 64
dataset_treino = dataset_treino.shuffle(BUFFER_SIZE)
dataset_treino = dataset_treino.padded_batch(BATCH_SIZE)
dataset_teste = dataset_teste.padded_batch(BATCH_SIZE)

# Arquitetura do modelo RNN
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (Dense, 
                                     Embedding, 
                                     Bidirectional, 
                                     Dropout, 
                                     LSTM)
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.optimizers import Adam

# Criando o modelo
vocab_size = 10000
model = Sequential([Embedding(vocab_size, 64), 
                     Bidirectional(LSTM(64, return_sequences=True)),
                     Bidirectional(LSTM(32)), 
                     Dense(64, activation='relu'), 
                     Dropout(0.5), 
                     Dense(1)])
model.summary()
tf.keras.utils.plot_model(model)

# Compilação e treinamento do modelo
model.compile(loss=BinaryCrossentropy(from_logits=True),
             optimizer=Adam(1e-4),
             metrics=['accuracy'])

historico = model.fit(dataset_treino,
                     epochs = 1,
                     validation_data = dataset_teste,
                     validation_steps = 30)

# Verificar o comportamento da função de erro
import matplotlib.pyplot as plt
plt.title('Cálculo do Erro ao longo do treinamento')
plt.ylabel('Erro')
plt.xlabel('Época')
plt.plot(historico.history['loss'])
plt.plot(historico.history['val_loss'])
plt.legend(['loss (treinamento)', 'val_loss (validação)'], loc='upper right')
plt.show()

# Avaliação do modelo
test_loss, test_acc = model.evaluate(dataset_teste)
print('Teste de Perda: {}'.format(test_loss))
print('Teste de Acurácia: {}'.format(test_acc))

# Uso do modelo para predição
# Tratar os dados: preenchimento de um texto com zeros sempre que for necessário por meio da seguinte função:
def padding_comentario(comentario_codificado, tamanho_padding):
     zeros = [0] * (tamanho_padding - len(comentario_codificado))
     comentario_codificado.extend(zeros)
     return comentario_codificado
# Também precisamos codificar numericamente o texto de entrada, conforme a função:
def comentario_encoder(comentario): 
     comentario_codificado = 
     padding_comentario(encoder.encode(comentario), 64) 
     comentario_codificado = 
     tf.cast(comentario_codificado, tf.float32) 
     return tf.expand_dims(comentario_codificado, 0)

# Verificar o modelo com um exemplo
comentario = 'the film was a beautiful production with a very deep approach to issues that affect society.'
r = modelo.predict(comentario_encoder(comentario))
print(r)
resultado = lambda x: 'Avaliação Positiva' if x>0.5 else 'Avaliação Negativa'
print(resultado(r[0]))