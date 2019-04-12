# -*- coding: utf-8 -*-
"""
Crea y suministra los diccionarios con las palabras a incluir en la web
para los diferentes lenguajes
"""

def crea_dicc_lenguajes():

	diccionario_todos_lenguajes = {'es' :
			{'sesion_leng':'es',

			'menu_inicio':'Inicio',
			'menu_favoritos':'Favoritos',
			'menu_en_retrogaming':'en Retrogaming',
			'menu_en_archive':'en Archive.org',
			'menu_todos_juegos':'Todos los Juegos',
			'menu_ya_jugados':'Ya has jugado',
			'menu_no_has_jugado':'No has jugado',
			'menu_mas_vistos':'Mas Vistos',
			'menu_mas_stars':'Mas Stars',
			'menu_mas_comments':'Mas Comments',
			'menu_mas_jugados':'Mas Jugados',
			'menu_mejor_valorados':'Mejor Valorados',
			'menu_busqueda':'Buscar',
			'menu_busq_avan':'Búsqueda',
			'menu_login':'Inicio Sesión',
			'menu_logout':'Salir',

			'saludo':'Hola!',

			'pg_login_iniciar_sesion':'Iniciar Sesion',
			'pg_login_usuario':'Nombre Usuario',
			'pg_login_contras':'Contraseña',
			'pg_login_recordarme':'Recordarme',
			'pg_login_iniciar':'Iniciar Sesión',
			'pg_login_nuevo_user':'Nuevo Usuario?',
			'pg_login_click_reg':'Click para Registrarse!',
			'pg_login_error1':'[ Valor Requerido ]',
			'pg_login_men_error_base':'Por favor, identifíquese para acceder a esta página.',
			'pg_login_error_ident':'Nombre de usuario o contraseña erronea',

			'pg_reg_registro':'Registro',
			'pg_reg_usuario':'Usuario',
			'pg_reg_email':'Email',
			'pg_reg_contrasena':'Contraseña',
			'pg_reg_repe_contr':'Repetir Contraseña',
			'pg_reg_registrar':'Registrar',
			'pg_reg_registro_ok':'Felicidades, ya eres un usuario registrado!',
			'pg_reg_error_user':'[ Use un nombre de usuario diferente]',
			'pg_reg_error_email':'[ Email no valido ]',
			'pg_reg_error_contrasena':'[ Contraseña no valida ]',
			'pg_reg_error_contrasena_rep':'[ El valor debe coincidir con la contraseña ] ',

			'pg_ind_text':'...pensamos que te gustará',
			'pg_ind_tit_selec_modelos':'Modelos',
			'pg_ind_tit_selec_usuarios':'Usuarios',
			'pg_ind_tit_selec_productos':'Productos',

			'pg_ind_text_favoritos':'...tus juegos favoritos',
			'pg_ind_tit_selec_favoritos':'Favoritos',

			'pg_ind_text_mas_jugados_todos':'...los más jugados por todos los usuarios',
			'pg_ind_text_mejor_valor_todos':'...los mejor valorados por todos los usuarios',


			'pg_ind_tit_selec_mas_jugados':'Más Jugados',
			'pg_ind_tit_selec_mejor_valorados':'Mejor Valorados',

			'pg_ind_tit_selec_todos_juegos':' : Todos los juegos',
			'pg_ind_tit_selec_ya_jugados':' : Jugados antes por ti',
			'pg_ind_tit_selec_no_jugados':' : Aún no has jugado',

			'pg_ind_text_mas_vistos_archive':'...los más vistos en archive.org',
			'pg_ind_text_mas_stars_archive':'...con más stars en archive.org',
			'pg_ind_text_mas_comments_archive':'...con más comentarios en archive.org',

			'pg_ind_tit_selec_mas_vistos':'Más Vistos en archive.org',
			'pg_ind_tit_selec_mas_stars':'Con más stars en archive.org',
			'pg_ind_tit_selec_mas_comments':'Con más comentarios en archive.org',

			'pg_ind_text_busqueda':'...los resultados de tu búsqueda',
			'pg_ind_tit_selec_busqueda':'Busqueda',

			'pg_ind_no_resultados':'Uppps!!!    Parece que no hay resultados para esta búsqueda',

			'pg_bsq_avan_en_archive':'en Archive.org',
			'pg_bsq_avan_en_retrogaming':'en Retrogaming',
			'pg_bsq_avan_vistas':'Vistas',
			'pg_bsq_avan_stars':'Stars',
			'pg_bsq_avan_comment':'Comentarios',
			'pg_bsq_avan_valor':'Tu Valoracion',
			'pg_bsq_avan_media':'Media',
			'pg_bsq_avan_jugadores':'Jugadores',
			'pg_bsq_avan_de_los_jugados':'¿De los que has jugado antes?',
			'pg_bsq_avan_jgd_todos':'Todos los Juegos',
			'pg_bsq_avan_jgd_si':'Ya Jugados',
			'pg_bsq_avan_jgd_no':'No Jugados',
			'pg_bsq_avan_por_palabra':'Busqueda por palabra',
			'pg_bsq_avan_enviar':'Enviar',

			'tira_juego_juega':'juega en su web',
			'tira_juego_tu_valoracion':'tu valoración',

			'iframe_cerrar':'Cerrar Juego',

			'paginacion_pagina':'página',
			'paginacion_de':'de',
			'paginacion_inicio':'inicio',
			'paginacion_final':'final',
			'paginacion_anterior':'anterior',
			'paginacion_siguient':'siguiente',

			'introd_1':'Retrogaming Recommender',
			'introd_2':'Commodore 64',
			'introd_3':'Podrás ver más de 10.000 juegos de la mítica commodore 64.',
			'introd_4':'Dispondrás de predicciones de los juegos que mejor se adaptan a tu trayectoria de juego.',
			'introd_5':'Puntua cada juego según tu preferencias. Lista y busca juegos según han sido puntuados en Retrogaming o en Archive.org',
			'introd_6':'La lista de juegos está basada en los que se encuetran disponibles en web archive.org'
			},
		'en' :
			{'sesion_leng':'en',

			'menu_inicio':'Home',
			'menu_favoritos':'Favorites',
			'menu_en_retrogaming':'in Retrogaming',
			'menu_en_archive':'in Archive.org',
			'menu_todos_juegos':'All Games',
			'menu_ya_jugados':'Already Played',
			'menu_no_has_jugado':'You have not played',
			'menu_mas_vistos':'Most Seen',
			'menu_mas_stars':'Most Stars',
			'menu_mas_comments':'Most Comments',
			'menu_mas_jugados':'Most Played',
			'menu_mejor_valorados':'Top Rated',
			'menu_busqueda':'Search',
			'menu_busq_avan':'Search',
			'menu_login':'Login',
			'menu_logout':'Logout',

			'saludo':'Hi!',

			'pg_login_iniciar_sesion':'Login',
			'pg_login_usuario':'User',
			'pg_login_contras':'Password',
			'pg_login_recordarme':'Remember me',
			'pg_login_iniciar':'Login',
			'pg_login_nuevo_user':'New User?',
			'pg_login_click_reg':'Click for Register!',
			'pg_login_error1':'[ This field is required ]',
			'pg_login_men_error_base':'Please log in to access this page.',
			'pg_login_error_ident':'Invalid username or password',

			'pg_reg_registro':'Register',
			'pg_reg_usuario':'User',
			'pg_reg_email':'Email',
			'pg_reg_contrasena':'Password',
			'pg_reg_repe_contr':'Repeat Password',
			'pg_reg_registrar':'Register',
			'pg_reg_registro_ok':'Congratulations, you are already a registered user!',
			'pg_reg_error_user':'[ Use a different username ]',
			'pg_reg_error_email':'[ Invalid email address ]',
			'pg_reg_error_contrasena':'[ Invalid password ]',
			'pg_reg_error_contrasena_rep':'[ Field must be equal to password ] ',

			'pg_ind_text':'...we think you\'ll like',
			'pg_ind_tit_selec_modelos':'Models',
			'pg_ind_tit_selec_usuarios':'Users',
			'pg_ind_tit_selec_productos':'Products',
			'pg_ind_text_favoritos':'...your favorite games',
			'pg_ind_tit_selec_favoritos':'Favorites',

			'pg_ind_text_mas_jugados_todos':'...the most played by all users',
			'pg_ind_text_mejor_valor_todos':'...the best rated by all users',
			'pg_ind_tit_selec_mas_jugados':'Most Played',
			'pg_ind_tit_selec_mejor_valorados':'Top Rated',

			'pg_ind_tit_selec_todos_juegos':' : All the games',
			'pg_ind_tit_selec_ya_jugados':' : Played before by you',
			'pg_ind_tit_selec_no_jugados':' : You have not played yet',

			'pg_ind_text_mas_vistos_archive':'...the most viewed in archive.org',
			'pg_ind_text_mas_stars_archive':'...with more stars in archive.org',
			'pg_ind_text_mas_comments_archive':'...with more comments on archive.org',
			'pg_ind_tit_selec_mas_vistos':'Most Viewed on archive.org',
			'pg_ind_tit_selec_mas_stars':'With more stars on archive.org',
			'pg_ind_tit_selec_mas_comments':'With more comments on archive.org',

			'pg_ind_text_busqueda':'...the results of your search',
			'pg_ind_tit_selec_busqueda':'Search',

			'pg_ind_no_resultados':'Uppps!!!    there seems to be no results for this search',

			'pg_bsq_avan_en_archive':'in Archive.org',
			'pg_bsq_avan_en_retrogaming':'in Retrogaming',
			'pg_bsq_avan_vistas':'Views',
			'pg_bsq_avan_stars':'Stars',
			'pg_bsq_avan_comment':'Comments',
			'pg_bsq_avan_valor':'Your Rate',
			'pg_bsq_avan_media':'Mean',
			'pg_bsq_avan_jugadores':'Players',
			'pg_bsq_avan_de_los_jugados':'¿Have you played before?',
			'pg_bsq_avan_jgd_todos':'All the Games',
			'pg_bsq_avan_jgd_si':'Played',
			'pg_bsq_avan_jgd_no':'Not Played',
			'pg_bsq_avan_por_palabra':'Search by word',
			'pg_bsq_avan_enviar':'Send',

			'tira_juego_juega':'play on your website',
			'tira_juego_tu_valoracion':'your valuation',

			'iframe_cerrar':'Close Game',

			'paginacion_pagina':'page',
			'paginacion_de':'of',
			'paginacion_inicio':'star',
			'paginacion_final':'end',
			'paginacion_anterior':'previous',
			'paginacion_siguient':'next',

			'introd_1':'Retrogaming Recommender',
			'introd_2':'Commodore 64',
			'introd_3':'You can see more than 10,000 games of the legendary commodore 64',
			'introd_4':'You will have predictions of the games that best suit your gaming trajectory',
			'introd_5':'Score each game according to your preferences. List and search for games as they have been rated in Retrogaming or in Archive.org',
			'introd_6':'The list of games is based on the ones available on web archive.org'
			},
		'fr' :
			{'sesion_leng':'fr',

			'menu_inicio':'Accueil',
			'menu_favoritos':'Favori',
			'menu_en_retrogaming':'sur Retrogaming',
			'menu_en_archive':'sur Archive.org',
			'menu_todos_juegos':'Tous les jeux',
			'menu_ya_jugados':'Vous avez déjà joué',
			'menu_no_has_jugado':'Vous n\'avez pas joué',
			'menu_mas_vistos':'Les plus vues',
			'menu_mas_stars':'Plus Stars',
			'menu_mas_comments':'Plus Comments',
			'menu_mas_jugados':'Plus Joué',
			'menu_mejor_valorados':'Mieux Notés',
			'menu_busqueda':'Recherche',
			'menu_busq_avan':'Recherche',
			'menu_login':'Login',
			'menu_logout':'Logout',

			'saludo':'Salut!',

			'pg_login_iniciar_sesion':'Commencer Session',
			'pg_login_usuario':'Nom Utilisateur',
			'pg_login_contras':'Mot de Passe',
			'pg_login_recordarme':'Rappeler',
			'pg_login_iniciar':'Commencer Session',
			'pg_login_nuevo_user':'Nouvel Utilisateur?',
			'pg_login_click_reg':'Cliquez pour vous Inscrire!',
			'pg_login_error1':'[ Valeur Obligatoire ]',
			'pg_login_men_error_base':'S\'il vous plait, Veuillez vous connecter pour accéder à cette page.',
			'pg_login_error_ident':'Nom d\'utilisateur ou mot de passe incorrect',

			'pg_reg_registro':'Inscription',
			'pg_reg_usuario':'Utilisateur',
			'pg_reg_email':'Email',
			'pg_reg_contrasena':'Mot de Passe',
			'pg_reg_repe_contr':'Répéter Mot de Passe',
			'pg_reg_registrar':'Inscription',
			'pg_reg_registro_ok':'Félicitations, vous êtes déjà un utilisateur enregistré!',
			'pg_reg_error_user':'[ Utilisez un nom d\'utilisateur différent ]',
			'pg_reg_error_email':'[ Email non valide ]',
			'pg_reg_error_contrasena':'[ Mot de passe non valide ]',
			'pg_reg_error_contrasena_rep':'[ La valeur doit correspondre au mot de passe ] ',

			'pg_ind_text':'...nous pensons que cela vous plaira',
			'pg_ind_tit_selec_modelos':'Modèles',
			'pg_ind_tit_selec_usuarios':'Utilisateurs',
			'pg_ind_tit_selec_productos':'Produits',

			'pg_ind_text_favoritos':'...vos jeux préférés',
			'pg_ind_tit_selec_favoritos':'Favoris',

			'pg_ind_text_mas_jugados_todos':'...le plus joué par tous les utilisateurs',
			'pg_ind_text_mejor_valor_todos':'...le mieux noté par tous les utilisateurs',

			'pg_ind_tit_selec_mas_jugados':'Plus Joué',
			'pg_ind_tit_selec_mejor_valorados':'Mieux Notés',

			'pg_ind_tit_selec_todos_juegos':' : Tous les jeux',
			'pg_ind_tit_selec_ya_jugados':' : Joué devant vous',
			'pg_ind_tit_selec_no_jugados':' : Vous n\'avez pas encore joué',

			'pg_ind_text_mas_vistos_archive':'...les plus vues sur archive.org',
			'pg_ind_text_mas_stars_archive':'...avec plus d\'étoiles sur archive.org',
			'pg_ind_text_mas_comments_archive':'...avec plus de commentaires sur archive.org',

			'pg_ind_tit_selec_mas_vistos':'Plus vu archive.org',
			'pg_ind_tit_selec_mas_stars':'Avec plus stars sur archive.org',
			'pg_ind_tit_selec_mas_comments':'Avec plus comentarios sur archive.org',

			'pg_ind_text_busqueda':'...les résultats de votre recherche',
			'pg_ind_tit_selec_busqueda':'Recherche',

			'pg_ind_no_resultados':'Uppps!!!    Il semble n\'y avoir aucun résultat pour cette recherche',

			'pg_bsq_avan_en_archive':'sur Archive.org',
			'pg_bsq_avan_en_retrogaming':'sur Retrogaming',
			'pg_bsq_avan_vistas':'Vues',
			'pg_bsq_avan_stars':'Étoiles',
			'pg_bsq_avan_comment':'Commentarires',
			'pg_bsq_avan_valor':'Évaluation',
			'pg_bsq_avan_media':'Moyenne',
			'pg_bsq_avan_jugadores':'Joueurs',
			'pg_bsq_avan_de_los_jugados':'De ceux que vous avez déjà joué?',
			'pg_bsq_avan_jgd_todos':'Tous les Jeux',
			'pg_bsq_avan_jgd_si':'Déjà Joué',
			'pg_bsq_avan_jgd_no':'Pas Joués',
			'pg_bsq_avan_por_palabra':'Recherche par mot',
			'pg_bsq_avan_enviar':'Envoyer',

			'tira_juego_juega':'jouer sur le web',
			'tira_juego_tu_valoracion':'votre évaluation',

			'iframe_cerrar':'Fermer Jeu',

			'paginacion_pagina':'page',
			'paginacion_de':'de',
			'paginacion_inicio':'début',
			'paginacion_final':'final',
			'paginacion_anterior':'précédent',
			'paginacion_siguient':'suivant',

			'introd_1':'Retrogaming Recommender',
			'introd_2':'Commodore 64',
			'introd_3':'Vous pouvez voir plus de 10 000 jeux du légendaire commodore 64',
			'introd_4':'Vous aurez des prédictions sur les jeux qui conviennent le mieux à votre trajectoire de jeu.',
			'introd_5':'Marquez chaque jeu en fonction de vos préférences. Listez et recherchez les jeux tels qu\'ils ont été évalués dans Retrogaming ou sur Archive.org',
			'introd_6':'La liste des jeux est basée sur ceux disponibles sur web archive.org'
			},
		'rm' :
			{'sesion_leng':'rm',

			'menu_inicio':'început',
			'menu_favoritos':'Favorite',
			'menu_en_retrogaming':'în Retrogaming',
			'menu_en_archive':'în Archive.org',
			'menu_todos_juegos':'Toate Jocurile',
			'menu_ya_jugados':'Jucat deja',
			'menu_no_has_jugado':'Nu ai jucat',
			'menu_mas_vistos':'Mai Vizionate',
			'menu_mas_stars':'Mai Multe Stars',
			'menu_mas_comments':'Mai Multe Comments',
			'menu_mas_jugados':'Mai Jucate',
			'menu_mejor_valorados':'Mai Votate',
			'menu_busqueda':'Căuta',
			'menu_busq_avan':'Căutare',
			'menu_login':'Login',
			'menu_logout':'Logout',

			'saludo':'Salut!',

			'pg_login_iniciar_sesion':'Autentificare',
			'pg_login_usuario':'Nume de utilizator',
			'pg_login_contras':'Parola',
			'pg_login_recordarme':'Ține-mă minte',
			'pg_login_iniciar':'Autentificare',
			'pg_login_nuevo_user':'Utilizator nou?',
			'pg_login_click_reg':'Clickezi pentru a vă înregistra!',
			'pg_login_error1':'[ Datele necesare ]',
			'pg_login_men_error_base':'Vă rugăm să vă autentificați pentru a accesa această pagină.',
			'pg_login_error_ident':'Nume de utilizator sau parolă incorecte',

			'pg_reg_registro':'Înregistrare',
			'pg_reg_usuario':'Utilizator',
			'pg_reg_email':'Email',
			'pg_reg_contrasena':'Parola',
			'pg_reg_repe_contr':'Repetați parola',
			'pg_reg_registrar':'Înregistrare',
			'pg_reg_registro_ok':'Felicitări, sunteți deja un utilizator înregistrat!',
			'pg_reg_error_user':'[ Utilizați un alt nume de utilizator ]',
			'pg_reg_error_email':'[ Email nu valid ]',
			'pg_reg_error_contrasena':'[ Parolă nu validă ]',
			'pg_reg_error_contrasena_rep':'[ Valoarea trebuie să corespundă parolei ] ',

			'pg_ind_text':'...credem că o-să vă placă',
			'pg_ind_tit_selec_modelos':'Models',
			'pg_ind_tit_selec_usuarios':'Utilizators',
			'pg_ind_tit_selec_productos':'Produse',

			'pg_ind_text_favoritos':'...jocurile tale preferate',
			'pg_ind_tit_selec_favoritos':'Favorite',

			'pg_ind_text_mas_jugados_todos':'...cele mai jucate de toți utilizatorii',
			'pg_ind_text_mejor_valor_todos':'...cels mai bine valorați de toți utilizatorii',


			'pg_ind_tit_selec_mas_jugados':'Cele Mai Jucate',
			'pg_ind_tit_selec_mejor_valorados':'Cele Mai votate',

			'pg_ind_tit_selec_todos_juegos':' : Toate jocurile',
			'pg_ind_tit_selec_ya_jugados':' : Jucate înainte de tine',
			'pg_ind_tit_selec_no_jugados':' : Nu ai jucat încă',

			'pg_ind_text_mas_vistos_archive':'...cele mai vizualizate în arhive.org',
			'pg_ind_text_mas_stars_archive':'...cu mai multe stele de pe archive.org',
			'pg_ind_text_mas_comments_archive':'...cu mai multe comentarii pe arhive.org',

			'pg_ind_tit_selec_mas_vistos':'Cele mai vizionate pe arhive.org',
			'pg_ind_tit_selec_mas_stars':'Cu mai multe stele de pe archive.org',
			'pg_ind_tit_selec_mas_comments':'Cu mai multe comentarii pe arhive.org',

			'pg_ind_text_busqueda':'...rezultatele căutării tale',
			'pg_ind_tit_selec_busqueda':'Căutare',

			'pg_ind_no_resultados':'Uppps!!!    Se pare că nu există rezultate pentru această căutare',

			'pg_bsq_avan_en_archive':'în Archive.org',
			'pg_bsq_avan_en_retrogaming':'în Retrogaming',
			'pg_bsq_avan_vistas':'Vizualizari',
			'pg_bsq_avan_stars':'Stele',
			'pg_bsq_avan_comment':'Comentarii',
			'pg_bsq_avan_valor':'Evaluarea ta',
			'pg_bsq_avan_media':'Medie',
			'pg_bsq_avan_jugadores':'Jucători',
			'pg_bsq_avan_de_los_jugados':'Dintre cele pe care le-ai jucat înainte?',
			'pg_bsq_avan_jgd_todos':'Toate Jocurile',
			'pg_bsq_avan_jgd_si':'Jucat Deja',
			'pg_bsq_avan_jgd_no':'Nu Jucate',
			'pg_bsq_avan_por_palabra':'Căutare după Cuvânt',
			'pg_bsq_avan_enviar':'Trimite',

			'tira_juego_juega':'juacă pe site-ul lor.',
			'tira_juego_tu_valoracion':'evaluarea ta',

			'iframe_cerrar':'Închide Jocul',

			'paginacion_pagina':'pagina',
			'paginacion_de':'de',
			'paginacion_inicio':'început',
			'paginacion_final':'sfârșit',
			'paginacion_anterior':'precedent',
			'paginacion_siguient':'următor',

			'introd_1':'Retrogaming Recommender',
			'introd_2':'Commodore 64',
			'introd_3':'Poți vedea mai mult de 10.000 de jocuri ale commodorei miticului 64',
			'introd_4':'Veți avea previziuni ale jocurilor care se potrivesc cel mai bine traiectoriei ta de jocuri',
			'introd_5':'Scorați fiecare joc în funcție de preferințele tale. Listați și căutați jocuri așa cum au fost evaluate în Retrogaming sau pe Archive.org',
			'introd_6':'Lista de jocuri se bazează pe cele disponibile pe site-ul archive.org'
			}
		}

	return diccionario_todos_lenguajes

def carga_dicc_lenguaje(lenguaje):
	dicc_total = crea_dicc_lenguajes()
	return dicc_total[lenguaje]