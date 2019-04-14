from app import db
from app.models import User

app = app(config=Config)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
