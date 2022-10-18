# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 20:15:46 2022

@author: Equipo
"""

import matplotlib.pyplot as plt
import cv2
import os

pathImg = 'images'

files = os.listdir(pathImg)

for i, document in enumerate(files, start=1):
    path_imagen = pathImg + "/" + document
    path_anotacion = 'parsed_annotations' + "/" + document.split('.')[0] + ".txt"

    img = cv2.imread(path_imagen)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    dh, dw, _ = img.shape
            
    fl = open(path_anotacion, 'r')
    data = fl.readlines()
    fl.close()
            
    for dt in data:
                
        _, x, y, w, h = dt.split(' ')
                
        nx = int((float(x) - float(w)/2)*dw)
        ny = int((float(y) - float(h)/2)*dh)
        nw = int(float(w)*dw)
        nh = int(float(h)*dh)
        
        cv2.rectangle(img, (nx,ny), (nx+nw,ny+nh), (0,240,251), 2)
                
    plt.imshow(img)
    plt.title(path_imagen)
    plt.show()
    print("Imagenes mostradas: {}/{} \t {}%".format(i, len(files), 
                                                    round(i/len(files)*100,2)))