# -*- coding: utf-8 -*-
"""
Filtro Colaborativo basodo en Productos
"""
import numpy as np

# Carga datos inicales - Matrices Y - R
y = np.load('../static/datos/Y.npy')
r = np.load('../static/datos/R.npy')
n_juegos,n_users = y.shape

# Crea matriz similitud (Coef.Corr.Pearson)
sim = np.corrcoef(y, rowvar=True)
# Da valor -1 a sim donde varianza de Y sea 0 (sin volores con NaN)
sim[np.where(np.isnan(sim))] = -1

# Crea matriz Predicción Filtro Colab. Productos
p_mem_juegos = np.copy(y)

# Recorre todos los juegos sin Valoración para generar Predicción
# indices de juegos [juego,usuario] a Predecir rating
ind_predecir = np.transpose(np.where(r==0))

for ind_p in ind_predecir:

    juego = ind_p[0]
    user = ind_p[1]

    #if (sim[:,juego]<=0).all is not None:
    # Indices a eliminar por sim negativa o ser el propio Juego
    ind_elim = np.array(np.where(sim[:,juego]<=0))
    ind_elim = np.append(ind_elim, juego)

    rating_user = np.delete(y[:,user], ind_elim)
    sim_juego = np.delete(sim[:,juego], ind_elim)

    suma_ddo = np.sum(rating_user * sim_juego)
    suma_dsor = np.sum(np.absolute(sim_juego))

    if suma_dsor > 0:
        p_mem_juegos[juego,user] = suma_ddo/suma_dsor


p_mem_juegos[np.where(np.isnan(p_mem_juegos))] = 0
p_mem_juegos[np.where(p_mem_juegos > 5)] = 5
p_mem_juegos[np.where(p_mem_juegos < 0)] = 0

# Guarda Matriz Pronosticos
np.save('../static/datos/P_Mem_Juegos', p_mem_juegos)