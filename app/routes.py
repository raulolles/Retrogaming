from flask import render_template, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app.filtros.selectOfertas import select_predicciones, select_favoritos, select_aleatorio, select_mejor_valorados, select_mas_jugados, actualiza_selec, select_busqueda, select_archive, select_busqueda_avanz, calcula_limites_busq
from app.filtros.actualizaFiltros import actualiza_filtros, actualiza_yr
from app.internalizacion.lenguajes import carga_dicc_lenguaje

import copy

selec = list()
origen_datos = "app/static/datos/"

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_modelos, select_users, select_juegos = select_predicciones(origen_datos, id_user)
	selecciones = [{'filtro': txt['pg_ind_tit_selec_modelos'], 'select':select_modelos}, {'filtro': txt['pg_ind_tit_selec_usuarios'], 'select':select_users}, {'filtro': txt['pg_ind_tit_selec_productos'], 'select':select_juegos}]
	selec = selecciones
	return redirect(url_for('index2'))

@app.route('/index2', methods=['GET', 'POST'])
@login_required
def index2():
	txt = control_lenguaje(request.args,'index')
	jg_ifrm = control_parametros(request.args)
	texto = txt['pg_ind_text']
	return render_template('index.html', txt=txt, title='Home', selecciones=selec, texto_cab=texto, jg_ifrm=jg_ifrm)


@app.route('/login', methods=['GET', 'POST'])
def login():
	txt = control_lenguaje(request.args)
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	select_aleat = select_aleatorio(origen_datos)
	selecciones =[{'filtro':'', 'select':select_aleat}]
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash(txt['pg_login_error_ident'])
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', txt=txt, title='Sign In', form=form, selecciones=selecciones)


@app.route('/favoritos', methods=['GET', 'POST'])
@login_required
def favoritos():
		global selec
		txt = control_lenguaje(request.args)
		id_user = current_user.id - 1
		select_fav = select_favoritos(origen_datos, id_user)
		selecciones =[{'filtro':txt['pg_ind_tit_selec_favoritos'], 'select':select_fav}]
		selec = selecciones
		return redirect(url_for('favoritos2'))


@app.route('/favoritos2', methods=['GET', 'POST'])
@login_required
def favoritos2():
	txt = control_lenguaje(request.args, 'favoritos')
	jg_ifrm = control_parametros(request.args)
	texto = txt['pg_ind_text_favoritos']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec, 'favoritos2')
	return render_template('index.html', txt=txt, title='Favoritos', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag=page, total_pag=total_pag, jg_ifrm=jg_ifrm)


@app.route('/mas_jugados_todos', methods=['GET', 'POST'])
@login_required
def mas_jugados_todos():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_mas_jug = select_mas_jugados(origen_datos, id_user,3)
	selecciones =[{'filtro': txt['pg_ind_tit_selec_mas_jugados']+txt['pg_ind_tit_selec_todos_juegos'], 'select':select_mas_jug}]
	selec = selecciones
	return redirect(url_for('mas_jugados2_todos'))


@app.route('/mas_jugados2_todos', methods=['GET', 'POST'])
@login_required
def mas_jugados2_todos():
	txt = control_lenguaje(request.args, 'mas_jugados_todos')
	jg_ifrm = control_parametros(request.args)
	texto= txt['pg_ind_text_mas_jugados_todos']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec, 'mas_jugados2_todos')
	return render_template('index.html', txt=txt, title='Mas Jugados', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag=page, total_pag=total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_jugados_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_jugados_ya_jugado():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_mas_jug = select_mas_jugados(origen_datos, id_user,1)
	selecciones =[{'filtro': txt['pg_ind_tit_selec_mas_jugados']+txt['pg_ind_tit_selec_ya_jugados'], 'select':select_mas_jug}]
	selec = selecciones
	return redirect(url_for('mas_jugados2_ya_jugado'))


@app.route('/mas_jugados2_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_jugados2_ya_jugado():
	txt = control_lenguaje(request.args, 'mas_jugados_ya_jugado')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mas_jugados_todos']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec, 'mas_jugados2_ya_jugado')
	return render_template('index.html', txt=txt, title='Mas Jugados', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag=page, total_pag=total_pag, jg_ifrm=jg_ifrm)


@app.route('/mas_jugados_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_jugados_no_jugado():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_mas_jug = select_mas_jugados(origen_datos, id_user,0)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_jugados']+txt['pg_ind_tit_selec_no_jugados'], 'select':select_mas_jug}]
	selec = selecciones
	return redirect(url_for('mas_jugados2_no_jugado'))


