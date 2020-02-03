import numpy as np
import urllib.request
from nltk.corpus import stopwords
from todojuntov2 import *

def get_archivo(link):
    #archivo = urllib.request.urlopen("http://corpus.rae.es/frec/1000_formas.TXT")
    archivo = urllib.request.urlopen(link)
    con_etiquetas = archivo.read()
    from bs4 import BeautifulSoup
    texto_limpio = BeautifulSoup(con_etiquetas, "lxml")
    texto = texto_limpio.get_text(strip=True)
    lineas = texto.splitlines()
    return lineas

def print_corpus_to_file(lineas):
    palabras = list()
    file = open("corpus.txt", "w")
    file.write("Palabras\t")
    file.write("Frecuencias\t")
    file.write("\n")
    out_espannol = stopwords.words('spanish')
    for i in range(1,len(lineas)):
        if len(palabras) == 500:
            break
        linea = lineas[i].split("\t")
        palabra_candidata = linea[1].split()[0]
        if palabra_candidata in out_espannol:
            continue
        palabras.append(palabra_candidata)
        file.write("%s\t" % palabra_candidata)
        file.write("%s\t" % linea[3])
        file.write("\n")
    file.close()

def random_word_corpus_generator(lineas, number_of_words = 10):
    palabras = list()
    frecuencias = list()
    out_espannol = stopwords.words('spanish')
    for i in range(1,len(lineas)):
        if len(palabras) == 500:
            break
        linea = lineas[i].split("\t")
        palabra_candidata = linea[1].split()[0]
        if palabra_candidata in out_espannol:
            continue
        palabras.append(palabra_candidata)
        frecuencias.append(float(linea[3]))
    total_frecuencias = sum(frecuencias)
    probabilidad = [x/total_frecuencias for x in frecuencias]
    return list(np.random.choice(palabras, number_of_words, False, probabilidad))
    
lineas = get_archivo("http://corpus.rae.es/frec/1000_formas.TXT")
print_corpus_to_file(lineas)
print('A3.a')
print('Al correr la función get_archivo() obtenemos la lista de palabras de la url que llamaremos "lineas"')
print('---------------')
print(lineas[1:10])
print('---------------')
print('A3.b y c')
print('Al correr la función print_corpus_to_file(lineas) generamos el archivo de texto corpus.txt ya ordenado por frecuencias')
print('---------------')
print('A3.d')
print('Al correr la función random_word_corpus_generator(lineas, number_of_words = n) generamos una lista de n palabras escogidas por frecuencia de uso. Véase el ejemplo con 10 palabras')
print(random_word_corpus_generator(lineas, 10))