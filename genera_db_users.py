from app import db
from app.models import User
import numpy as np

for i in range(0,1000):
	name = 'user'+str(i)
	mail = name+'@retrogaming.com'
	avat = 'img'+str(np.random.randint(1,31))
	pssw = 'parola'

	user = User(username=name, email=mail, avatar=avat)
	user.set_password(pssw)
	db.session.add(user)

db.session.commit()