# -*- coding: utf-8 -*-
"""
Filtro Colaborativo basodo en Usuarios
"""
import numpy as np

# Carga datos inicales - Matrices Y - R
y = np.load('..\static\datos\Y.npy')
r = np.load('..\static\datos\R.npy')
nJuegos,nUsers = y.shape

# Crea matriz similitud (Coef.Corr.Pearson)
sim = np.corrcoef(y, rowvar=False)

# Da valor -1 a sim donde varianza de Y sea 0 (sin volores con NaN)
sim[np.where(np.isnan(sim))] = -1

# Crea matriz Predicción Filtro Colab. Usuarios
p_mem_users = np.copy(y)

# Recorre todos los juegos sin Valoración para generar Predicción
# indices de juegos a Predecir rating
ind_predecir = np.transpose(np.where(r==0))

for ind_p in ind_predecir:

    juego = ind_p[0]
    user = ind_p[1]
    suma_ddo = 0
    suma_dsor = 0

    # Recorre todos los users que han jugado al juego y similutid > 0
    # indices de users que han jugado a juego a predecir para User
    ind_jugado = np.transpose(np.where(r[juego,:]==1))
    ind_jugado = ind_jugado[:,0]
    ind_jugado_red = list(filter(lambda x: (sim[x,user]>0), ind_jugado))

    # Controla que no hay ningún usuario con sim > 0
    if len(ind_jugado_red) > 0:
        for i_user_jdo in ind_jugado_red:
            suma_ddo = suma_ddo + (y[juego,i_user_jdo]-y[:,i_user_jdo].mean()) * sim[i_user_jdo,user]
            suma_dsor = suma_dsor + np.absolute(sim[i_user_jdo,user])

        predicc = y[:,user].mean() + (suma_ddo/suma_dsor)
        if predicc > 0:
            p_mem_users[juego,user] = predicc

p_mem_users[np.where(np.isnan(p_mem_users))] = 0
p_mem_users[np.where(p_mem_users > 5)] = 5
p_mem_users[np.where(p_mem_users < 0)] = 0

# Guarda Matriz Pronosticos
np.save('../static/datos/P_Mem_Users', p_mem_users)
