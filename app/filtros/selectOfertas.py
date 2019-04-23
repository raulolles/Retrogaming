import numpy as np
import pandas as pd
from pandas import read_table
import random
import jellyfish as jel

def calcula_estad_juego(juego,y,r):
	tabla_estad = list()

	y_juego = y[juego,:]
	users_jugado = int(np.sum(r[juego,:]))
	puntuacion = np.sum(y_juego)
	puntuacion_media = puntuacion/users_jugado
	imagen_punt = imagen_puntuacion(puntuacion_media)

	tabla_estad.append(str("{:.1f}".format(puntuacion_media)))
	tabla_estad.append(imagen_punt)
	tabla_estad.append(users_jugado)

	tabla_estad.append(len(np.where(y_juego ==5)[0]))
	tabla_estad.append(len(np.where(y_juego ==4)[0]))
	tabla_estad.append(len(np.where(y_juego ==3)[0]))
	tabla_estad.append(len(np.where(y_juego ==2)[0]))
	tabla_estad.append(len(np.where(y_juego ==1)[0]))

	return tabla_estad


def imagen_puntuacion(puntuacion):
	if puntuacion > -0.5 and puntuacion <= 0.4:
		str_imagen = "simbolos/star_cero.png"
	elif puntuacion < 1:
		str_imagen = "simbolos/star_cero_med.png"
	elif puntuacion < 1.4:
		str_imagen = "simbolos/star_uno.png"
	elif puntuacion < 2:
		str_imagen = "simbolos/star_uno_med.png"
	elif puntuacion < 2.4:
		str_imagen = "simbolos/star_dos.png"
	elif puntuacion < 3:
		str_imagen = "simbolos/star_dos_med.png"
	elif puntuacion < 3.4:
		str_imagen = "simbolos/star_tres.png"
	elif puntuacion < 4:
		str_imagen = "simbolos/star_tres_med.png"
	elif puntuacion < 4.4:
		str_imagen = "simbolos/star_cuatro.png"
	elif puntuacion < 5:
		str_imagen = "simbolos/star_cuatro_med.png"
	else:
		str_imagen = "simbolos/star_cinco.png"

	return str_imagen


def importa_tablas(origen_datos):
	# Importa Matrices
	y = np.load(origen_datos+'Y.npy')
	r = np.load(origen_datos+'R.npy')
	p_modelos = np.load(origen_datos+'P_Modelos.npy')
	p_mem_users = np.load(origen_datos+'P_Mem_Users.npy')
	p_mem_juegos = np.load(origen_datos+'P_Mem_Juegos.npy')

	# Importa Datos del scraping
	items = read_table(origen_datos+'datosJuegos.csv',header=None,sep=';',encoding='ISO-8859-1')
	items.columns = ['juego','fabricante','visitas', 'favoritos', 'comentarios', 'url']

	return y, r, p_modelos, p_mem_users, p_mem_juegos, items


def importa_tablas_2(origen_datos):
	# Importa Matrices
	y = np.load(origen_datos+'Y.npy')
	r = np.load(origen_datos+'R.npy')

	# Importa Datos del scraping
	items = read_table(origen_datos+'datosJuegos.csv',header=None,sep=';',encoding='ISO-8859-1')
	items.columns = ['juego','fabricante','visitas', 'favoritos', 'comentarios', 'url']

	return y, r, items


def select_de_matriz(y,p,r,id_user,unid_select,items):
	r0 = r[:,id_user]
	# Crea una matriz en la que se guardan los indices, R0 y P0
	p0= p[:,id_user]

	jugado = 0

	tabla_slc = crea_tabla_slc(p0, r0, True, jugado)
	seleccion = ejecuta_seleccion (id_user, items, y, r, unid_select, tabla_slc)

	return seleccion


def select_predicciones(origen_datos, id_user):
	unid_select = 5
	y, r, p_modelos, p_mem_users, p_mem_juegos, items = importa_tablas(origen_datos)

	select_users = select_de_matriz(y,p_mem_users,r,id_user,unid_select,items)
	select_juegos = select_de_matriz(y,p_mem_juegos,r,id_user,unid_select,items)
	select_modelos = select_de_matriz(y,p_modelos,r,id_user,unid_select,items)

	return select_modelos, select_users, select_juegos


def select_aleatorio(origen_datos):
	unid_select = 6
	y, r, items = importa_tablas_2(origen_datos)
	n_juegos = y.shape[0]
	n_juegos = n_juegos-1
	seleccion = list()
	linea_select_a = list()
	linea_select_b = list()

	i = 0
	while i < unid_select:
		juego = random.randint(0,n_juegos)
		linea_select_a = items.loc[juego].values.tolist()
		linea_select_b = calcula_estad_juego(juego,y,r)
		seleccion.append(linea_select_a + linea_select_b)
		i = i+1

	return seleccion


