import string
from todojuntov2 import *
def create_dictionary_agenda():
    agenda = {}
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
    #definimos las letras mayúsculas
    letras = list(string.ascii_uppercase)
    #establecemos un bucle de forma que acada letra mayúscula le
    #corresponda un dato del array resultante del primer split.
    for i in range(longitud_num_clientes):
        agenda[letras[i]] ={
            int(num_clientes[i])
            #,"renta": renta_pc[i]}
            }
    return agenda
agenda = create_dictionary_agenda()
paises = {}
def create_dictionary_countries():
    letras = list(string.ascii_uppercase)
    fPaises = open('paises.txt', 'r')
    i = 0
    for linea in fPaises:
        paises[letras[i]] = linea.strip()
        i = i+1
    fPaises.close()

create_dictionary_countries()
print ('Este es el diccionario de países:')
print (paises)
print ('Este es el diccionario de letras asociado a número de clientes, al que llamamos agenda:')
create_dictionary_agenda()
print (agenda)

