import string
import numpy as np
import urllib.request
from nltk.corpus import stopwords
import pandas as pd
from bs4 import BeautifulSoup
### Ejercicio A Letras-clientes.
#Abrimos el archivo de texto. Leemos las lineas y separamos por elementos
fClientes = open('clientes_pibpc.txt', 'r')
num_clientes = fClientes.readline().split()
renta_pc = fClientes.readline().split()
fClientes.close()
#como medida para asegurarnos de que las dimensiones del diccionario se mantienen
longitud_renta_pc = len(renta_pc)
longitud_num_clientes = len(num_clientes)
if longitud_num_clientes != longitud_renta_pc:
    print('esto no está bien')
    quit()
#definimos el diccionario como agenda
agenda = {}
#definimos las letras mayúsculas
letras = list(string.ascii_uppercase)
#establecemos un bucle de forma que acada letra mayúscula le
#corresponda un dato del array resultante del primer split.
for i in range(longitud_num_clientes):
    agenda[letras[i]] ={
        int(num_clientes[i])
        #,"renta": renta_pc[i]}
        }

import string
paises = {}
letras = list(string.ascii_uppercase)
fPaises = open('paises.txt', 'r')
i = 0
for linea in fPaises:
    paises[letras[i]] = linea.strip()
    i = i+1
fPaises.close()


#Codigos cliente: "letra país" - número (0000)

def getPais(): 
    # definimos la lista de las letras en mayúscula
    letras = list(string.ascii_uppercase)
    # establecemos el total de clientes a 0
    totalClientes = 0    
    # definimos un bucle de i hasta el final de los elementos de agenda
    for i in range(len(agenda)):
        #print(i)
        #para conseguir que el valor asociado a la letra en Agenda vuelva como 
        #int es necesario convertirlo en lista llamando al primer elemento
        totalClientes = totalClientes + list(agenda[letras[i]])[0]
    #por la misma razón de los int definimos las listas de elements y probabilities
    elements = list()
    probabilities = list()
    #definimos el siguiente bucle para construir el cálculo de probabilidad una 
    #vez sabemos el numero de clientes asociado a la letra y por tanto el peso.
    for i in range(len(agenda)):
        elements.append(letras[i])
        probabilities.append(list(agenda[letras[i]])[0]/totalClientes)
    #como no almacena en la memoria el replacement, no importa ponerlo como True
    # o False.
    return np.random.choice(elements, 1, True, probabilities)[0]  


def getCodigo(letraPais: str):
    #obtenemos el valor máximo del código introduciendo la letra en agenda
    setNumero = agenda[letraPais]
    #lo pasamos a lista para poder acceder al entero
    listaNumero = list(setNumero)
    #pedimos solamente el primer y único elemento
    elementoListaNumero = listaNumero[0]
    #calculamos el numero aleatorio con el rango establecido por el máximo
    #valor que es el número de clientes - 1 para cada letra..
    numero = np.random.choice(range(elementoListaNumero), 1)[0]
    numero = str(numero)
    #establecemos un código de 4 "0000" y reemplazamos por el número del código.
    numero = numero.zfill(4)
    return numero

#concatenamos el resultado de las dos funciones
#def clienteAleatorio():
#    return (getPais() + '-' + getCodigo(getPais()))
def clienteAleatorio():
    letra_pais = getPais()
    return (letra_pais + '-' + getCodigo(letra_pais))

def get_archivo(link):
    #archivo = urllib.request.urlopen("http://corpus.rae.es/frec/1000_formas.TXT")
    archivo = urllib.request.urlopen(link)
    con_etiquetas = archivo.read()
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
    
def create_messages_txt():
    file = open("mensajes_muestra.txt", "w")  
    for i in range(0,5000):
        file.write(clienteAleatorio() + "  #  " + clienteAleatorio() + "  #  ") 
        palabras_mensaje = random_word_corpus_generator(lineas, 12)
        for j in range(0,np.random.randint(3,12)):
            file.write((palabras_mensaje[j] + " "))
        file.write("\n")
    file.close()