@app.route('/mas_jugados2_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_jugados2_no_jugado():
	txt = control_lenguaje(request.args, 'mas_jugados_no_jugado')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mas_jugados_todos']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec, 'mas_jugados2_no_jugado')
	return render_template('index.html', txt=txt, title='Mas Jugados', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag=page, total_pag=total_pag, jg_ifrm=jg_ifrm)



@app.route('/mejor_valorados_todos', methods=['GET', 'POST'])
@login_required
def mejor_valorados_todos():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_mejor_valorados(origen_datos, id_user, 3)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mejor_valorados']+txt['pg_ind_tit_selec_todos_juegos'], 'select':select_valor}]
	selec = selecciones
	return redirect(url_for('mejor_valorados2_todos'))


@app.route('/mejor_valorados2_todos', methods=['GET', 'POST'])
@login_required
def mejor_valorados2_todos():
	txt = control_lenguaje(request.args, 'mejor_valorados_todos')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mejor_valor_todos']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'mejor_valorados2_todos')
	return render_template('index.html', txt=txt, title='Mejor Valorados', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)


@app.route('/mejor_valorados_ya_jugado', methods=['GET', 'POST'])
@login_required
def mejor_valorados_ya_jugado():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_mejor_valorados(origen_datos, id_user, 1)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mejor_valorados']+txt['pg_ind_tit_selec_ya_jugados'], 'select':select_valor}]
	selec = selecciones
	return redirect(url_for('mejor_valorados2_ya_jugados'))


@app.route('/mejor_valorados2_ya_jugados', methods=['GET', 'POST'])
@login_required
def mejor_valorados2_ya_jugados():
	txt = control_lenguaje(request.args, 'mejor_valorados_ya_jugado')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mejor_valor_todos']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'mejor_valorados2_ya_jugados')
	return render_template('index.html', txt=txt, title='Mejor Valorados', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)


@app.route('/mejor_valorados_no_jugado', methods=['GET', 'POST'])
@login_required
def mejor_valorados_no_jugado():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_mejor_valorados(origen_datos, id_user, 0)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mejor_valorados']+txt['pg_ind_tit_selec_no_jugados'], 'select':select_valor}]
	selec = selecciones
	return redirect(url_for('mejor_valorados2_no_jugado'))


@app.route('/mejor_valorados2_no_jugado', methods=['GET', 'POST'])
@login_required
def mejor_valorados2_no_jugado():
	txt = control_lenguaje(request.args, 'mejor_valorados_no_jugado')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mejor_valor_todos']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'mejor_valorados2_no_jugado')
	return render_template('index.html', txt=txt, title='Mejor Valorados', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_vistos_archive_todos', methods=['GET', 'POST'])
@login_required
def mas_vistos_archive_todos():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'visitas', 3)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_vistos']+txt['pg_ind_tit_selec_todos_juegos'], 'select':select_valor}]
	selec = selecciones
	return redirect(url_for('mas_vistos_archive2_todos'))


@app.route('/mas_vistos_archive2_todos', methods=['GET', 'POST'])
@login_required
def mas_vistos_archive2_todos():
	txt = control_lenguaje(request.args, 'mas_vistos_archive_todos')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mas_vistos_archive']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'mas_vistos_archive2_todos')
	return render_template('index.html', txt=txt, title='Mas Vistos', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)


@app.route('/mas_vistos_archive_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_vistos_archive_ya_jugado():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'visitas', 1)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_vistos']+txt['pg_ind_tit_selec_ya_jugados'], 'select':select_valor}]
	selec = selecciones
	return redirect(url_for('mas_vistos_archive2_ya_jugado'))


