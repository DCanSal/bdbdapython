import string
import numpy as np
import urllib.request
import pandas as pd
from todojuntov2 import *

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
    
gdp = get_gdp()
paises_gdp = get_paises_gdp()
pop = get_pop()
paises_pop = get_paises_pop()
pop_write = pop_gdp_matching()
generate_paises_ampliado_txt()
print('B3.9a')
print('paises_ampliado.txt creado con éxito.')
generate_diccionario_paises_ampliado()
print('la función generate_diccionario_paises_ampliado() crea el diccionario paises_ampliado que es la base para ejecutar el programa completo')
print(paises_ampliado)
print('-------------------')
generate_clientes_pibpc_txt_ampliado()
print('clientes_ampliado.txt creado con éxito.')
print('la función generate_clientes_pibpc_txt_ampliado() genera el archivo de texto clientes_ampliado.txt que es análogo a clientes_pipbc.txt. También es fundamental para ejecutar el resto del programa')
print('se construye a partir de las listas pop_write y gdp_limpio')
print(gdp_limpio)
print(pop_write)
print('-------------------')
agenda_ampliada = generate_agenda_ampliada()
print('generamos el diccionario base que fundamenta el código del programa')
print(agenda_ampliada)


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
#        totalClientes = totalClientes + agenda_ampliada[i]
#        totalClientes = totalClientes + list(agenda_ampliada[letras[i]])[0]
    #por la misma razón de los int definimos las listas de elements y probabilities
    elements = list()
    probabilities = list()
    #definimos el siguiente bucle para construir el cálculo de probabilidad una 
    #vez sabemos el numero de clientes asociado a la letra y por tanto el peso.
    for i in range(len(agenda_ampliada)):
        elements.append(letras[i])
        probabilities.append(float(list(agenda_ampliada[letras[i]])[0])/totalClientes)   
#        probabilities.append(list(agenda_ampliada[letras[i]])[0]/totalClientes)
    #como no almacena en la memoria el replacement, no importa ponerlo como True
    # o False.
    return np.random.choice(elements, 1, True, probabilities)[0] 

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

def clienteAleatorio_ampliado():
    letra_pais = getPais_ampliado()
    return (letra_pais + '-' + getCodigo_ampliado(letra_pais))

def create_messages_txt_ampliado():
    file = open("mensajes_ampliado.txt", "w")  
    for i in range(0,2500):
        file.write(clienteAleatorio_ampliado() + "  #  " + clienteAleatorio_ampliado() + "  #  ") 
        palabras_mensaje = random_word_corpus_generator(lineas, 12)
        for j in range(0,np.random.randint(3,12)):
            file.write((palabras_mensaje[j] + " "))
        file.write("\n")
    file.close()
    
create_messages_txt_ampliado()
print('mensajes_ampliado.txt creado con éxito')
    
def create_df_messages_ampliado(): 
    pais1=list()
    pais2=list()
    cantidad_palabras=list()
    file = open("mensajes_ampliado.txt", "r")
    linea = file.readline() # leo la primera linea
    while len(linea) > 2: # mientras que la linea contenga texto (no este vacia)
        lineaSep = linea.split("#") # separo pais, pais, palabras
        if len(lineaSep) < 3: # por si la linea esta mal, para no acceder a posiciones prohibidas
            print('ahi va la hostia')
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

dfmessages_ampliado = create_df_messages_ampliado()
agenda_mapa_ampliada = {}
mi_iterador = dfmessages_ampliado.iterrows()

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

matrix_mensajes_ampliada = np.zeros((len(agenda_ampliada), len(agenda_ampliada)))
def create_matrix_mensajes_ampliado():
    for i in range(len(agenda_ampliada)):
        for j in range(len(agenda_ampliada)):   
            matrix_mensajes_ampliada[i, j] = agenda_mapa_ampliada[letras[i],letras[j]]
    return matrix_mensajes_ampliada

create_matrix_ampliado(dfmessages_ampliado)
create_df_messages_ampliado()
print('---------------')
print('B3.9b')
print('A continuación se muestran prints de las funciones empleando la lista ampliada de países hasta lograr la matriz que cuenta los mensajes enviados entre esos países')
print(agenda_mapa_ampliada)
print('---------------')
print(matrix_mensajes_ampliada)
print('---------------')
print(create_matrix_mensajes_ampliado())