def create_df_messages_mal(): 
    pais_emisor=list()
    pais_receptor=list()
    palabras_mensaje=list()
    pais1=list()
    pais2=list()
    cantidad_palabras=list()
    file = open("mensajes_muestra.txt", "r")
    linea = file.readline() # leo la primera linea
    while len(linea) > 2: # mientras que la linea contenga texto (no este vacia)
        lineaSep = linea.split("#") # separo pais, pais, palabras
        if len(lineaSep) < 3: # por si la linea esta mal, para no acceder a posiciones prohibidas
            print('algo no funciona bien')
            print(lineaSep)
            break
        pais_emisor.append(lineaSep[0].strip()) 
        pais_receptor.append(lineaSep[1].strip())
        palabras_mensaje.append(lineaSep[2].strip())
        pais1.append(lineaSep[0].strip()[0]) 
        pais2.append(lineaSep[1].strip()[0])
        palabras_sucio = lineaSep[2].split(" ")
        palabras_limpias = list()
        for palabra_candidata in palabras_sucio:
            if palabra_candidata != '' and palabra_candidata != '\n':
                palabras_limpias.append(palabra_candidata)
        cantidad_palabras.append(len(palabras_limpias))
        linea = file.readline() # leemos la siguiente linea
    data=list(zip(pais_emisor,pais_receptor,palabras_mensaje, pais1, pais2, cantidad_palabras))
    print(pd.DataFrame(data, columns = ['codigo_emisor', 'codigo_receptor', 'palabras_mensaje', 'pais_emisor', 'pais_reeptor', 'cantidad_palabras']))

def create_df_messages_bien(): 
    pais1=list()
    pais2=list()
    cantidad_palabras=list()
    file = open("mensajes_muestra.txt", "r")
    linea = file.readline() # leo la primera linea
    while len(linea) > 2: # mientras que la linea contenga texto (no este vacia)
        lineaSep = linea.split("#") # separo pais, pais, palabras
        if len(lineaSep) < 3: # por si la linea esta mal, para no acceder a posiciones prohibidas
            print('algo no está funcionando bien')
            print(lineaSep)
            break
        pais1.append(lineaSep[0].strip()[0]) 
        pais2.append(lineaSep[1].strip()[0])
        palabras_sucio = lineaSep[2].split(" ")
        palabras_limpias = list()
        for palabra_candidata in palabras_sucio:
            if palabra_candidata != '' and palabra_candidata != '\n':
                palabras_limpias.append(palabra_candidata)
        cantidad_palabras.append(len(palabras_limpias))
        linea = file.readline() # leemos la siguiente linea
    data=list(zip(pais1,pais2,cantidad_palabras))
    dfmessages = pd.DataFrame(data, columns = ['pais_emisor', 'pais_receptor', 'cantidad_palabras'])
    return dfmessages

dfmessages_aux = create_df_messages_bien()
agenda_mapa = {}
mi_iterador = dfmessages_aux.iterrows() #codigo Ange

def create_matrix(dataframe):
    for i in range(len(agenda)):
        for j in range(len(agenda)):
            agenda_mapa[(letras[i], letras[j])] = 0
    for dataframe in mi_iterador:
        letra_pais_emisor = dataframe[1]['pais_emisor']
        letra_pais_receptor = dataframe[1]['pais_receptor']
        cantidad_palabras = dataframe[1]['cantidad_palabras']
           
        valor_actual = agenda_mapa[(letra_pais_emisor, letra_pais_receptor)]
        agenda_mapa[(letra_pais_emisor, letra_pais_receptor)] = valor_actual + cantidad_palabras
    return dataframe
    
letras = list(string.ascii_uppercase)
gdp = list()
gdp_limpio = list()
def get_gdp():
    #conectamos con el databank.worldbank para obtener los datos de gdp
    #abrimos y guardamos la información en un archivo GDP.xls
    gdp_file = urllib.request.urlopen("https://databank.worldbank.org/data/download/GDP.xls")
    file = open("GDP.xls", 'wb')
    file.write(gdp_file.read())
    file.close()
    #Al comenzar el scraping de la tabla, las lineas que valen para análisis son de la 4 a la 208.
    gdp_sucio = pd.read_excel("GDP.xls")[4:208]
    paises_gdp = list(gdp_sucio[list(gdp_sucio.columns)[3]][0:25])
    #el resultado es una lista con el gdp de los primeros 25 países del mundo.
    gdp = list(gdp_sucio[list(gdp_sucio.columns)[4]][0:25])
    for i in range(len(gdp)):
        gdp_limpio_candidato = round(gdp[i]/10, ndigits = 0)
        gdp_limpio.append(gdp_limpio_candidato)
    return gdp

def get_paises_gdp():
    file = open("GDP.xls", 'r')
    file.close()
    #Al comenzar el scraping de la tabla, las lineas que valen para análisis son de la 4 a la 208.
    gdp_sucio = pd.read_excel("GDP.xls")[4:208]
    paises_gdp = list(gdp_sucio[list(gdp_sucio.columns)[3]][0:25])
    return paises_gdp