@app.route('/mas_vistos_archive2_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_vistos_archive2_ya_jugado():
	txt = control_lenguaje(request.args, 'mas_stars_archive_ya_jugado')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mas_vistos_archive']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'mas_vistos_archive2_ya_jugado')
	return render_template('index.html', txt=txt, title='Mas Vistos', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_vistos_archive_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_vistos_archive_no_jugado():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'visitas', 0)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_vistos']+txt['pg_ind_tit_selec_no_jugados'], 'select':select_valor}]
	selec = selecciones
	return redirect(url_for('mas_vistos_archive2_no_jugado'))


@app.route('/mas_vistos_archive2_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_vistos_archive2_no_jugado():
	txt = control_lenguaje(request.args, 'mas_vistos_archive2_no_jugado')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mas_vistos_archive']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'mas_vistos_archive2_no_jugado')
	return render_template('index.html', txt=txt, title='Mas Vistos', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_stars_archive', methods=['GET', 'POST'])
@login_required
def mas_stars_archive_todos():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'favoritos', 3)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_stars']+txt['pg_ind_tit_selec_todos_juegos'], 'select':select_valor}]
	selec = selecciones
	return redirect(url_for('mas_stars_archive2_todos'))


@app.route('/mas_stars_archive2_todos', methods=['GET', 'POST'])
@login_required
def mas_stars_archive2_todos():
	txt = control_lenguaje(request.args, 'mas_stars_archive_todos')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mas_stars_archive']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'mas_stars_archive2_todos')
	return render_template('index.html', txt=txt, title='Mas Stars', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_stars_archive_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_stars_archive_ya_jugado():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'favoritos', 1)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_stars']+txt['pg_ind_tit_selec_ya_jugados'], 'select':select_valor}]
	selec = selecciones
	return redirect(url_for('mas_stars_archive2_ya_jugado'))


@app.route('/mas_stars_archive2_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_stars_archive2_ya_jugado():
	txt = control_lenguaje(request.args, 'mas_stars_archive_ya_jugado')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mas_stars_archive']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'mas_stars_archive2_ya_jugado')
	return render_template('index.html', txt=txt, title='Mas Stars', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_stars_archive_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_stars_archive_no_jugado():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'favoritos', 0)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_stars']+txt['pg_ind_tit_selec_no_jugados'], 'select':select_valor}]
	selec = selecciones
	return redirect(url_for('mas_stars_archive2_no_jugado'))


@app.route('/mas_stars_archive2_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_stars_archive2_no_jugado():
	txt = control_lenguaje(request.args, 'mas_stars_archive_no_jugado')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mas_stars_archive']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'mas_stars_archive2_no_jugado')
	return render_template('index.html', txt=txt, title='Mas Stars', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)


@app.route('/mas_comments_archive_todos', methods=['GET', 'POST'])
@login_required
def mas_comments_archive_todos():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'comentarios', 3)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_comments']+txt['pg_ind_tit_selec_todos_juegos'], 'select':select_valor}]
	selec = selecciones
	return redirect(url_for('mas_comments_archive2_todos'))


@app.route('/mas_comments_archive2_todos', methods=['GET', 'POST'])
@login_required
def mas_comments_archive2_todos():
	txt = control_lenguaje(request.args, 'mas_comments_archive_todos')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mas_comments_archive']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'mas_comments_archive2_todos')
	return render_template('index.html', txt=txt, title='Mas Comments', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)


@app.route('/mas_comments_archive_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_comments_archive_ya_jugado():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'comentarios', 1)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_comments']+txt['pg_ind_tit_selec_ya_jugados'], 'select':select_valor}]
	selec = selecciones
	return redirect(url_for('mas_comments_archive2_ya_jugado'))


@app.route('/mas_comments_archive2_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_comments_archive2_ya_jugado():
	txt = control_lenguaje(request.args, 'mas_comments_archive_ya_jugado')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mas_comments_archive']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'mas_comments_archive2_ya_jugado')
	return render_template('index.html', txt=txt, title='Mas Comments', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_comments_archive_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_comments_archive_no_jugado():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'comentarios', 0)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_comments']+txt['pg_ind_tit_selec_no_jugados'], 'select':select_valor}]
	selec = selecciones
	return redirect(url_for('mas_comments_archive2_no_jugado'))


@app.route('/mas_comments_archive2_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_comments_archive2_no_jugado():
	txt = control_lenguaje(request.args, 'mas_comments_archive_no_jugado')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_mas_comments_archive']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'mas_comments_archive2_no_jugado')
	return render_template('index.html', txt=txt, title='Mas Comments', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/busqueda', methods=['GET', 'POST'])
@login_required
def busqueda():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1
	palabra_busq = request.args.get('q')
	text_filtro = txt['pg_ind_tit_selec_busqueda'] + ':  '+ palabra_busq
	select_busq = select_busqueda(origen_datos, id_user, palabra_busq)
	selecciones =[{'filtro': text_filtro, 'select':select_busq}]
	selec = selecciones
	return redirect(url_for('busqueda2'))


@app.route('/busqueda2', methods=['GET', 'POST'])
@login_required
def busqueda2():
	txt = control_lenguaje(request.args, 'busqueda')
	jg_ifrm = control_parametros(request.args)
	texto=txt['pg_ind_text_busqueda']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec,'busqueda2')

	return render_template('index.html', txt=txt, title='Busqueda', selecciones=selecciones, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag=page, total_pag=total_pag, jg_ifrm=jg_ifrm)


@app.route('/busqueda_avanzada', methods=['GET', 'POST'])
@login_required
def busqueda_avanzada():
	global selec
	txt = control_lenguaje(request.args)
	id_user = current_user.id - 1

	if request.args.get('vist_min') != None:
		select_busq_avanz = select_busqueda_avanz(origen_datos, id_user, request.args);
		selecciones =[{'filtro': txt['pg_ind_tit_selec_busqueda'], 'select':select_busq_avanz}]
		selec = selecciones
		return redirect(url_for('busqueda2'))
	else:
		limites_busq = calcula_limites_busq(origen_datos, id_user);
		return render_template('busqueda_avanzada.html', txt=txt, title='Busqueda', limites_busq=limites_busq)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	txt = control_lenguaje(request.args)
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		avatar = form.avatar.data

		if avatar is None:
			avatar = 'img12'
		else:
			avatar = 'img'+str(avatar)

		user = User(username=form.username.data, email=form.email.data, avatar=avatar)
		user.set_password(form.password.data)

		# Actuliza las tablas e Insercción en BD
		actualiza_filtros()
		db.session.add(user)
		db.session.commit()

		flash(txt['pg_reg_registro_ok'])
		return redirect(url_for('login'))
	return render_template('register.html', txt=txt, title='Register', form=form)


def control_parametros(param):
	global selec
	jg_ifrm = None
	if param.get('juego') != None:
		juego = int(param.get('juego'))
		user = int(param.get('user'))
		valor = int(param.get('valor'))
		actualiza_yr(juego, user, valor)
		if param.get('jg_ifrm') != "":
			jg_ifrm = int(param.get('jg_ifrm'))

		selec = actualiza_selec(juego, valor, selec)

	return jg_ifrm


def control_lenguaje(param, origen=None):
	global selec
	if not 'lenguaje' in session:
		session['lenguaje'] = 'es'

	if param.get('leng_cambio') != None:
		session['lenguaje'] = param.get('leng_cambio')

		txt = carga_dicc_lenguaje(session['lenguaje'])
		if origen == 'index':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_modelos']
			selec[1]['filtro'] = txt['pg_ind_tit_selec_usuarios']
			selec[2]['filtro'] = txt['pg_ind_tit_selec_productos']
		elif origen == 'favoritos':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_favoritos']
		elif origen == 'mas_jugados_todos':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mas_jugados'] + txt['pg_ind_tit_selec_todos_juegos']
		elif origen == 'mas_jugados_ya_jugado':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mas_jugados'] + txt['pg_ind_tit_selec_ya_jugados']
		elif origen == 'mas_jugado_no_jugado':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mas_jugados'] + txt['pg_ind_tit_selec_no_jugados']
		elif origen == 'mejor_valorados_todos':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mejor_valorados'] + txt['pg_ind_tit_selec_todos_juegos']
		elif origen == 'mejor_valorados_ya_jugado':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mejor_valorados'] + txt['pg_ind_tit_selec_ya_jugados']
		elif origen == 'mejor_valorados_no_jugado':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mejor_valorados'] + txt['pg_ind_tit_selec_no_jugados']
		elif origen == 'mas_vistos_archive_todos':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mas_vistos'] + txt['pg_ind_tit_selec_todos_juegos']
		elif origen == 'mas_vistos_archive_ya_jugado':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mas_vistos'] + txt['pg_ind_tit_selec_ya_jugados']
		elif origen == 'mas_vistos_archive_no_jugado':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mas_vistos'] + txt['pg_ind_tit_selec_no_jugados']
		elif origen == 'mas_stars_archive_todos':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mas_stars'] + txt['pg_ind_tit_selec_todos_juegos']
		elif origen == 'mas_stars_archive_ya_jugado':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mas_stars'] + txt['pg_ind_tit_selec_ya_jugados']
		elif origen == 'mas_stars_archive_no_jugado':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mas_stars'] + txt['pg_ind_tit_selec_no_jugados']
		elif origen == 'mas_comments_archive_todos':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mas_comments'] + txt['pg_ind_tit_selec_todos_juegos']
		elif origen == 'mas_comments_archive_ya_jugado':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mas_comments'] + txt['pg_ind_tit_selec_ya_jugados']
		elif origen == 'mas_comments_archive_no_jugado':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_mas_comments'] + txt['pg_ind_tit_selec_no_jugados']
		elif origen == 'busqueda':
			selec[0]['filtro'] = txt['pg_ind_tit_selec_busqueda']


	return carga_dicc_lenguaje(session['lenguaje'])


def calc_paginacion(page, selec, origen):
	inc_selec = (page-1)*app.config['SEL_POR_PAG']
	fin_selec = page*app.config['SEL_POR_PAG']
	selecciones = copy.deepcopy(selec)
	selecciones[0]['select'] = selec[0]['select'][inc_selec: fin_selec]

	if len(selec[0]['select']) % app.config['SEL_POR_PAG'] == 0:
		total_pag = len(selec[0]['select']) // app.config['SEL_POR_PAG']
	else:
		total_pag = len(selec[0]['select']) // app.config['SEL_POR_PAG'] + 1

	if page > 1:
		pag_ante = page - 1
	else:
		pag_ante = page

	if page < total_pag:
		pag_post = page+1
	else:
		pag_post = page

	next_url = url_for(origen, page=pag_post)
	prev_url = url_for(origen, page=pag_ante)
	inic_url = url_for(origen, page=1)
	fin_url = url_for(origen, page=total_pag)

	return next_url, prev_url, inic_url, fin_url, total_pag, selecciones