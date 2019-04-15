# -*- coding: utf-8 -*-
"""
Filtro Colaborativo basado en Modelos
"""

import numpy as np
from scipy.optimize import minimize


# Calculo del Coste (J) y el Gradiante de J
def cofi_cost_func (parameters, y, r, n_users, n_juegos, n_features, lamb):

    cost=0
    gradient=np.zeros_like(parameters)

    # Matriz X y Theta
    x = parameters[0 : n_juegos*n_features]
    x = x.reshape(n_juegos, n_features)
    theta = parameters[n_juegos*n_features :]
    theta = theta.reshape(n_users, n_features)

    # Coste
    matriz_hipot = x.dot(theta.T)
    matriz_error = (matriz_hipot - y) * r
    matriz_error_cuad = matriz_error ** 2
    matriz_error_cuad_pel_vista = matriz_error_cuad

    error = np.sum(matriz_error_cuad_pel_vista)
    cost = error * 0.5

    # regularización
    cost = cost + np.sum(lamb*0.5*(x*x))
    cost = cost + np.sum(lamb*0.5*(theta*theta))

    # Gradiante
    grad_x = matriz_error.dot(theta) + lamb * x
    grad_theta = matriz_error.T.dot(x) + lamb * theta
    gradient = np.append(grad_x.flatten(), grad_theta.flatten())

    return (cost, gradient)


# Define a function to be minimized
def cofi_cost_func_minimize(parameters):
    return cofi_cost_func(parameters,y, r, n_users, n_juegos, n_feat,lamb)


# Carga datos inicales - Matrices Y - R
y = np.load('../static/datos/Y.npy')
r = np.load('../static/datos/R.npy')

n_juegos,n_users = y.shape
n_feat = 10
lamb = 10
max_iter=200
initParam = np.random.rand(1, n_users*n_feat + n_juegos*n_feat)

# Minimize the function using minimize from the package scipy.optimize and get the optimized parameters
parameters = (minimize(cofi_cost_func_minimize,initParam,method="CG",jac=True,
				   options={'maxiter':max_iter, "disp":True})).x


# Matriz X y Theta
x = parameters[0 : n_juegos*n_feat]
x = x.reshape(n_juegos, n_feat)
theta = parameters[n_juegos*n_feat :]
theta = theta.reshape(n_users, n_feat)

# Predicciones
p_modelos = np.dot(x, theta.T)


p_modelos[np.where(np.isnan(p_modelos))] = 0
p_modelos[np.where(p_modelos > 5)] = 5
p_modelos[np.where(p_modelos < 0)] = 0

# Graba la matriz de predicción
np.save('../static/datos/P_Modelos', p_modelos)