pop = list()
paises_pop = list()
def get_pop():
    #Empleando la misma fuente obtenemos una lista de los países ordenados por población
    pop_file = urllib.request.urlopen("http://databank.worldbank.org/data/download/POP.xls")
    file = open("POP.xls", 'wb')
    file.write(pop_file.read())
    file.close()
    #Al comenzar el scraping de la tabla, las lineas que valen para análisis son de la 4 a la 208.
    pop_sucio = pd.read_excel("POP.xls")[4:208]
    #nos quedamos con una lista de un tamaño considerable (los 100 primeros países ordenados por población)
    pop = list(pop_sucio[list(pop_sucio.columns)[4]][0:100])
    return pop

def get_paises_pop():
    file = open("POP.xls", 'r')
    file.close()
    #Al comenzar el scraping de la tabla, las lineas que valen para análisis son de la 4 a la 208.
    pop_sucio = pd.read_excel("POP.xls")[4:208]
    paises_pop = list(pop_sucio[list(pop_sucio.columns)[3]][0:100])
    return paises_pop

#matrix = np.zeros((n,2))
pop_write = list()
gdp_limpio = list()  
def pop_gdp_matching():
    # este bucle hace match entre 
    for i in range(len(paises_gdp)):
        for j in range(len(paises_pop)):
            if paises_gdp[i] == paises_pop[j]:
                # la población está comprendida en cientos de miles. para ajustarla al formato del texto original
                # clientes_pibpc.txt
                pop_candidata = round(pop[j]/100, ndigits = 0)
                pop_write.append(pop_candidata)
            else:
                continue
    return pop_write
            
def generate_paises_ampliado_txt():
    #Esta función genera el archivo paises_ampliado txt con la lista de los 25 países.
    file = open("paises_ampliado.txt", "w")  
    #este bucle asigna a cada linea del archivo de texto cada país.
    for i in range(len(paises_gdp)):
        file.write(paises_gdp[i])
        file.write('\n')
    file.close()

paises_ampliado = {}
#una vez hemos generado el archivo de texto, procedemos a leerlo en forma de diccionario
def generate_diccionario_paises_ampliado():
    #para ello necesitamos llamar al conjunto de letras en mayúscula
    letras = list(string.ascii_uppercase)
    #abrimos el archivo en formato lectura
    f_paises_ampliado = open('paises_ampliado.txt', 'r')
    i = 0
    #con este bucle, le asignamos una letra del diccionario a cada país.
    for linea in f_paises_ampliado:
        paises_ampliado[letras[i]] = linea.strip()
        i = i+1
    f_paises_ampliado.close()

#clientesgdp_muestra = list()
def generate_clientes_pibpc_txt_ampliado():
    #abrimos el archivo clientes_ampliado.txt en formato escritura
    f_clientes_ampliado = open('clientes_ampliado.txt', 'w')
    #con estos dos bucles replicamos el formato del clientes_pibpc original. una linea del fichero
    #de texto para cada variable: numero de clientes en la primera linea y gdp en la segunda.
    for i in range(len(paises_gdp)):
        f_clientes_ampliado.write(str(pop_write[i]) + " ")
    f_clientes_ampliado.write('\n')
    for i in range(len(paises_gdp)):
        f_clientes_ampliado.write(str(gdp_limpio[i]) + " ")
    f_clientes_ampliado.close()

#las listas finales con las que trabajar son pop_write, paises_gdp y gdp_limpio
#en la misma linea que en el programa original, llamaremos agenda_ampliada al diccionario que contiene los países
agenda_ampliada = {}
def generate_agenda_ampliada():
    #abrimos el archivo de texto clientes_ampliado.txt en modo lectura
    f_clientes = open('clientes_ampliado.txt', 'r')
    #volvemos a partirlo en dos lineas a las que asignamos nombres: num_clientes y renta_pc
    num_clientes = f_clientes.readline().split()
    renta_pc = f_clientes.readline().split()
    f_clientes.close()
    #establecemos esta medida preventiva para asegurarnos de que el diccionario se genera con las dimensiones correctas.
    longitud_renta_pc = len(renta_pc)
    longitud_num_clientes = len(num_clientes)
    if longitud_num_clientes != longitud_renta_pc:
        print('esto no está bien')
        quit()
    #asignamos a cada letra mayúscula un país con este bucle.
    for i in range(longitud_num_clientes):
        agenda_ampliada[letras[i]] ={
                num_clientes[i]
            #,"renta": renta_pc[i]}
            }
    return agenda_ampliada
    
