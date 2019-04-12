# -*- coding: utf-8 -*-
"""
Genera las Tablas Y R a partir de:
    - cantidad de juegos
    - 1000 usuarios ficticios con 100 valoraciones aleatorias por usuario

Matriz Y: ratings
Matriz X: juegos valorados
"""

import numpy as np
import random


rating_max = 5
n_users = 1000
n_valoraciones = 100


# Genera valoraciones aleatorias entre 0 y 5
def genera_tablas(n_juegos):

    # Crea Y R a zeros
    y = np.zeros ((n_juegos, n_users), dtype = np.float)
    r = np.zeros ((n_juegos, n_users), dtype = np.int)

    # Rellena Y
    for user in range(n_users):
		i = 0
		while i < n_valoraciones:
			y[random.randint(0,n_juegos-1), user] = random.randint(0, rating_max)
			i = i+1

    # Genera R
    r[y>0]=1

    # Guarda Matrices
    np.save('../static/datos/Y', y)
    np.save('../static/datos/R', r)