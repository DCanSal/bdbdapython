from B3_ampliacion_informes import *

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

create_messages_txt_ampliado()
dfmessages_ampliado = create_df_messages_ampliado()
create_matrix_ampliado(dfmessages_ampliado)
create_df_messages_ampliado()
create_matrix_mensajes_ampliado()