def getPais_ampliado(): 
    # definimos la lista de las letras en mayúscula
    letras = list(string.ascii_uppercase)
    # establecemos el total de clientes a 0
    totalClientes = 0    
    # definimos un bucle de i hasta el final de los elementos de agenda
    for i in range(len(agenda_ampliada)):
        #print(i)
        #para conseguir que el valor asociado a la letra en Agenda vuelva como 
        #int es necesario convertirlo en lista llamando al primer elemento
         totalClientes += float(list(agenda_ampliada[letras[i]])[0])   
    #por la misma razón de los int definimos las listas de elements y probabilities
    elements = list()
    probabilities = list()
    #definimos el siguiente bucle para construir el cálculo de probabilidad una 
    #vez sabemos el numero de clientes asociado a la letra y por tanto el peso.
    for i in range(len(agenda_ampliada)):
        elements.append(letras[i])
        probabilities.append(float(list(agenda_ampliada[letras[i]])[0])/totalClientes)   
    #como no almacena en la memoria el replacement, no importa ponerlo como True
    # o False.
    return np.random.choice(elements, 1, True, probabilities)[0] 
#
def getCodigo_ampliado(letraPais: str):
    #obtenemos el valor máximo del código introduciendo la letra en agenda
    setNumero = agenda_ampliada[letraPais]
    #lo pasamos a lista para poder acceder al entero
    listaNumero = list(setNumero)
    #pedimos solamente el primer y único elemento
    elementoListaNumero = listaNumero[0]
    #calculamos el numero aleatorio con el rango establecido por el máximo
    #valor que es el número de clientes - 1 para cada letra..
    numero = np.random.choice(range(int(float(elementoListaNumero))), 1)[0]
    numero = str(numero)
    #establecemos un código de 4 "0000" y reemplazamos por el número del código.
    numero = numero.zfill(4)
    return numero
#
def clienteAleatorio_ampliado():
    letra_pais = getPais_ampliado()
    return (letra_pais + '-' + getCodigo_ampliado(letra_pais))
#
def create_messages_txt_ampliado():
    file = open("mensajes_ampliado.txt", "w")  
    for i in range(0,2500):
        file.write(clienteAleatorio_ampliado() + "  #  " + clienteAleatorio_ampliado() + "  #  ") 
        palabras_mensaje = random_word_corpus_generator(lineas, 12)
        for j in range(0,np.random.randint(3,12)):
            file.write((palabras_mensaje[j] + " "))
        file.write("\n")
    file.close()
#    
def create_df_messages_ampliado(): 
    pais1=list()
    pais2=list()
    cantidad_palabras=list()
    file = open("mensajes_ampliado.txt", "r")
    linea = file.readline() # leo la primera linea
    while len(linea) > 2: # mientras que la linea contenga texto (no este vacia)
        lineaSep = linea.split("#") # separo pais, pais, palabras
        if len(lineaSep) < 3: # por si la linea esta mal, para no acceder a posiciones prohibidas
            print('algo no está funcionando bien')
            print(lineaSep)
            break
        pais1.append(lineaSep[0].strip()[0]) 
        pais2.append(lineaSep[1].strip()[0])
        palabras_sucio = lineaSep[2].split(" ")
        palabras_limpias = list()
        for palabra_candidata in palabras_sucio:
            if palabra_candidata != '' and palabra_candidata != '\n':
                palabras_limpias.append(palabra_candidata)
        cantidad_palabras.append(len(palabras_limpias))
        linea = file.readline() # leemos la siguiente linea
    data=list(zip(pais1,pais2,cantidad_palabras))
    dfmessages = pd.DataFrame(data, columns = ['pais_emisor', 'pais_receptor', 'cantidad_palabras'])
    return dfmessages

def create_matrix_ampliado(dataframe):
    for i in range(len(agenda_ampliada)):
        for j in range(len(agenda_ampliada)):
            agenda_mapa_ampliada[(letras[i], letras[j])] = 0
    for dataframe in mi_iterador:
        letra_pais_emisor = dataframe[1]['pais_emisor']
        letra_pais_receptor = dataframe[1]['pais_receptor']
        cantidad_palabras = dataframe[1]['cantidad_palabras']
           
        valor_actual = agenda_mapa_ampliada[(letra_pais_emisor, letra_pais_receptor)]
        agenda_mapa_ampliada[(letra_pais_emisor, letra_pais_receptor)] = valor_actual + cantidad_palabras
    return dataframe
#
matrix_mensajes_ampliada = np.zeros((len(agenda_ampliada), len(agenda_ampliada)))
def create_matrix_mensajes_ampliado():
    for i in range(len(agenda_ampliada)):
        for j in range(len(agenda_ampliada)):   
            matrix_mensajes_ampliada[i, j] = agenda_mapa_ampliada[letras[i],letras[j]]
    return matrix_mensajes_ampliada
