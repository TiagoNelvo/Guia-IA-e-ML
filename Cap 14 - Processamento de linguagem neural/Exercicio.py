import pandas as pd
import string
import spacy
import en_core_web_sm
import random
import seaborn as sns
import numpy as np
import re

# Classificação de textos do Twitter com spaCy

# Carregamento das bases de dados

# Link Kaggle: https://www.kaggle.com/augustop/portuguese-tweets-for-sentiment-analysis#TweetsNeutralHash.csv

# Base de treinamento

# Negative label: 0
# Positive label: 1

arquivo_treinamento = "Train50.csv"
base_treinamento = pd.read_csv(arquivo_treinamento, delimiter=',')

base_treinamento.shape

base_treinamento.head()

sns.countplot(base_treinamento['sentiment'], label = 'Contagem');

base_treinamento.drop(['id', 'tweet_date', 'query_used'], axis = 1, inplace=True)

base_treinamento.head()

sns.heatmap(pd.isnull(base_treinamento));

# Base de teste

arquivo_teste = "Test.csv"
base_teste = pd.read_csv(arquivo, delimiter=';')

base_teste.head()

base_teste.shape
base_teste.drop(['id', 'tweet_date', 'query_used'], axis = 1, inplace=True)

base_teste.head()

sns.heatmap(pd.isnull(base_teste));

# Função para pré-processamento dos textos

# Letras minúsculas
# Nome do usuário (@)
# URLs
# Espaços em branco
# Emoticons
# Stop words
# Lematização
# Pontuações

pln = en_core_web_sm.load()
pln

from spacy.lang.pt.stop_words import STOP_WORDS

stop_words = STOP_WORDS

def preprocessamento(texto):
    # Letras minúsculas
    texto = texto.lower()

    # Nome do usuário
    texto = re.sub(r"@[A-Za-z0-9$-_@.&+]+", ' ', texto)

    # URLs
    texto = re.sub(r"https?://[A-Za-z0-9./]+", ' ', texto)

    # Espaços em branco
    texto = re.sub(r" +", ' ', texto)

    # Emoticons
    lista_emocoes = {':)': 'emocaopositiva',
                    ':d': 'emocaopositiva',
                    ':(': 'emocaonegativa'}
    for emocao in lista_emocoes:
        texto = texto.replace(emocao, lista_emocoes[emocao])

    # Lematização
    documento = pln(texto)

    lista = []
    for token in documento:
        lista.append(token.lemma_)

    # Stop words e pontuações
    lista = [palavra for palavra in lista if palavra not in stop_words and palavra not in string.punctuation]
    lista = ' '.join([str(elemento) for elemento in lista if not elemento.isdigit()])

    return lista

# Pré-processamento da base de dados

# Limpeza dos textos

base_treinamento.head(10)

base_treinamento['tweet_text'] = base_treinamento['tweet_text'].apply(preprocessamento)

base_treinamento.head(10)

base_teste['tweet_text'] = base_teste['tweet_text'].apply(preprocessamento)

base_teste.head(10)

# Tratamento da classe

exemplo_base_dados = [["este trabalho é agradável", {"POSITIVO": True, "NEGATIVO": False}],
                      ["este lugar continua assustador", {"POSITIVO": False, "NEGATIVO": True}]]

base_dados_treinamento_final = []
for texto, emocao in zip(base_treinamento['tweet_text'], base_treinamento['sentiment']):
    if emocao == 1:
        dic = ({'POSITIVO': True, 'NEGATIVO': False})
    elif emocao == 0:
        dic = ({'POSITIVO': False, 'NEGATIVO': True})

    base_dados_treinamento_final.append([texto, dic.copy()])

len(base_dados_treinamento_final)

base_dados_treinamento_final[10:15]

base_dados_treinamento_final[45000:45005]

# Criação do classificador

modelo = spacy.blank('pt')
categorias = modelo.add_pipe("textcat")
categorias.add_label("POSITIVO")
categorias.add_label("NEGATIVO")
historico = []

from spacy.training import Example

modelo.begin_training()
for epoca in range(5):
    random.shuffle(base_dados_treinamento_final)
    losses = {}
    for batch in spacy.util.minibatch(base_dados_treinamento_final, 512):
        textos = [modelo(texto) for texto, entities in batch]
        annotations = [{'cats': entities} for texto, entities in batch]
        examples = [Example.from_dict(doc, annotation) for doc, annotation in zip(
            textos, annotations
        )]
        modelo.update(examples, losses=losses)
        historico.append(losses)
    if epoca % 5 == 0:
        print(losses)
    
historico_loss = []
for i in historico:
    historico_loss.append(i.get('textcat'))    
    
historico_loss = np.array(historico_loss)
historico_loss

import matplotlib.pyplot as plt
plt.plot(historico_loss)
plt.title('Progressão do erro')
plt.xlabel('Batches')
plt.ylabel('Erro')

modelo.to_disk("modelo")

# Testes com uma frase

modelo_carregado = spacy.load('modelo')
modelo_carregado

# Texto Positivo

texto_positivo = base_teste['tweet_text'][21]
texto_positivo

previsao = modelo_carregado(texto_positivo)
previsao

previsao.cats
  
texto_positivo = 'eu gosto muito de você'
texto_positivo = preprocessamento(texto_positivo)
texto_positivo

modelo_carregado(texto_positivo).cats 
  
# Texto Negativo 

base_teste['tweet_text'][4000]

texto_negativo = base_teste['tweet_text'][4000]
previsao = modelo_carregado(texto_negativo)
previsao.cats

# Avaliação Modelo

previsoes = []
for texto in base_teste['tweet_text']:
    previsao = modelo_carregado(texto)
    previsoes.append(previsao.cats)

previsoes_final = []
for previsao in previsoes:
    if previsao['POSITIVO'] > previsao['NEGATIVO']:
        previsoes_final.append(1)
    else:
        previsoes_final.append(0)

previsoes_final = np.array(previsoes_final)

respostas_reais = base_teste['sentiment'].values

from sklearn.metrics import accuracy_score
accuracy_score(respostas_reais, previsoes_final)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(respostas_reais, previsoes_final)
cm

sns.heatmap(cm, annot=True)

