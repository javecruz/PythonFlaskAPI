from ficheros import db, Fichero
from run import app

with app.app_context():
    db.init_app(app)

data = Fichero.query.all()


