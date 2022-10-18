# -*- coding: utf-8 -*-
"""
Created on Sat May 14 11:28:31 2022

@author: Antonio José Aroca Aguilar
"""

import os

path = './test/labels' # introducir ruta
files = os.listdir(path)

for file in files:
    
    file = path + '/' + file
    contenido= list()
    
    with open(file, 'r') as archivo:
       for linea in archivo:
           print(linea)
           
    with open(file, 'r') as archivo:
       for linea in archivo:
           columnas = linea.split(' ')
           columnas[0] = '0'
           contenido.append(' '.join(columnas))
    
    with open(file, 'w') as archivo:
        archivo.writelines(contenido)
    
    with open(file, 'r') as archivo:
       for linea in archivo:
           print(linea)
    print('-----------------------')