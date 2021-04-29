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

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def newCatalog ():
    catalog = model.newCatalog()
    return catalog
# Funciones para la carga de datos
def loadData (catalog):
    songfile1 = cf.data_dir + 'Subsamples/user_track_hashtag_timestamp/user_track_hashtag_timestamp-50pct.csv'
    input_file1 = csv.DictReader(open(songfile1, encoding='utf-8'), delimiter=",")
    songfile2 = cf.data_dir + 'Subsamples/context_content_features/context_content_features-50pct.csv'
    input_file2 = csv.DictReader(open(songfile2, encoding='utf-8'), delimiter=",")
    #songfile3 = cf.data_dir + 'Subsamples/sentiment_values.csv'
    #input_file3 = csv.DictReader(open(songfile3, encoding='utf-8'), delimiter=",")
    model.createCharact(catalog)
    model.createCharactSong(catalog)
    for song in input_file2:
        model.addContextSong(catalog['contextsong'], song)
    for song in input_file1:
            issong = model.songByUserId(catalog['contextsong'], song)
            if issong != None:
                model.addSongbyCharact(catalog, issong)
                model.addArtist(catalog, issong)
                model.addPista(catalog, issong)
                model.newAddSong(catalog)
    model.addSong(catalog)





           
        


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def reprodByCaractRange (catalog, characteristics, range ) :
    return  model.reprodByCaractRange(catalog, characteristics, range )

def SongsByCharactRange (catalog, characteristics, range ) :
    return 

def SongByInstruRangeAndTempoRange (catalog, characteristics, range ) :
    return 

def NumSongsByGenre (catalog, genre, range ) :
    return 