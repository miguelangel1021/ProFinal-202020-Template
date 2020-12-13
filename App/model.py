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

import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import edge as e
from DISClib.ADT import stack as st
import datetime
assert config
 
"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def inicializar_catalogo():

    catalog={"Taxis_map":None, "Compañias":None, "Lista_taxis":None}
    catalog["Taxis_map"]=m.newMap(numelements=200001,
                                     maptype='PROBING',
                                     comparefunction=comparar_Taxis)
    catalog["Lista_taxis"]=lt.newList("ARRAY_LIST",comparar_lista_taxis)
    catalog["Compañias"]=lt.newList("ARRAY_LIST",Comparar_Compañias)
    catalog["Fechas"]=om.newMap(omaptype='RBT',
                                      comparefunction=compararFechas)
    catalog["Zonas"] = gr.newGraph(datastructure='ADJ_LIST',
                                  directed=True,
                                  size=1000,
                                  comparefunction=compararZonas)
    catalog["Horas"]=om.newMap(omaptype='RBT',
                                      comparefunction=comparar_Horas)
    return catalog


# Funciones para agregar informacion al grafo


def agregar_Zona(catalog,viaje):

    Hora_inicial=viaje["trip_start_timestamp"]
    Hora_final=viaje["trip_end_timestamp"]
    if Hora_inicial != "" and Hora_final != "":
        if viaje["pickup_community_area"] != "" and viaje['dropoff_community_area'] != ""  and viaje["pickup_community_area"] != viaje['dropoff_community_area']:
            if viaje['trip_seconds'] != "":
                Hora_I=encontrar_hora(Hora_inicial)
                Hora_F=encontrar_hora(Hora_final)
                mapa_horas(catalog,Hora_I)
                mapa_horas(catalog,Hora_F)
                origin = viaje['pickup_community_area']+"_"+Hora_I
                destination = viaje['dropoff_community_area']+"_"+Hora_F
                duration = float(viaje['trip_seconds'])
                addZone(catalog, origin)
                addZone(catalog, destination)
                addConnection(catalog, origin, destination, duration)
    
def encontrar_hora(hora):

    lt=hora.split("T")
    es=lt[1].split(":")
    hora=es[0]+":"+es[1]
     
    return hora 

def addZone(catalog, zona):
    
    if not gr.containsVertex(catalog ["Zonas"], zona):
            gr.insertVertex(catalog ["Zonas"], zona)
    return catalog

def addConnection(catalog, origin, destination, duration):
    
    edge = gr.getEdge(catalog["Zonas"], origin, destination)
    if edge is None:
        gr.addEdge(catalog["Zonas"], origin, destination, duration)
    else:
        e.updateAverageWeigth(edge,duration)
    
    return catalog


 
def cargar_taxis(catalogo,viaje):

    map_taxis=catalogo["Taxis_map"]
    ID_T=viaje["taxi_id"]
    lista_taxis=catalogo["Lista_taxis"]
    entry= m.get(map_taxis,ID_T)
    if entry is None :
        Taxi=new_Taxi(ID_T)
        Taxi["Numero_viajes"]+=1
        m.put(map_taxis,ID_T,Taxi)
    else:
        Taxi=me.getValue(entry)
        Taxi["Numero_viajes"]+=1

    if lt.isPresent(lista_taxis,ID_T) == 0:
            lt.addLast(lista_taxis,ID_T)
    Agregar_compañia(catalogo,ID_T,viaje)

def new_Taxi(ID_T):
    Taxi={"ID_T":ID_T,"Numero_viajes":0}
    return Taxi

def new_company(nombre):
    compañia={"Nombre":nombre, "Taxis_afiliados":None}
    compañia["Taxis_afiliados"]=lt.newList("ARRAY_LIST",comparar_lista_taxis)
    return compañia


def Agregar_compañia(catalogo,ID_T,viaje):

    lista_companies=catalogo["Compañias"]
    if viaje["company"] == None:
        compañia_nombre="Independent Owner"
    else:
        compañia_nombre=viaje["company"]

    entry= lt.isPresent(lista_companies,compañia_nombre)
    if entry == 0:
        compañia=new_company(compañia_nombre)
        lista_taxis=compañia["Taxis_afiliados"]
        if lt.isPresent(lista_taxis,ID_T) == 0:
            lt.addLast(lista_taxis,ID_T)
        lt.addLast(lista_companies,compañia)
    else:
        compañia=lt.getElement(lista_companies,entry)
        lista_taxis=compañia["Taxis_afiliados"]
        if lt.isPresent(lista_taxis,ID_T) == 0:
            lt.addLast(lista_taxis,ID_T)
        lt.changeInfo(lista_companies,entry,compañia)

