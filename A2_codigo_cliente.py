
import string
import numpy as np
from todojuntov2 import *

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
print('A2.a')
print('función: getPais()')
print('A continuación se presentan varios ejemplos de la función getPais() que genera las letras del código de cliente')
print(getPais())
print(getPais())
print(getPais())

print('---------------')

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

print('A2.b')
print('función: getCodigo()')
print('A continuación se presentan varios ejemplos de la función getCodigo() que genera los números del código de cliente')
print(getCodigo(getPais()))
print(getCodigo(getPais()))
print(getCodigo(getPais()))

def clienteAleatorio():
    return (getPais() + '-' + getCodigo(getPais()))
print('---------------')
print('A2.c')
print('función: clienteAleatorio()')
print('A continuación se presentan varios ejemplos de la función clienteAleatorio() que genera los códigos de cliente')
print(clienteAleatorio())
print(clienteAleatorio())
print(clienteAleatorio())