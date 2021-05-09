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
 """
import time
import tracemalloc
import config as cf
import model
import csv
import random
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def newCatalog ():
    catalog = model.newCatalog()
    return catalog
# Funciones para la carga de datos

def loadData (catalog):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    songfile1 = cf.data_dir + 'Subsamples/user_track_hashtag_timestamp/user_track_hashtag_timestamp-small.csv'
    input_file1 = csv.DictReader(open(songfile1, encoding='utf-8'), delimiter = ',')
    songfile2 = cf.data_dir + 'Subsamples/context_content_features/context_content_features-small.csv'
    input_file2 = csv.DictReader(open(songfile2, encoding='utf-8'), delimiter = ',')
    songfile3 = cf.data_dir + 'Subsamples/sentiment_values.csv'
    input_file3 = csv.DictReader(open(songfile3, encoding='utf-8'), delimiter=",")
    model.createCharact(catalog)
    model.createCharactSong(catalog)
    for dicc in input_file3:
        model.addHashtag(catalog['hashtags'], dicc)
    for song in input_file1:
        model.addContextSong(catalog['tracksong'], song)
    for song in input_file2:
        issong = model.songByUserId(catalog['tracksong'], song)
        if issong is not None:
            model.addSongbyCharact(catalog, issong)
            model.addArtist(catalog['artists'], issong)
            model.addPista(catalog['pistas'], issong)
            model.newAddSong(catalog)
    model.addSong(catalog)
    addGenre(catalog, None)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return (delta_time, delta_memory)

def addGenre (catalog, genre):
    Genre = [['Reggae',60,90],['Dowm-tempo',70,100],['Chill-out',90,120],['Hip-hop',85,115],['Jazz and Funk',120,125],['Pop',100,130],['RGB',60,80],['Rock',110,140],['Metal',100,160]]
    if genre is None:
        for i in Genre:
            model.addGenre(catalog['genre'], i)   
    else:
        model.addGenre(catalog['genre'], genre)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def reprodByCharactRange (catalog, characteristics, range ) :
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    reprod = model.reprodByCharactRange(catalog, characteristics, range)
    result = model.unicTrackorArtist(reprod[0], 'artist_id')

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return  ((reprod[1], result[1] ), (delta_time, delta_memory))

    

def songByTwoCharactRange (catalog, characteristics, range1, range2 ):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    reprod = model.reprodByCharactRange(catalog, characteristics[0], range1)
    reprod = model.reprodByCharactRangeLst(reprod[0], characteristics[1], range2)
    unictrack = model.unicTrackorArtist(reprod, 'track_id')
    result = model.selectResults(unictrack[0], 5, characteristics)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return ((unictrack[1], result), (delta_time, delta_memory))

def consultByGenre (catalog, genre) :
    entry = mp.get(catalog['genre'], genre)
    min = me.getValue(entry)[0]
    max = me.getValue(entry)[1]
    reprod = model.reprodByCharactRange(catalog, 'tempo', (min, max))
    unicartist = model.unicTrackorArtist(reprod[0], 'artist_id')


    return ((reprod[1], unicartist[1]),model.selectResults(unicartist[0], 5, characteristics= None))

def totalReprodByGenre (catalog, lstgenre):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    reprod = 0
    for genre in lstgenre:
        entry = mp.get(catalog['genre'], genre)
        min = me.getValue(entry)[0]
        max = me.getValue(entry)[1]
        reprod += model.reprodByCharactRange(catalog, 'tempo', (min, max))[1]

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return (reprod, (delta_time, delta_memory))

def resultReprodByGenre (catalog, lstgenre):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    for genre in lstgenre:
            entry = mp.get(catalog['genre'], genre)
            min = me.getValue(entry)[0]
            max = me.getValue(entry)[1]
            result = consultByGenre(catalog, genre)
            print ('For '+ genre.capitalize(), ' the tempo is between ', min, ' and ', max, ' BPM\n'+
            genre.capitalize(), ' reproductions: ', result[0][0], ' with ', result[0][1], ' different artists\n\n',
            '----- Some artists for '+ genre.capitalize()+ ' -----')
            for value in lt.iterator(result[1]):
                print (value)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return (delta_time, delta_memory)

def songByInstruRangeAndTempoRange (catalog, characteristics, range ) :
    return 

def sumSongsByGenre (catalog, genre, range ) :
    return 

def getTime():
        return float(time.perf_counter()*1000)

def getMemory():
    return tracemalloc.take_snapshot()

def deltaMemory(start_memory, stop_memory):

    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff

    delta_memory = delta_memory/1024.0
    return delta_memory