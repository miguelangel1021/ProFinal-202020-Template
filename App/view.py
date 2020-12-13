"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import list as lt
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información:")
    print("3- Top taxis afiliados:")
    print("4- Top numero de servicios:")
    print("5- Top puntos en fecha: ")
    print("6- Top puntos en rango de fechas: ")
    print("7- Mejor horario para una community area: ")
    print("0- Salir")
    print("*******************************************")
"""
Menu principal
"""
def optionTwo():
    num=int(input("Ingrese el numero de archivos a cargar (1, 2 o 3): "))
    print("\nCargando información de los taxis....")
    controller.loadTrips(catalog,num)
    compañias,numero_taxis=controller.num_t_c(catalog)
    print('Numero de taxis: ' + str(numero_taxis))
    print('Numero de compañias: ' + str(compañias))
    

def optionThree():
    num=int(input("Ingrese el numero de compañias en el top: "))
    print('El top de compañias con mas taxis es: ')
    lista=controller.req_1_a(catalog,num)
    iterador=it.newIterator(lista)
    while it.hasNext(iterador):
        compañia=it.next(iterador)
        print(compañia["Nombre"], "con un numero de",lt.size(compañia["Taxis_afiliados"]),"taxis afiliados.")


def optionFour():
    num=int(input("Ingrese el numero de compañias en el top: "))
    print('El top de compañias con mas taxis es: ')
    lista=controller.req_1_b(catalog,num)
    iterador=it.newIterator(lista)
    while it.hasNext(iterador):
        compañia=it.next(iterador)
        print(compañia["compañia"], "con un numero de",compañia["servicios"],"servicios.")

def optionFive():
    num=int(input("Ingrese el numero de taixs en el top: "))
    fecha =input("Ingrese la fecha en la que desea conocer el top (AAAA-MM-DD): ")
    print('El top de taxis con mas puntos en la fecha es: ')
    lista=controller.req_2_a(catalog,num,fecha)
    iterador=it.newIterator(lista)
    while it.hasNext(iterador):
        compañia=it.next(iterador)
        print(compañia["ID_T"], "con un numero de",round(compañia["Puntos"],2),"puntos.")

def optionSix():
    num=int(input("Ingrese el numero de taixs en el top: "))
    fecha_I =input("Ingrese la fecha inicial en la que desea conocer el top (AAAA-MM-DD): ")
    fecha_f =input("Ingrese la fecha final en la que desea conocer el top (AAAA-MM-DD): ")
    print('El top de taxis con mas puntos en el rango de fechas es: ')
    lista=controller.req_2_b(catalog,num,fecha_I,fecha_f)
    iterador=it.newIterator(lista)
    while it.hasNext(iterador):
        compañia=it.next(iterador)
        print(compañia["ID_T"], "con un numero de",round(compañia["Puntos"],2),"puntos")

def optionSeven():
    area_1=input("Ingrese la community area inicial: ")
    area_2=input("Ingrese la community area final: ")
    fecha_I =input("Ingrese la hora inicial (HH:MM): ")
    fecha_f =input("Ingrese la hora final (HH:MM): ")
    hora,recor,tiempo=controller.req_3(catalog,area_1,area_2,fecha_I,fecha_f)
    if hora ==None:
        print("No se encontraron viajes entre estas community areas en el rango de tiempo estimado...")
    else:
        print("La mejor hora para tomar el viaje es:", hora)
        print("La ruta para llegar a la community area",area_2,"es:\n")
        iterador=it.newIterator(recor)
        while it.hasNext(iterador):
            element=it.next(iterador)
            lt=element.split("_")
            print(lt[0])
        print("\nY el tiempo estimado de viaje es:", tiempo)



while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        catalog = controller.iniciar_catalog()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    elif int(inputs[0])==4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecucion: " + str(executiontime) )
    
    elif int(inputs[0])==5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecucion: " + str(executiontime) )
    elif int(inputs[0])==6:
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecucion: " + str(executiontime) )
    elif int(inputs[0])==7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecucion: " + str(executiontime) )
    else:
        sys.exit(0)
sys.exit(0)
