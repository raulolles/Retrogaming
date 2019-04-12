from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from flask import request


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')


class RegistrationForm(FlaskForm):
	username = StringField('Usuario', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	avatar = StringField('Avatar', default=13)
	password = PasswordField('Contraseña', validators=[DataRequired()])
	password2 = PasswordField('Repetir Contraseña', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Registrar')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Por favor, use un nombre de usurio diferente')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Por favor, use un email diferente')


class SearchForm(FlaskForm):
	q = StringField(('Search'), validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		if 'formdata' not in kwargs:
			kwargs['formdata'] = request.args
		if 'csrf_enabled' not in kwargs:
			kwargs['csrf_enabled'] = False
			super(SearchForm, self).__init__(*args, **kwargs)