def select_favoritos(origen_datos, id_user):
	unid_select = 15
	y, r, items = importa_tablas_2(origen_datos)
	r0 = r[:,id_user]

	# Crea una matriz en la que se guardan los indices, R0 y P0
	y0= y[:,id_user]

	jugado = 1

	tabla_slc = crea_tabla_slc(y0, r0, True, jugado)
	seleccion = ejecuta_seleccion (id_user, items, y, r, unid_select, tabla_slc)

	return seleccion


def select_mas_jugados(origen_datos, id_user, jugado):
	unid_select = 15
	y, r, items = importa_tablas_2(origen_datos)
	r0 = r[:,id_user]

	# Crea una matriz en la que se guardan los indices, R0 y suma juegos
	veces_jug = r.sum(axis = 1)

	tabla_slc = crea_tabla_slc(veces_jug, r0, True, jugado)
	seleccion = ejecuta_seleccion (id_user, items, y, r, unid_select, tabla_slc)

	return seleccion


def select_mejor_valorados(origen_datos, id_user, jugado):
	unid_select = 15
	y, r, items = importa_tablas_2(origen_datos)
	r0 = r[:,id_user]

	# Crea una matriz en la que se guardan los indices, R0 y suma juegos
	valor_medio = y.sum(axis = 1) / r.sum(axis = 1)
	valor_medio[np.where(np.isnan(valor_medio))] = 0

	tabla_slc = crea_tabla_slc(valor_medio, r0, True, jugado)
	seleccion = ejecuta_seleccion (id_user, items, y, r, unid_select, tabla_slc)

	return seleccion


def select_archive(origen_datos, id_user,columna,jugado):
	unid_select = 15
	y, r, items = importa_tablas_2(origen_datos)
	r0 = r[:,id_user]

	# Crea una matriz en la que se guardan los indices, R0 y suma juegos
	datos = pd.to_numeric(items[columna].tolist())

	tabla_slc = crea_tabla_slc(datos, r0, True, jugado)
	seleccion = ejecuta_seleccion (id_user, items, y, r, unid_select, tabla_slc)

	return seleccion


def select_busqueda(origen_datos, id_user, palabra_busq):
	unid_select = 15
	y, r, items = importa_tablas_2(origen_datos)
	r0 = r[:,id_user]

	# Crea lista con distancia (Levenshtein )
	distancia = list()
	palabra_busq = palabra_busq.lower()
	for i in range(len(r0)):
		palabra = items.loc[i][0].lower()
		dist_min = np.inf
		for p in palabra.split():
			if palabra_busq in p:
				dist = 0
				if dist < dist_min:
					dist_min = dist

			dist = jel.levenshtein_distance(palabra_busq, p)
			if dist < dist_min:
				dist_min = dist
		distancia.append(dist_min)

	jugado = 3

	tabla_slc = crea_tabla_slc(distancia, r0, False, jugado)
	seleccion = ejecuta_seleccion (id_user, items, y, r, unid_select, tabla_slc)

	return seleccion

def select_busqueda_avanz(origen_datos, id_user, param):
	unid_select = 15
	y, r, items = importa_tablas_2(origen_datos)
	r0 = r[:,id_user]

	# Crea tabla con id_jgo, vistas, stars, comment, valor, media, jugados, distancia(q)
	ind = range(0, len(r0))
	visitas = pd.to_numeric(items['visitas'].tolist())
	star = pd.to_numeric(items['favoritos'].tolist())
	comm = pd.to_numeric(items['comentarios'].tolist())
	valor = y[:,id_user]
	media = y.sum(axis = 1) / r.sum(axis = 1)
	jugados = r.sum(axis=1)
	distancia = range(0, len(r0))
	l = np.concatenate((ind, r0, visitas, star, comm, valor, media, jugados, distancia))
	l = l.reshape(9, len(r0))
	l = l.T

	# Discriminación en funcion de jugados
	if param['jugados'] == 'no_jugados':
		l = l[np.where(l[:,1] == 0)]
	elif param['jugados'] == 'si_jugados':
		l = l[np.where(l[:,1] == 1)]

	# Seleccina de la tabla según parámetros
	l = l [np.where(l[:,2] >= int(param['vist_min']))]
	l = l [np.where(l[:,2] <= int(param['vist_max']))]

	l = l [np.where(l[:,3] >= int(param['star_min']))]
	l = l [np.where(l[:,3] <= int(param['star_max']))]

	l = l [np.where(l[:,4] >= int(param['comm_min']))]
	l = l [np.where(l[:,4] <= int(param['comm_max']))]

	l = l [np.where(l[:,5] >= int(param['valo_min']))]
	l = l [np.where(l[:,5] <= int(param['valo_max']))]

	l = l [np.where(l[:,6] >= int(param['medi_min']))]
	l = l [np.where(l[:,6] <= int(param['medi_max']))]

	l = l [np.where(l[:,7] >= int(param['juga_min']))]
	l = l [np.where(l[:,7] <= int(param['juga_max']))]


	# Si hay juegos en l y hay palabra de búsqueda
	if len(l) > 0 and param['q'] != '':
		palabra_busq = param['q'].lower()
		for valor in l:
			palabra = items.loc[valor[0]][0].lower()
			dist_min = np.inf
			for p in palabra.split():
				if palabra_busq in p:
					dist = 0
					if dist < dist_min:
						dist_min = dist

				dist = jel.levenshtein_distance(palabra_busq, p)
				if dist < dist_min:
					dist_min = dist
			valor[8] = dist_min

		# ordena la tabla por distancia
		l = l[l[:,8].argsort()]

	seleccion = ejecuta_seleccion (id_user, items, y, r, unid_select, l)

	return seleccion


