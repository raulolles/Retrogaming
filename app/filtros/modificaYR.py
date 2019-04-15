# -*- coding: utf-8 -*-
"""
Modifica las tablas Y, R después de hacer hacer una valoración un user
"""
import numpy as np
import sys

# Importa Matrices
Y = np.load('../static/datos/Y.npy')
R = np.load('../static/datos/R.npy')

'''
juego = sys.argv[1]
user = sys.argv[2]
valor = sys.argv[3]
'''
juego = 2909
user = 323
valor = 3

if valor == '--':
    valor = 0

Y[juego, user] = valor

if valor == 0:
    R[juego, user] = 0
else:
    R[juego, user] = 1

# Guarda tablas actualizadas
np.save('../static/datos/Y', Y)
np.save('../static/datos/R', R)


print (juego, user)
print (Y[juego, user])
print (R[juego, user])