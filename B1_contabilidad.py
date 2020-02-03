import pandas as pd
from todojuntov2 import *

def create_df_messages_mal(): 
    pais_emisor=list()#para cada columna del dataframe generamos una lista
    pais_receptor=list()
    palabras_mensaje=list()
    pais1=list()
    pais2=list()
    cantidad_palabras=list()
    file = open("mensajes_muestra.txt", "r")
    linea = file.readline() # leo la primera linea
    while len(linea) > 2: # mientras que la linea contenga texto (no este vacia)
        lineaSep = linea.split("#") # separo pais, pais, palabras por asteriscos
        if len(lineaSep) < 3: # por si la linea esta mal, para no acceder a posiciones prohibidas
            print('algo no está funcionando bien')
            print(lineaSep)
            break
        pais_emisor.append(lineaSep[0].strip()) #de cada linea escogemos la porción que nos interesa
        pais_receptor.append(lineaSep[1].strip())
        palabras_mensaje.append(lineaSep[2].strip())
        pais1.append(lineaSep[0].strip()[0]) 
        pais2.append(lineaSep[1].strip()[0])
        palabras_sucio = lineaSep[2].split(" ")
        palabras_limpias = list()
        for palabra_candidata in palabras_sucio:
            if palabra_candidata != '' and palabra_candidata != '\n': #nos aseguramos de que la palabra candidata del mensaje sea una palabra
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
        pais1.append(lineaSep[0].strip()[0]) #es más fácil separar los códigos emisor y receptor
        pais2.append(lineaSep[1].strip()[0])
        palabras_sucio = lineaSep[2].split(" ")#con las palabras del mensaje es más difícil. primero separamos haciendo split por espacios
        palabras_limpias = list()#luego generamos una lista donde almacenar las palabras en limpio del mensaje
        for palabra_candidata in palabras_sucio:
            if palabra_candidata != '' and palabra_candidata != '\n':
                palabras_limpias.append(palabra_candidata)
        cantidad_palabras.append(len(palabras_limpias))
        linea = file.readline() # leemos la siguiente linea
    data=list(zip(pais1,pais2,cantidad_palabras))
    dfmessages = pd.DataFrame(data, columns = ['pais_emisor', 'pais_receptor', 'cantidad_palabras'])
    return dfmessages
print("B1.5")
print("Al llamar a la función create_df_messages_mal() generamos el dataframe con las seis columnas que pedía el ejercicio")
dfmessages_mal = create_df_messages_mal()
print(dfmessages_mal)
print("-------------")
print("B1.6")
print("Al llamar a la función create_df_messages_bien() generamos el dataframe con la información esencial para generar la posterior matriz")
dfmessages_bien = create_df_messages_bien()
print(dfmessages_bien)
print("B1.7")
print("Fui incapaz de entender por mí mismo cómo se realizaba el planteamiento map/reduce. Razón por la que no se incluye en este trabajo.")