def calcula_limites_busq(origen_datos, id_user):
	y, r, items = importa_tablas_2(origen_datos)
	limites = {'vist_min': items['visitas'].min(),
			'vist_max': items['visitas'].max(),
			'star_min': items['favoritos'].min(),
			'star_max': items['favoritos'].max(),
			'comm_min': items['comentarios'].min(),
			'comm_max': items['comentarios'].max(),
			'valo_min': np.min(y[:,id_user]),
			'valo_max': np.max(y[:,id_user]),
			'medi_min': 0,
			'medi_max': 5,
			'juga_min': (np.min(r.sum(axis=1))),
			'juga_max': (np.max(r.sum(axis=1)))}
	return limites


def crea_tabla_slc (criterio_slc, r0, ascendiente, jugado):
	# Crea una matriz en la que se guardan los indices, R0 y criterio_slc
	ind = range(0, len(r0))
	l = np.concatenate((ind, r0, criterio_slc))
	l = l.reshape(3, len(r0))
	l = l.T

	if jugado == 0:
		l = l[np.where(l[:,1] == 0)]  # deja en la matriz los juegos no jugados
	elif jugado == 1:
		l = l[np.where(l[:,1] == 1)]  # deja en la matriz los juegos si jugados

	# Ordena la matriz
	l = l[l[:,2].argsort()]

	if ascendiente:
		l = np.flipud(l)

	return l

def ejecuta_seleccion (id_user, items, y, r, unid_select, l):
	seleccion = list()
	linea_select_a = list()
	linea_select_b = list()

	if unid_select > len(l):
		unid_select = len(l)

	for i in range (unid_select):
		juego = int(l[i][0])
		linea_select_a = items.loc[juego].values.tolist()
		linea_select_b = calcula_estad_juego(juego,y,r)
		valor = int(y[juego,id_user])

		seleccion.append(linea_select_a + linea_select_b + [valor, juego, id_user])

	return seleccion


def actualiza_selec(id_juego, valor, seleccion_total):
	# Recorre todas las selecciones que incluya el total
	for slc_parcial in seleccion_total:

		# Recorre la seleccion en particular
		for slc in slc_parcial['select']:

			slc = actualiza_selec2(slc, id_juego, valor)

		# fin for parcial
	#fin for total
	return seleccion_total


def actualiza_selec2(slc, id_juego, valor):
	# Actualiza los valores del juego si existe
	if slc[15] == id_juego:

		# slc[8] == Numero usuarios     #slc[14] == Puntuacion
		# slc[9] - slc[13] == 5 stars - 1 star

		if slc[14] == 0:
			slc[8] = slc[8] + 1
		else:
			ind_menos = 14 - slc[14]
			slc[ind_menos] = slc[ind_menos] - 1

		if valor == 0:
			slc[8] = slc[8] - 1
		else:
			ind_mas = 14 - valor
			slc[ind_mas] = slc[ind_mas] + 1

		# Puntuacion y  Media
		slc[14] = valor
		slc[6] = str("{:.1f}".format((slc[9]*5 + slc[10]*4 + slc[11]*3 + slc[12]*2 + slc[13])/slc[8]))
		slc[7] = imagen_puntuacion((slc[9]*5 + slc[10]*4 + slc[11]*3 + slc[12]*2 + slc[13])/slc[8])

	return slc

