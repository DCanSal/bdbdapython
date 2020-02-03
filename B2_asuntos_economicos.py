from todojuntov2 import *
import numpy as np

def create_matrix_tarifas():
    matrix_tarifas = np.zeros((len(agenda), len(agenda)))
    fClientes = open('clientes_pibpc.txt', 'r')
    num_clientes = fClientes.readline().split()
    renta_pc = fClientes.readline().split()
#    for i in range(len(num_clientes)):    
#        print(float(num_clientes[i])/float(renta_pc[i]))
    for i in range(len(num_clientes)):    
       matrix_tarifas [i,:] = round((float(num_clientes[i])/float(renta_pc[i]) * 10), ndigits = 3)
    return matrix_tarifas 

tarifas = create_matrix_tarifas()
file_tarifas = open('tarifas.txt', 'w')
np.savetxt('tarifas.txt', tarifas, delimiter=',')
file_tarifas.close()
print('archivo tarifas.txt creado con éxito')

dfmessages = create_df_messages_bien()
agenda_mapa = {}

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

create_matrix(dfmessages)
matrix_mensajes = np.empty((len(agenda), len(agenda)))
def create_matrix_mensajes():
    for i in range(len(agenda)):
        for j in range(len(agenda)):   
            matrix_mensajes[i, j] = agenda_mapa[letras[i],letras[j]]
    return matrix_mensajes

mensajes = create_matrix_mensajes()

print('B2.8a')
print('Calculamos la matriz de valores que hemos guardado en el fichero tarifas.txt')
print(tarifas)
print('-------------')
print('B2.8b')
print('primero calculamos una matriz acumulando los mensajes por cada pais emisor-receptor')
print(mensajes)
print('luego calculamos el producto escalar entre ambas matrices para obtener los precios')

print(tarifas * mensajes)