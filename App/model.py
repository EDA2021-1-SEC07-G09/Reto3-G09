"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
import random

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog ():
    catalog = {'songs' : None,
                'hashtags': None,
                'pistas': None,
                'artists': None,
                'numevent': 0,
                'tracksong': None,
                'issong': None,
                'genre': None}
    catalog['songs'] = mp.newMap(11,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
    catalog['hashtags'] = mp.newMap(6000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
    catalog['pistas'] = mp.newMap(1000000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
    catalog['artists'] = mp.newMap(1000000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
    catalog['tracksong'] = mp.newMap(1000000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)

    catalog['issong'] = mp.newMap(11,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
    catalog['genre'] = mp.newMap(11,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
                                

    return catalog
# Funciones para agregar informacion al catalogo
def addSong (catalog):
    songs = catalog['songs']
    #charact = ["created_at"]
    charact = ["instrumentalness","danceability","tempo","energy","created_at"]
    for i in charact:
        dataentry = mp.get(songs, i)
        map = me.getValue(dataentry)
        dataentry2 = mp.get(catalog['issong'], i)
        map2 = me.getValue(dataentry2)
        for j in lt.iterator(mp.keySet(map2)):
            if j:
                subentry = mp.get(map2, j)
                newentry = me.getValue(subentry)
                om.put(map, j, newentry)


def addArtist (map, song):
    artist = song['artist_id']
    existpista = mp.contains(map, artist)
    if existpista is False:
        mp.put(map, artist, song)

def addPista (map, song):
    pista = song['track_id']
    existpista = mp.contains(map, pista)
    if existpista is False:
        mp.put(map, pista, song)
        
def newAddSong (catalog):
    catalog['numevent'] += 1


def addGenre (map, genre):
    existgenre = mp.contains(map, genre[0])
    if existgenre is False:
        mp.put(map, genre[0], (genre[1], genre[2]))


def addContextSong (map, song):
    pista = song['user_id']
    existpista = mp.contains(map, pista)
    if existpista:
        entry = mp.get(map, pista)
        ltpista = me.getValue(entry)
    else:
        ltpista = lt.newList('ARRAY_LIST')
        mp.put(map, pista, ltpista)
    lt.addLast(ltpista, song)

def addHashtag (map, dicc):
    hashtag = dicc['hashtag']
    existpista = mp.contains(map, hashtag)
    if existpista is False:
        mp.put(map, hashtag, dicc)

def addTrack (map, song):
    pista = song['track_id']
    existpista = mp.contains(map, pista)
    if existpista:
        entry = mp.get(map, pista)
        ltpista = me.getValue(entry)
    else:
        ltpista = lt.newList('ARRAY_LIST')
        mp.put(map, pista, ltpista)
    lt.addLast(ltpista, song)

# Funciones para creacion de datos
def newSong (song, contexsong):
    finalsong = None
    if song['user_id'] == contexsong['user_id'] and song['track_id'] == contexsong['track_id'] and song['created_at'] == contexsong['created_at']:
            lt.addLast(contexsong['hashtag'], song['hashtag'])
            finalsong = contexsong
    return finalsong

def createCharact (catalog):
    map = catalog['songs']
    #charact = ["created_at"]
    charact = ["instrumentalness","danceability","tempo","energy","created_at"]
    for i in charact:
        entry = om.newMap(omaptype='RBT',comparefunction=cmpCharact)
        mp.put(map, i, entry)


def createCharactSong (catalog):
    map = catalog['issong']
    #charact = ["created_at"]
    charact = ["instrumentalness","danceability","tempo","energy","created_at"]
    for i in charact:
        entry = mp.newMap(100000,
                            maptype='PROBING',
                            loadfactor=0.5,
                            comparefunction=cmpByPista)
        mp.put(map, i, entry)

def addSongbyCharact (catalog, song):
    #charact = ["created_at"]
    charact = ["instrumentalness","danceability","tempo","energy","created_at"]
    for i in charact:
        entry = mp.get(catalog['issong'], i)
        map = me.getValue(entry)
        if i == "created_at":
            hora = song[i]
            pista = hora[11:]
        else:
            pista = float(song[i])
        existpista = mp.contains(map, pista)
        if existpista:
            entry = mp.get(map, pista)
            datapista = me.getValue(entry)
        else:
            datapista = lt.newList('ARRAY_LIST')
            mp.put(map, pista, datapista)
        lt.addLast(datapista, song)

def selectResults (lstvalues, num, characteristics):
    lstresults = lt.newList('ARRAY_LIST')
    pos = range(1,lt.size(lstvalues))
    pos = random.sample(pos, num)
    i = 1
    if characteristics is not None:
        for num in pos:
            song = lt.getElement(lstvalues, num)
            element = 'Track '+ str(i)+ ': '+ song['track_id']+ ' with '+ characteristics[0]+ ' of '+ song[characteristics[0]]+ ' and '+ characteristics[1]+ ' of '+ song[characteristics[1]]
            lt.addLast(lstresults, element)
            i += 1
    else:
        for num in pos:
            song = lt.getElement(lstvalues, num)
            element = 'Artist '+ str(i)+ ': '+ song['artist_id']
            lt.addLast(lstresults, element)
            i += 1
    
    return lstresults

# Funciones de consulta
def songByUserId(map, song):
    pista = song['user_id']
    existpista = mp.contains(map, pista)
    issong = None
    if existpista is True:
        song['hashtag'] = lt.newList('ARRAY_LIST')
        entry = mp.get(map, pista)
        ltpista = me.getValue(entry)
        '''for song1 in lt.iterator(ltpista):
            issong = newSong(song1, song)
            if issong is not None:
                u = lt.isPresent(ltpista, song1)
                lt.deleteElement(ltpista, u)
                break'''
        ejecutar = True
        i = 1
        while i <= lt.size(ltpista) and ejecutar == True:
            song1 = lt.getElement(ltpista, i)
            issong = newSong(song1, song)
            if issong is not None:
                lt.deleteElement(ltpista, i)
                ejecutar = False
            i += 1
    return issong

def reprodByCharactRange (catalog, characteristics, range ) :
    songs = catalog['songs']
    dataentry = mp.get(songs, characteristics)
    map = me.getValue(dataentry)
    lstpista = om.values(map, range[0], range[1])
    reprod = 0
    for value in lt.iterator(lstpista):
        reprod += lt.size(value)
    return (lstpista,reprod)

def reprodByCharactRangeLst (lstevent, characteristics, range ) :
    lstpista = lt.newList('ARRAY_LIST')
    for value in lt.iterator(lstevent):
        for pista in lt.iterator(value):
            if float(pista[characteristics]) >= range[0] and float(pista[characteristics]) <= range[1]:
                lt.addLast(lstpista, pista)
    return lstpista

def unicTrackorArtist (lstevent, id):
    map = mp.newMap(2000,
                    maptype='PROBING',
                    loadfactor=0.5,
                    comparefunction=cmpByPista)
    if lstevent['type'] == 'SINGLE_LINKED':
        for value in lt.iterator(lstevent):
            for song in lt.iterator(value):
                if id == 'track_id':
                    addPista(map, song)
                elif id == 'artist_id':
                    addArtist(map,song)
    else:
        for song in lt.iterator(lstevent):
            if id == 'track_id':
                addPista(map, song)
            elif id == 'artist_id':
                addArtist(map,song)
    lstvalues = mp.valueSet(map)

    return (lstvalues, mp.size(map))

# Funciones utilizadas para comparar elementos dentro de una lista
def cmpByPista(key, element):
        tagentry = me.getKey(element)
        if (str(key) == str(tagentry)):
                return 0
        elif (str(key) != str(tagentry)):
                return 1
        else:
                return 0
def cmpCharact(key1, key2):
    if (key1 == key2):
        return 0
    elif (key1 > key2):
        return 1
    else:
        return -1

# Funciones de ordenamiento
