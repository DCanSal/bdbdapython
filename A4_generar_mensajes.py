import numpy as np
from todojuntov2 import *

def create_messages_txt():
    file = open("mensajes_muestra.txt", "w")  
    for i in range(0,5000):
        file.write(clienteAleatorio() + "  #  " + clienteAleatorio() + "  #  ") 
        palabras_mensaje = random_word_corpus_generator(lineas, 12)
        for j in range(0,np.random.randint(3,12)):
            file.write((palabras_mensaje[j] + " "))
        file.write("\n")
    file.close()
create_messages_txt()

print('¡mensajes de texto creados correctamente!')
print('la función create_messages_txt() genera el archivo de texto mensajes_muestra.txt. La función se podría reescribir para que la cantidad de mensajes se controle al llamar la función cambiando el 5000 por n en el primer bucle. En última instancia preferí dejarlo fijo en 5000 mensajes')