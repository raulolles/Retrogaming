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

origen_datos = "app/static/datos/"

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
# Si el usuario está logeado selecciona ofertas
def index():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_modelos, select_users, select_juegos = select_predicciones(origen_datos, id_user)
	selec_m = {'filtro': txt['pg_ind_tit_selec_modelos'], 'select':select_modelos}
	selec_u = {'filtro': txt['pg_ind_tit_selec_usuarios'], 'select':select_users}
	selec_j = {'filtro': txt['pg_ind_tit_selec_productos'], 'select':select_juegos}
	return redirect(url_for('index2', selec_m=selec_m, selec_u=selec_u, selec_j=selec_j))

@app.route('/index2', methods=['GET', 'POST'])
@login_required
# Si el usuario está logeado selecciona ofertas
def index2():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args,'index', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto = txt['pg_ind_text']
	return render_template('index.html', txt=txt, title='Home', selecciones=selec_global, selec_global=selec_global, texto_cab=texto, jg_ifrm=jg_ifrm)


@app.route('/login', methods=['GET', 'POST'])
def login():
	txt,selecciones = control_lenguaje(request.args)
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
# Si el usuario está logeado selecciona ofertas
def favoritos():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_fav = select_favoritos(origen_datos, id_user)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_favoritos'], 'select':select_fav}]
	return redirect(url_for('favoritos2', selec = selecciones))


@app.route('/favoritos2', methods=['GET', 'POST'])
@login_required
# Si el usuario está logeado selecciona ofertas
def favoritos2():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'favoritos', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto = txt['pg_ind_text_favoritos']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global, 'favoritos2')
	return render_template('index.html', txt=txt, title='Favoritos', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag=page, total_pag=total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_jugados_todos', methods=['GET', 'POST'])
@login_required
def mas_jugados_todos():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_mas_jug = select_mas_jugados(origen_datos, id_user,3)
	selecciones =[{'filtro': txt['pg_ind_tit_selec_mas_jugados']+txt['pg_ind_tit_selec_todos_juegos'], 'select':select_mas_jug}]
	return redirect(url_for('mas_jugados2_todos', 	selec = selecciones))


@app.route('/mas_jugados2_todos', methods=['GET', 'POST'])
@login_required
def mas_jugados2_todos():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mas_jugados_todos', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto= txt['pg_ind_text_mas_jugados_todos']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global, 'mas_jugados2_todos')
	return render_template('index.html', txt=txt, title='Mas Jugados', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag=page, total_pag=total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_jugados_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_jugados_ya_jugado():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_mas_jug = select_mas_jugados(origen_datos, id_user,1)
	selecciones =[{'filtro': txt['pg_ind_tit_selec_mas_jugados']+txt['pg_ind_tit_selec_ya_jugados'], 'select':select_mas_jug}]
	return redirect(url_for('mas_jugados2_ya_jugado', selec = selecciones))


@app.route('/mas_jugados2_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_jugados2_ya_jugado():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mas_jugados_ya_jugado', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mas_jugados_todos']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global, 'mas_jugados2_ya_jugado')
	return render_template('index.html', txt=txt, title='Mas Jugados', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag=page, total_pag=total_pag, jg_ifrm=jg_ifrm)


@app.route('/mas_jugados_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_jugados_no_jugado():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_mas_jug = select_mas_jugados(origen_datos, id_user,0)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_jugados']+txt['pg_ind_tit_selec_no_jugados'], 'select':select_mas_jug}]
	return redirect(url_for('mas_jugados2_no_jugado', selec = selecciones))


@app.route('/mas_jugados2_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_jugados2_no_jugado():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mas_jugados_no_jugado', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mas_jugados_todos']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global, 'mas_jugados2_no_jugado')
	return render_template('index.html', txt=txt, title='Mas Jugados', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag=page, total_pag=total_pag, jg_ifrm=jg_ifrm)



@app.route('/mejor_valorados_todos', methods=['GET', 'POST'])
@login_required
def mejor_valorados_todos():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_mejor_valorados(origen_datos, id_user, 3)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mejor_valorados']+txt['pg_ind_tit_selec_todos_juegos'], 'select':select_valor}]
	return redirect(url_for('mejor_valorados2_todos', selec = selecciones))


@app.route('/mejor_valorados2_todos', methods=['GET', 'POST'])
@login_required
def mejor_valorados2_todos():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mejor_valorados_todos', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mejor_valor_todos']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'mejor_valorados2_todos')
	return render_template('index.html', txt=txt, title='Mejor Valorados', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)


