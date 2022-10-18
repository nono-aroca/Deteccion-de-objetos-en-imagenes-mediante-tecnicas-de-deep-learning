# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 16:43:36 2022

@author: Antonio José Aroca Aguilar
"""

###############################################################################
################################### IMPORTS ###################################
###############################################################################

import os
from xml.dom import minidom


###############################################################################
############################# CONSTANTES GLOBALES #############################
###############################################################################

#path de los directorios
path = "C:/Users/Equipo/Desktop/TFM/dataset/annotations"
new_path = "C:/Users/Equipo/Desktop/TFM/dataset/parsed_annotations"

#diccionario de clases
diccionario_clases = {'trafficlight': 0, 'stop': 1, 'speedlimit': 2, 
                      'crosswalk': 3}


###############################################################################
########################### DEFINICION DE FUNCIONES ###########################
###############################################################################

def convertirCoordenadas(x_min: int, y_min: int, x_max: int, y_max: int,
                         width: int, height: int) -> tuple:
    """Permite convertir las coordenadas de un bounding box del formato xml a yolo.
    
    La función permite convertir los datos de un bounding box extraido a través
    del formato xml, es decir, sus cuatro esquinas, al formato requerido por 
    yolo. Esto es, las coordenadas del centro del bounding box y su ancho y alto.
    Todo esto teniendo en cuenta que yolo trabaja con coordenadas delimitadas 
    por el intervalo [0,1].
    """
    
    #Pasamos los datos a float para poder operar correctamente
    x_min = float(x_min)
    y_min = float(y_min)
    x_max = float(x_max)
    y_max = float(y_max)
    width = float(width)
    height = float(height)
    
    #Convertimos el bounding box al formato requerido (punto medio y tamaño)
    x = (x_min + x_max) / 2.0
    y = (y_min + y_max) / 2.0
    w = x_max - x_min
    h = y_max - y_min
    
    #Las hacemos relativas al tamaño de la imagen
    dw = 1.0/width
    dh = 1.0/height
    
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    
    return (x, y, w, h)


def parseFile(filepath: str, path_destino: str) -> None:
    """Permite transformar anotaciones de detección de objetos de xml a formato yolo.
    
    La función permite convertir las anotaciones de detección de objetos de una
    imagen del formato xml a un txt en formato yolo. Para ello recibe la ruta 
    del archivo xml con las anotaciones y la ruta del archivo de salida.
    """
    
    #Extraemos los objetos anotados y tamaño de la imagen
    informacion = minidom.parse(filepath)
    
    objetos = informacion.getElementsByTagName('object')
    
    size = informacion.getElementsByTagName('size')[0]
    width = int((size.getElementsByTagName('width')[0]).firstChild.data)
    height = int((size.getElementsByTagName('height')[0]).firstChild.data)
    
    #Vamos procesando cada objeto por separado y escribiendo los datos en el archivo
    with open(path_destino, "w") as f:
        
        for item in objetos:
                
            #Obtenemos la clase y las coordenadas del bounding box
            clase =  (item.getElementsByTagName('name')[0]).firstChild.data
            x_min = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
            y_min = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
            x_max = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
            y_max = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
            
            #Convertimos las coordenadas y la clase al formato yolo
            clase_yolo = diccionario_clases[clase]
            bounding_box = convertirCoordenadas(x_min, y_min, x_max, y_max, width, height)
            
            #Escribimos el nuevo archivo con los datos parseados
            f.write(str(clase_yolo) + " " + " ".join([("%.6f" % coord) for coord in bounding_box]) + '\n')
    


###############################################################################
#################################### MAIN #####################################
###############################################################################

#Obtenemos todos los archivos del directorio
files = os.listdir(path)

#Parseamos cada archivo
for i, document in enumerate(files, start=1):
    filepath = path + "/" + document
    new_filepath = new_path + "/" + document.split('.')[0] + ".txt"
    parseFile(filepath, new_filepath)
    print("Archivos parseados: {}/{} \t {}%".format(i, len(files), 
                                                    round(i/len(files)*100,2)))
