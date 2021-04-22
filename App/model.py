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

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog ():
    catalog = {'songs' : None,
                'hastags': None,
                'pistas': None,
                'artists': None,
                'numevent': 0,
                'contextsong': None}
    catalog['songs'] = lt.newList('ARRAY_LIST')
    catalog['pistas'] = lt.newList('ARRAY_LIST', cmpfunction = cmpBySong)
    catalog['artists'] = lt.newList('ARRAY_LIST', cmpfunction = cmpByartist)
    catalog['contextsong'] = mp.newMap(1000000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)

    return catalog
# Funciones para agregar informacion al catalogo
def addSong (catalog, song):
    songs = catalog['songs']
    charact = ["instrumentalness","liveness","speechiness","danceability","valence","loudness","tempo","acousticness","energy","mode","key"]
    for i in charact:
        dataentry = mp.get(songs, i)
        map = me.getValue(dataentry)
        entry = om.get(map, song[i])
        if entry is None:
            newentry = mp.newMap(1000000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
            om.put(map, song[i], newentry)
        else:
            newentry = me.getValue(entry)
        addCharactSong(newentry, song)
def addArtist (catalog, song):
    artist = song['artist_id']
    existartis = lt.isPresent(catalog['artists'], artist)
    if existartis == 0:
        lt.addLast(catalog['artists'], artist)

def addPista (catalog, song):
    pista = song['track_id']
    existpista = lt.isPresent(catalog['pistas'], pista)
    if existpista == 0:
        lt.addLast(catalog['pistas'], pista)

def newAddSong (catalog):
    catalog['numevent'] += 1


def addCharactSong (map, song):
    pista = song['track_id']
    existpista = mp.contains(map, pista)
    if existpista:
        entry = mp.get(map, pista)
        ltpista = me.getValue(entry)
    else:
        ltpista = lt.newList('ARRAY_LIST')
        mp.put(map, pista, ltpista)
    lt.addLast(ltpista, song)

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

# Funciones para creacion de datos
def newSong (song, contexsong):
    finalsong = None
    if song['user_id'] == contexsong['user_id'] and song['track_id'] == contexsong['track_id'] and song['created_at'] == contexsong['created_at']:
            contexsong['hashtag'] = song['hashtag']
            finalsong = contexsong
    return finalsong

def createCharact (catalog):
    catalog['songs'] =  mp.newMap(11,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=cmpByPista)
    map = catalog['songs']
    charact = ["instrumentalness","liveness","speechiness","danceability","valence","loudness","tempo","acousticness","energy","mode","key"]
    for i in charact:
        existcharact = mp.contains(map, i)
        if existcharact == False:
            entry = om.newMap(omaptype='RBT',comparefunction=cmpCharact)
            mp.put(map, i, entry)


# Funciones de consulta
def songByUserId(map, song):
    pista = song['user_id']
    existpista = mp.contains(map, pista)
    issong = None
    if existpista:
        entry = mp.get(map, pista)
        ltpista = me.getValue(entry)
        ejecutar = True
        i = 1
        while i < lt.size(ltpista) and ejecutar == True:
            song1 = lt.getElement(ltpista, i)
            issong = newSong(song, song1)
            if issong != None:
                ejecutar = False
            i += 1
    return issong
def reprodByCaractRange (catalog, characteristics, range ) :
    return  

def SongsByCharactRange (catalog, characteristics, range ) :
    return 

def SongByInstruRangeAndTempoRange (catalog, characteristics, range ) :
    return 

def NumSongsByGenre (catalog, genre, range ) :
    return 
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
def cmpByartist(key1, key2):
    if (key1 == key2):
        return 0
    elif (key1 > key2):
        return 1
    else:
        return -1
def cmpBySong(key1, key2):
    if (key1 == key2):
        return 0
    elif (key1 > key2):
        return 1
    else:
        return -1
# Funciones de ordenamiento
