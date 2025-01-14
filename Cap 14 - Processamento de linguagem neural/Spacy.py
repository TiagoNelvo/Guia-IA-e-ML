import bs4 as bs
import urllib.request
import nltk
import spacy

#!pip install -q spacy==2.2.3 #Atualizado: 02/05/2021 Obs: utilizar esta versão.
#!python3 -m spacy download pt

pln  = spacy.load('pt')
pln

pln = spacy.load('pt')
pln

documento = pln('Estou aprendendo processamento de linguagem natural, curso em Curitiba')

type(documento)

for token in documento:
    print(token.text, token.pos_)
    
#Lemetização e Stemização

for token in documento:
    print(token.text, token.lemma_)
    
doc = pln('encontrei encontraram encontrarão encontrariam cursando curso cursei')
[token.lemma_ for token in doc]

import nltk
nltk.download('rslp')

stemmer = nltk.stem.RSLPStemmer()
stemmer.stem('aprender')

for token in documento:
    print(token.text, token.lemma_, stemmer.stem(token.text))
    
#Carregamento dos textos

dados = urllib.request.urlopen('https://pt.wikipedia.org/wiki/Intelig%C3%AAncia_artificial')

#'https://pt.wikipedia.org/wiki/Intelig%C3%AAncia_artificial'

#dados = urllib.request.urlopen('https://pt.wikipedia.org/wiki/Inteligência_artificial')

dados = dados.read()
dados

dados_html = bs.BeautifulSoup(dados, 'lxml')
dados_html

paragrafos = dados_html.find_all('p')
len(paragrafos)

paragrafos[1]

paragrafos[1].text

conteudo = ''
for p in paragrafos:
    conteudo += p.text 

conteudo

conteudo = conteudo.lower()
conteudo

# Buscas em textos com spaCy

pln = spacy.load('pt')
pln

string = 'turing'
token_pesquisa = pln(string)

pln.vocab

from spacy.matcher import PhraseMatcher
matcher = PhraseMatcher(pln.vocab)
matcher.add('SEARCH', None, token_pesquisa)

doc = pln(conteudo)
matches = matcher(doc)
matches

doc[2323:2324], doc[2323-5:2324+5]

doc[2333:2334], doc[2333-5:2334+5]

matches[0], matches[0][1], matches[0][2]

matches[0], matches[0][1], matches[0][2]

from IPython.core.display import HTML
texto = ''
numero_palavras = 50
doc = pln(conteudo)
matches = matcher(doc)

display(HTML(f'<h1>{string.upper()}</h1>'))
display(HTML(f"""<p><strong>Resultados encontrados:</strong> {len(matches)}</p>"""))
for i in matches:
    inicio = i[1] - numero_palavras
    if inicio < 0:
        inicio = 0
    texto += str(doc[inicio:i[2] + numero_palavras]).replace(string, f"<mark>{string}</mark>")
    texto += "<br /><br />"
display(HTML(f"""... {texto} ... """))

# Extração de entidades nomeadas

for entidade in doc.ents:
    print(entidade.text, entidade.label_)
    
from spacy import displacy
displacy.render(doc, style = 'ent', jupyter = True)

# Nuvem de palavras e stop words

from spacy.lang.pt.stop_words import STOP_WORDS
print(STOP_WORDS)

len(STOP_WORDS)

pln.vocab['usa'].is_stop

doc = pln(conteudo)
lista_token = []
for token in doc:
    lista_token.append(token.text)
    
print(lista_token)

len(lista_token)

sem_stop = []
for palavra in lista_token:
    if pln.vocab[palavra].is_stop == False:
        sem_stop.append(palavra)
        
print(sem_stop)

len(sem_stop)

from matplotlib.colors import ListedColormap
color_map = ListedColormap(['orange','green', 'red', 'magenta'])        

from wordcloud import WordCloud
cloud = WordCloud(background_color = 'white', max_words = 100, colormap=color_map)
        
import matplotlib.pyplot as plt
cloud = cloud.generate(' '.join(sem_stop))
plt.figure(figsize=(15,15))
plt.imshow(cloud)
plt.axis('off')
plt.show()