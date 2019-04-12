from app.models import User

users = User.query.all()

for u in users:
    print (u.id, u.username, u.email, u.avatar, u.password_hash)

print('...................')
users = User.query.filter_by(username='user0')
for u in users:
    print (u.id, u.username, u.email, u.avatar, u.password_hash)

print('...................')
users = User.query.filter_by(id=1)
for u in users:
    print (u.id, u.username, u.email, u.avatar, u.password_hash)
