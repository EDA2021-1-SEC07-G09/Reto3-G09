"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar reproducciones basadas en una carectarestica de contenido para un rango determinado")
    print("3- Consultar canciones segun caracteristicas de contenido con un rango determinado")
    print("4- Consultar canciones para rangos de "+ "Intrumentalness"+" y "+ "Tempo"+ " determinados")
    print("5- Consultar numero de canciones por genero con tempo prederteminado o genero al criterio del usuario")

def initCatalog():
    return controller.newCatalog()
    

def loadData(catalog):
    return controller.loadData(catalog)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        print('Eventos cargados: ' , catalog['numevent'])
        print('Numero Artistas: ' ,lt.size(catalog['artists']))
        print('Numero Pistas: ' ,lt.size(catalog['pistas']))
    elif int(inputs[0]) == 2:
        inputc = input('Ingrese la caracteristica: ')
        inputm = float(input('Ingrese el valor minimo: '))
        inputM = float(input('Ingrese el valor maximo: '))
        controller.reprodByCaractRange(catalog, inputc, (inputm, inoutM))
    elif int(inputs[0]) == 3:
        print('df')
    
    elif int(inputs[0]) == 4:
        print('df')

    else:
        sys.exit(0)
sys.exit(0)