@app.route('/mejor_valorados_ya_jugado', methods=['GET', 'POST'])
@login_required
def mejor_valorados_ya_jugado():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_mejor_valorados(origen_datos, id_user, 1)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mejor_valorados']+txt['pg_ind_tit_selec_ya_jugados'], 'select':select_valor}]
	return redirect(url_for('mejor_valorados2_ya_jugados', selec = selecciones))


@app.route('/mejor_valorados2_ya_jugados', methods=['GET', 'POST'])
@login_required
def mejor_valorados2_ya_jugados():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mejor_valorados_ya_jugado', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mejor_valor_todos']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'mejor_valorados2_ya_jugados')
	return render_template('index.html', txt=txt, title='Mejor Valorados', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)


@app.route('/mejor_valorados_no_jugado', methods=['GET', 'POST'])
@login_required
def mejor_valorados_no_jugado():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_mejor_valorados(origen_datos, id_user, 0)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mejor_valorados']+txt['pg_ind_tit_selec_no_jugados'], 'select':select_valor}]
	return redirect(url_for('mejor_valorados2_no_jugado', selec = selecciones))


@app.route('/mejor_valorados2_no_jugado', methods=['GET', 'POST'])
@login_required
def mejor_valorados2_no_jugado():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mejor_valorados_no_jugado', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mejor_valor_todos']

	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'mejor_valorados2_no_jugado')
	return render_template('index.html', txt=txt, title='Mejor Valorados', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_vistos_archive_todos', methods=['GET', 'POST'])
@login_required
def mas_vistos_archive_todos():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'visitas', 3)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_vistos']+txt['pg_ind_tit_selec_todos_juegos'], 'select':select_valor}]
	return redirect(url_for('mas_vistos_archive2_todos', selec=selecciones))


@app.route('/mas_vistos_archive2_todos', methods=['GET', 'POST'])
@login_required
def mas_vistos_archive2_todos():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mas_vistos_archive_todos', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mas_vistos_archive']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'mas_vistos_archive2_todos')
	return render_template('index.html', txt=txt, title='Mas Vistos', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)


@app.route('/mas_vistos_archive_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_vistos_archive_ya_jugado():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'visitas', 1)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_vistos']+txt['pg_ind_tit_selec_ya_jugados'], 'select':select_valor}]
	return redirect(url_for('mas_vistos_archive2_ya_jugado', selec = selecciones))


@app.route('/mas_vistos_archive2_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_vistos_archive2_ya_jugado():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mas_stars_archive_ya_jugado', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mas_vistos_archive']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'mas_vistos_archive2_ya_jugado')
	return render_template('index.html', txt=txt, title='Mas Vistos', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_vistos_archive_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_vistos_archive_no_jugado():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'visitas', 0)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_vistos']+txt['pg_ind_tit_selec_no_jugados'], 'select':select_valor}]
	return redirect(url_for('mas_vistos_archive2_no_jugado', selec = selecciones))


@app.route('/mas_vistos_archive2_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_vistos_archive2_no_jugado():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mas_vistos_archive2_no_jugado', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mas_vistos_archive']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'mas_vistos_archive2_no_jugado')
	return render_template('index.html', txt=txt, title='Mas Vistos', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_stars_archive', methods=['GET', 'POST'])
@login_required
def mas_stars_archive_todos():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'favoritos', 3)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_stars']+txt['pg_ind_tit_selec_todos_juegos'], 'select':select_valor}]
	return redirect(url_for('mas_stars_archive2_todos', selec = selecciones))


@app.route('/mas_stars_archive2_todos', methods=['GET', 'POST'])
@login_required
def mas_stars_archive2_todos():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mas_stars_archive_todos', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mas_stars_archive']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'mas_stars_archive2_todos')
	return render_template('index.html', txt=txt, title='Mas Stars', selecciones=selecciones, selec_global=selec_global,  texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_stars_archive_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_stars_archive_ya_jugado():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'favoritos', 1)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_stars']+txt['pg_ind_tit_selec_ya_jugados'], 'select':select_valor}]
	return redirect(url_for('mas_stars_archive2_ya_jugado', selec = selecciones))