def agregar_fecha(catalogo,viaje):
    map_fechas=catalogo["Fechas"]

    fecha=viaje["trip_start_timestamp"]
    lts=fecha.split("T")
    entry=om.get(map_fechas,lts[0])
    if entry is None:
        valor=new_fecha()
        if viaje["trip_miles"] != "0.0" and viaje["trip_total"] != "0.0":
            taxi=taxi_fecha()
            lt.addLast(taxi["Viajes"],viaje)
            m.put(valor["Viajes"],viaje["taxi_id"],taxi)
            om.put(map_fechas,lts[0],valor)
    else:
        valor=me.getValue(entry)
        if viaje["trip_miles"] != "0.0" and viaje["trip_total"] != "0.0":
            entry2=m.get(valor["Viajes"],viaje["taxi_id"])
            if entry2 is not None:
                taxi=me.getValue(entry2)
                lt.addLast(taxi["Viajes"],viaje)
            else:
                taxi=taxi_fecha()
                lt.addLast(taxi["Viajes"],viaje)
                m.put(valor["Viajes"],viaje["taxi_id"],taxi)
                
                               

def new_fecha():
    Fecha={"Viajes":None}
    Fecha["Viajes"]=m.newMap(numelements=2107,
                                     maptype='PROBING', comparefunction=comparar_Taxis)
    return Fecha

def taxi_fecha():
    taxi={"Viajes":None}
    taxi["Viajes"]=lt.newList("ARRAY_LIST")
    return taxi

# ==============================
# Funciones de consulta
# ==============================

def dar_numero_t_c(catalogo):
    compañias=catalogo["Compañias"]
    Numero_taxis=lt.size(catalogo["Lista_taxis"])
    Numero_compañias=m.size(compañias)
    return Numero_compañias,Numero_taxis

def Req_1_A(catalog,numero1):

    compañias=catalog["Compañias"]
    ins.insertionSort(compañias,greater)
    top_afiliados=lt.subList(compañias,1,numero1)
    return top_afiliados

def Req_1_B(catalog,numero2):
    
    taxis=catalog["Taxis_map"]
    compañias=catalog["Compañias"]
    iterador=it.newIterator(compañias)
    lista=lt.newList("ARRAY_LIST")
    while it.hasNext(iterador):
        compañia=it.next(iterador)
        dic={"compañia":compañia["Nombre"],"servicios":0}
        listataxis=compañia["Taxis_afiliados"]
        iterador2=it.newIterator(listataxis)
        while it.hasNext(iterador2):
            taxi=it.next(iterador2)
            
            entry=m.get(taxis,taxi)
            if entry is not None:
                valor=me.getValue(entry)
                servicios=valor["Numero_viajes"]
                dic["servicios"]+=servicios
        lt.addLast(lista,dic)
    ins.insertionSort(lista,greater2)
    top_servicios=lt.subList(lista,1,numero2)
    return top_servicios



def Req_2_A(catalogo,n_taxis,fecha):

    map_fechas=catalogo["Fechas"]
    entry=om.get(map_fechas,fecha)
    map_taxis=me.getValue(entry)
    lista_taxis=m.keySet(map_taxis["Viajes"])
    iterador=it.newIterator(lista_taxis)
    lista=lt.newList("ARRAY_LIST")
    while it.hasNext(iterador):
        ID_T=it.next(iterador)
        entry=m.get(map_taxis["Viajes"],ID_T)
        valor=me.getValue(entry)
        lista_viajes=valor["Viajes"]
        puntos=puntos_taxi(lista_viajes)
        taxi={"ID_T":ID_T,"Puntos":puntos}
        lt.addLast(lista,taxi)
    
    ins.insertionSort(lista,greater_Rec_2)
    lista_final=lt.subList(lista,1,n_taxis)
    return lista_final


def Req_2_B(catalog,n_taxis,fecha_inicial,fecha_final):
    map_fechas=catalog["Fechas"]
    lista_valores=om.values(map_fechas,fecha_inicial,fecha_final)
    iterador=it.newIterator(lista_valores)
    lista=lt.newList("ARRAY_LIST",comparar_lista_taxis)
    while it.hasNext(iterador):
        map_taxis=it.next(iterador)
        lista_taxis=m.keySet(map_taxis["Viajes"])
        iterador2=it.newIterator(lista_taxis)
        while it.hasNext(iterador2):
            ID_T=it.next(iterador2)
            entry=m.get(map_taxis["Viajes"],ID_T)
            valor=me.getValue(entry)
            lista_viajes=valor["Viajes"]
            puntos=puntos_taxi(lista_viajes)
            posicion=lt.isPresent(lista,ID_T)
            if  lt.isPresent(lista,ID_T) == 0:
                 taxi={"ID_T":ID_T,"Puntos":puntos}
                 lt.addLast(lista,taxi)
            else:
                taxi=lt.getElement(lista,posicion,)
                taxi["Puntos"]+=1
    ins.insertionSort(lista,greater_Rec_2)
    lista_final=lt.subList(lista,1,n_taxis)
    return lista_final

