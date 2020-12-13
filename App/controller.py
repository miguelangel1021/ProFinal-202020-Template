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

import config as cf
from App import model
import csv
import os
import datetime
"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def iniciar_catalog():
    catalog= model.inicializar_catalogo()
    return catalog


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadTrips(catalog,num_archivos):
    lista_arch=os.listdir(cf.data_dir)
    
    for i in range(0,num_archivos):
        filename=lista_arch[i]
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(catalog, filename)
    return catalog
    

def loadFile(catalog, tripfile):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.cargar_taxis(catalog,trip)
        model.agregar_fecha(catalog,trip)
        model.agregar_Zona(catalog,trip)
    
    return catalog
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def num_t_c(catalog):
    companies,taxis=model.dar_numero_t_c(catalog)
    return companies,taxis

def req_1_a(catalog,num):
    top=model.Req_1_A(catalog,num)
    return top

def req_1_b(catalog,num):
    top=model.Req_1_B(catalog,num)
    return top

def req_2_a(catalog,n_taxis,fecha):
    top=model.Req_2_A(catalog,n_taxis, fecha)
    return top

def req_2_b(catalog,n_taxis,fecha_inicial,fecha_final):
    top=model.Req_2_B(catalog,n_taxis,fecha_inicial,fecha_final)
    return top

def req_3(catalogo,area_i,area_f,hora_inicial,hora_final):
    hora,recor,tiempo=model.mejor_Horario(catalogo,area_i,area_f,hora_inicial,hora_final)
    return hora,recor,tiempo