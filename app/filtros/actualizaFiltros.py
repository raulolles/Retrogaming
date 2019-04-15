import numpy as np

def actualiza_filtros():
	# Importa Matrices
	Y = np.load('app/static/datos/Y.npy')
	R = np.load('app/static/datos/R.npy')
	p_modelos = np.load('app/static/datos/P_Modelos.npy')
	p_mem_users = np.load('app/static/datos/P_Mem_Users.npy')
	p_mem_juegos = np.load('app/static/datos/P_Mem_Juegos.npy')

	n_juegos = Y.shape[0]

	# Actuliza Matrices de Predicciones
	media = np.matrix(np.mean(Y, axis=1))
	p_modelos = np.concatenate((p_modelos, media.T), axis=1)
	p_mem_users = np.concatenate((p_mem_users, media.T), axis=1)
	p_mem_juegos = np.concatenate((p_mem_juegos, media.T), axis=1)

	# Actuliza Y y R
	ceros = np.matrix(np.zeros(n_juegos))
	Y = np.concatenate((Y,ceros.T), axis=1)
	R = np.concatenate((R,ceros.T), axis=1)

	# Guarda tablas actualizadas
	np.save('app/static/datos/Y', Y)
	np.save('app/static/datos/R', R)
	np.save('app/static/datos/P_Modelos', p_modelos)
	np.save('app/static/datos/P_Mem_Users', p_mem_users)
	np.save('app/static/datos/P_Mem_Juegos', p_mem_juegos)


def actualiza_yr(juego, user, valor):
	# Importa Matrices
	Y = np.load('app/static/datos/Y.npy')
	R = np.load('app/static/datos/R.npy')

	if valor == '--' :
		valor = 0

	Y[juego,user] = valor

	if valor == 0:
		R[juego,user] = 0
	else:
		R[juego,user] = 1

	# Guarda tablas actualizadas
	np.save('app/static/datos/Y', Y)
	np.save('app/static/datos/R', R)