@app.route('/mas_stars_archive2_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_stars_archive2_ya_jugado():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mas_stars_archive_ya_jugado', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mas_stars_archive']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'mas_stars_archive2_ya_jugado')
	return render_template('index.html', txt=txt, title='Mas Stars', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_stars_archive_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_stars_archive_no_jugado():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'favoritos', 0)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_stars']+txt['pg_ind_tit_selec_no_jugados'], 'select':select_valor}]
	return redirect(url_for('mas_stars_archive2_no_jugado', selec = selecciones))


@app.route('/mas_stars_archive2_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_stars_archive2_no_jugado():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mas_stars_archive_no_jugado', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mas_stars_archive']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'mas_stars_archive2_no_jugado')
	return render_template('index.html', txt=txt, title='Mas Stars', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)


@app.route('/mas_comments_archive_todos', methods=['GET', 'POST'])
@login_required
def mas_comments_archive_todos():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'comentarios', 3)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_comments']+txt['pg_ind_tit_selec_todos_juegos'], 'select':select_valor}]
	return redirect(url_for('mas_comments_archive2_todos', selec = selecciones))


@app.route('/mas_comments_archive2_todos', methods=['GET', 'POST'])
@login_required
def mas_comments_archive2_todos():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mas_comments_archive_todos', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mas_comments_archive']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'mas_comments_archive2_todos')
	return render_template('index.html', txt=txt, title='Mas Comments', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)


@app.route('/mas_comments_archive_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_comments_archive_ya_jugado():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'comentarios', 1)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_comments']+txt['pg_ind_tit_selec_ya_jugados'], 'select':select_valor}]
	return redirect(url_for('mas_comments_archive2_ya_jugado', selec = selecciones))


