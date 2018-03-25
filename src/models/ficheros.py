from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/empresa'
db = SQLAlchemy(app)

class Fichero(db.Model):
    __tablename__ = 'ficheros'
    
    id = db.Column('id', db.Integer, primary_key = True)
    nombre = db.Column('nombre', db.VARCHAR)
    tipo = db.Column('tipo', db.VARCHAR)
    id_Vehiculo = db.Column('id_Vehiculo', db.Integer)
    
    def __init__(self, nombre, tipo, id_Vehiculo):
        self.nombre = nombre
        self.tipo = tipo
        self.id_Vehiculo = id_Vehiculo

'''
    from models import modelo, db
    ---INSERT---
    prueba = Fichero('test','factura')
    db.session.add(prueba)
    db.session.commit()
    prueba.id

    ---UPDATE---
    testie = Fichero.query.filter_by(id=1).first()
    testie.tipo = "newValue"
    testie.data = "updated!'
    db.session.commit()
    
    ---DELETE---
    test123 = Example.query.filter_by(id=18).first()
    db.session.delete(test123)
    db.session.commit()
'''