def mapa_horas(catalogo,hora):

    mapa=catalogo["Horas"]
    om.put(mapa,hora,hora)

def mejor_Horario(catalogo,area_origen,area_destino,hora_inicial,hora_final):

    grafo=catalogo["Zonas"]
    
    mapa_Horas=catalogo["Horas"]
    ultima=om.maxKey(mapa_Horas)
    lista=om.keys(mapa_Horas,hora_inicial,hora_final)
    lista2=om.keys(mapa_Horas,hora_inicial,ultima)
    iterador=it.newIterator(lista)
    mejor=1000000000
    mejor_Hora=None
    vertice=None
    while it.hasNext(iterador):
        hora=it.next(iterador)
        area=area_origen+"_"+hora
        if gr.containsVertex(grafo,area):
            recor=djk.Dijkstra(grafo,area)
            iterador2=it.newIterator(lista2)
            while it.hasNext(iterador2):
                hora2=it.next(iterador2)
                area_destin=area_destino+"_"+hora2
                if gr.containsVertex(grafo,area_destin):
                    tiempo=djk.distTo(recor,area_destin)
                    if tiempo < mejor:
                        mejor=tiempo
                        mejor_Hora=hora
                        vertice=area_destin
                        
    if mejor_Hora is not None:
        lista=lt.newList("ARRAY_LIST",comparar_zonas)
        area_es=area_origen+"_"+mejor_Hora
        recor=djk.Dijkstra(grafo,area_es)
        path_=djk.pathTo(recor,vertice)
        tiempo=djk.distTo(recor,area_destin)
    
        while (not st.isEmpty(path_)):
                stop = st.pop(path_)
                area1=stop["vertexA"]
                if lt.isPresent(lista,area1) == 0:
                    lt.addLast(lista,area1)
                area2=stop["vertexB"]
                if lt.isPresent(lista,area2) == 0:
                    lt.addLast(lista,area2)
    else:
        mejor_Hora,lista,mejor=None, None, None
    
    return mejor_Hora,lista,mejor
    

       
        
    
    


def puntos_taxi(lista_viajes):

    dinero_tot=0
    millas_tot=0
    iterador=it.newIterator(lista_viajes)
    while it.hasNext(iterador):
        viaje=it.next(iterador)
        if viaje["trip_total"] != "" and viaje["trip_miles"] != "":
            dinero=float(viaje["trip_total"])
            millas=float(viaje["trip_miles"])
            dinero_tot+=dinero
            millas_tot+=millas
    puntos=(millas_tot/dinero_tot)*lt.size(lista_viajes)
    return puntos
# ==============================
# Funciones Helper
# ==============================
def greater(element1, element2):
    if float(lt.size(element1['Taxis_afiliados']) )> float(lt.size(element2['Taxis_afiliados'])):
        return True

def greater2(element1, element2):
    if float(element1['servicios']) > float(element2['servicios']):
        return True

def greater_Rec_2(element1, element2):
    if float(element1['Puntos']) > float(element2['Puntos']):
        return True
# ==============================
# Funciones de Comparacion
# ==============================

def comparar_Taxis(Taxi1, Taxi2):
    

    taxi= me.getKey(Taxi2)
    if (Taxi1 == taxi):
        return 0
    elif (Taxi1 > taxi):
        return 1
    else:
        return -1
def comparar_Horas(hora1, hora2):
    

    
    if (hora1 == hora2):
        return 0
    elif (hora1 > hora2):
        return 1
    else:
        return -1
    
def Comparar_Compañias(Nombre_c, compañias):
    if (Nombre_c == compañias['Nombre'] ):
        return 0
    else:
        return 1

def comparar_lista_taxis(id, id2):
    if (id == id2 ):
        return 0
    else:
        return 1

def compararFechas(Fecha1, Fecha2):

    if (Fecha1 == Fecha2):
        return 0
    elif (Fecha1 > Fecha2):
        return 1
    else:
        return -1

def compararZonas(E1, E2):
   
    entry = me.getKey(E2)
    if (E1 == entry):
        return 0
    elif (E1 > entry):
        return 1
    else:
        return -1

def comparar_zonas(zona1,zona2):
    if zona1 == zona2:
        return 0
    else:
        return 1