@app.route('/mas_comments_archive2_ya_jugado', methods=['GET', 'POST'])
@login_required
def mas_comments_archive2_ya_jugado():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mas_comments_archive_ya_jugado', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mas_comments_archive']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'mas_comments_archive2_ya_jugado')
	return render_template('index.html', txt=txt, title='Mas Comments', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/mas_comments_archive_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_comments_archive_no_jugado():
	txt,selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	select_valor = select_archive(origen_datos, id_user, 'comentarios', 0)
	selecciones =[{'filtro':txt['pg_ind_tit_selec_mas_comments']+txt['pg_ind_tit_selec_no_jugados'], 'select':select_valor}]
	return redirect(url_for('mas_comments_archive2_no_jugado', selec = selecciones))


@app.route('/mas_comments_archive2_no_jugado', methods=['GET', 'POST'])
@login_required
def mas_comments_archive2_no_jugado():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'mas_comments_archive_no_jugado', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_mas_comments_archive']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'mas_comments_archive2_no_jugado')
	return render_template('index.html', txt=txt, title='Mas Comments', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag = page, total_pag = total_pag, jg_ifrm=jg_ifrm)



@app.route('/busqueda', methods=['GET', 'POST'])
@login_required
def busqueda():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1
	palabra_busq = request.args.get('q')
	text_filtro = txt['pg_ind_tit_selec_busqueda'] + ':  '+ palabra_busq
	select_busq = select_busqueda(origen_datos, id_user, palabra_busq)
	selecciones =[{'filtro': text_filtro, 'select':select_busq}]
	return redirect(url_for('busqueda2', selec = selecciones))


@app.route('/busqueda2', methods=['GET', 'POST'])
@login_required
def busqueda2():
	selec_global = control_selec(request.args)
	txt, selec_global = control_lenguaje(request.args, 'busqueda', selec_global)
	jg_ifrm, selec_global = control_parametros(request.args, selec_global)
	texto=txt['pg_ind_text_busqueda']
	page = request.args.get('page', 1, type=int)
	next_url, prev_url, inic_url, fin_url, total_pag, selecciones = calc_paginacion(page, selec_global,'busqueda2')
	return render_template('index.html', txt=txt, title='Busqueda', selecciones=selecciones, selec_global=selec_global, texto_cab=texto, next_url=next_url, prev_url=prev_url, inic_url=inic_url, fin_url=fin_url, pag=page, total_pag=total_pag, jg_ifrm=jg_ifrm)


@app.route('/busqueda_avanzada', methods=['GET', 'POST'])
@login_required
def busqueda_avanzada():
	txt, selecciones = control_lenguaje(request.args)
	id_user = current_user.id - 1

	if request.args.get('vist_min') != None:
		select_busq_avanz = select_busqueda_avanz(origen_datos, id_user, request.args);
		selecciones =[{'filtro': txt['pg_ind_tit_selec_busqueda'], 'select':select_busq_avanz}]
		return redirect(url_for('busqueda2', selec = selecciones))
	else:
		limites_busq = calcula_limites_busq(origen_datos, id_user);
		return render_template('busqueda_avanzada.html', txt=txt, title='Busqueda', limites_busq=limites_busq)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	txt,selecciones = control_lenguaje(request.args)
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

def control_selec(param):
	selec_global = list()
	if 'selec_global' in param:
		selec_global.append(eval(param['selec_global']))
	elif 'selec' in param:
		selec_global.append(eval(param['selec']))
	elif 'selec_m' in param:
		selec_global.append(eval(param['selec_m']))
		selec_global.append(eval(param['selec_u']))
		selec_global.append(eval(param['selec_j']))

	return selec_global	


def control_parametros(param, selec):
	jg_ifrm = None
	if param.get('juego') != None:
		juego = int(param.get('juego'))
		user = int(param.get('user'))
		valor = int(param.get('valor'))
		actualiza_yr(juego, user, valor)
		if param.get('jg_ifrm') != "":
			jg_ifrm = int(param.get('jg_ifrm'))

		selec = actualiza_selec(juego, valor, selec[0])

	return jg_ifrm, selec


def control_lenguaje(param, origen=None, selec=None):
	if not 'lenguaje' in session:
		session['lenguaje'] = 'es'

	if param.get('leng_cambio') != None:
		session['lenguaje'] = param.get('leng_cambio')

		txt = carga_dicc_lenguaje(session['lenguaje'])
		if selec !=  None:
			if origen == 'index':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_modelos']
				selec[0][1]['filtro'] = txt['pg_ind_tit_selec_usuarios']
				selec[0][2]['filtro'] = txt['pg_ind_tit_selec_productos']
			elif origen == 'favoritos':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_favoritos']
			elif origen == 'mas_jugados_todos':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mas_jugados'] + txt['pg_ind_tit_selec_todos_juegos']
			elif origen == 'mas_jugados_ya_jugado':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mas_jugados'] + txt['pg_ind_tit_selec_ya_jugados']
			elif origen == 'mas_jugado_no_jugado':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mas_jugados'] + txt['pg_ind_tit_selec_no_jugados']
			elif origen == 'mejor_valorados_todos':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mejor_valorados'] + txt['pg_ind_tit_selec_todos_juegos']
			elif origen == 'mejor_valorados_ya_jugado':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mejor_valorados'] + txt['pg_ind_tit_selec_ya_jugados']
			elif origen == 'mejor_valorados_no_jugado':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mejor_valorados'] + txt['pg_ind_tit_selec_no_jugados']
			elif origen == 'mas_vistos_archive_todos':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mas_vistos'] + txt['pg_ind_tit_selec_todos_juegos']
			elif origen == 'mas_vistos_archive_ya_jugado':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mas_vistos'] + txt['pg_ind_tit_selec_ya_jugados']
			elif origen == 'mas_vistos_archive_no_jugado':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mas_vistos'] + txt['pg_ind_tit_selec_no_jugados']
			elif origen == 'mas_stars_archive_todos':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mas_stars'] + txt['pg_ind_tit_selec_todos_juegos']
			elif origen == 'mas_stars_archive_ya_jugado':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mas_stars'] + txt['pg_ind_tit_selec_ya_jugados']
			elif origen == 'mas_stars_archive_no_jugado':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mas_stars'] + txt['pg_ind_tit_selec_no_jugados']
			elif origen == 'mas_comments_archive_todos':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mas_comments'] + txt['pg_ind_tit_selec_todos_juegos']
			elif origen == 'mas_comments_archive_ya_jugado':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mas_comments'] + txt['pg_ind_tit_selec_ya_jugados']
			elif origen == 'mas_comments_archive_no_jugado':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_mas_comments'] + txt['pg_ind_tit_selec_no_jugados']
			elif origen == 'busqueda':
				selec[0][0]['filtro'] = txt['pg_ind_tit_selec_busqueda']
			selec = selec[0]

	return carga_dicc_lenguaje(session['lenguaje']), selec


def calc_paginacion(page, selec_global, origen):
	inc_selec = (page-1)*app.config['SEL_POR_PAG']
	fin_selec = page*app.config['SEL_POR_PAG']
	selecciones = copy.deepcopy(selec_global)
	selecciones[0]['select'] = selec_global[0]['select'][inc_selec: fin_selec]

	if len(selec_global[0]['select']) % app.config['SEL_POR_PAG'] == 0:
		total_pag = len(selec_global[0]['select']) // app.config['SEL_POR_PAG']
	else:
		total_pag = len(selec_global[0]['select']) // app.config['SEL_POR_PAG'] + 1

	if page > 1:
		pag_ante = page - 1
	else:
		pag_ante = page

	if page < total_pag:
		pag_post = page+1
	else:
		pag_post = page

	next_url = url_for(origen, page=pag_post, selec_global=selec_global)
	prev_url = url_for(origen, page=pag_ante, selec_global=selec_global)
	inic_url = url_for(origen, page=1, selec_global=selec_global)
	fin_url = url_for(origen, page=total_pag, selec_global=selec_global)

	return next_url, prev_url, inic_url, fin_url, total_pag, selecciones