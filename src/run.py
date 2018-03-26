from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/empresa'

db = SQLAlchemy(app)


#TOFIX, models move another directory, circular dependency between db <--> app

#model Ficheero
class Fichero(db.Model): 
    __tablename__ = 'ficheros'

    id = db.Column('id', db.Integer, primary_key = True)
    nombre = db.Column('nombre', db.VARCHAR)
    tipo = db.Column('tipo', db.VARCHAR)
    id_Vehiculo =  db.Column('id_Vehiculo', db.Integer)

    def __init__(self, nombre, tipo, id_Vehiculo):
        self.nombre = nombre
        self.tipo = tipo
        self.id_Vehiculo = id_Vehiculo

#model cliente
class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = db.Column('id', db.SMALLINT, primary_key=True)
    nombres = db.Column('nombres', db.VARCHAR)
    ciudad = db.Column('ciudad',db.VARCHAR)
    sexo = db.Column('sexo', db.CHAR)
    telefono = db.Column('telefono', db.VARCHAR)
    fecha_nacimiento = db.Column('fecha_nacimiento', db.DateTime)
    direccion = db.Column('direccion', db.VARCHAR)
    provincia = db.Column('provincia', db.VARCHAR)
    fechaAlta = db.Column('fechaAlta', db.DateTime)

    def __init__(self, nombres, ciudad, sexo, telefono, fecha_nacimiento, direccion, provincia):
        self.nombres = nombres
        self.ciudad = ciudad
        self.sexo = sexo
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.provincia = provincia

#model vehiculos
class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'

    id = db.Column('id', db.Integer, primary_key = True)
    matricula = db.Column('matricula', db.VARCHAR)
    fecha_fabricacion = db.Column('fecha_fabricacion', db.DateTime)
    marca = db.Column('marca', db.VARCHAR)
    modelo = db.Column('modelo', db.VARCHAR)
    id_cliente = db.Column('id_cliente', db.SMALLINT)
    Tipo = db.Column('Tipo', db.SMALLINT)

    def __init__(self, matricula, fecha, marca, modelo, id_cliente, tipo):
        self.matricula = matricula
        self.fecha_fabricacion = fecha
        self.marca = marca
        self.modelo = modelo
        self.id_cliente = id_cliente
        self.Tipo = tipo


@app.route('/', methods=['GET'])
def test():
    return jsonify({'info' : 'API REST - VELANDO CRUZ, JAVIER'})

# todos los recursos
@app.route('/clientes', methods=['GET'])
def getAllClientes():
    data = Cliente.query.all()
    arrayData = []
    for i in data:
        arrayData.append({'id':i.id,'nombres':i.nombres,'ciudad':i.ciudad,'sexo':i.sexo,'telefono':i.telefono,'direccion':i.direccion,'provincia':i.provincia})
    return json.dumps(arrayData)


@app.route('/ficheros',methods=['GET'])
def getAllFicheros():
    data = Fichero.query.all()
    arrayData= []
    #TOFIX, chheck jsonify
    for i in data:
        arrayData.append({'id':i.id,'nombre':i.nombre,'tipo':i.tipo,'id_Vehiculo':i.id_Vehiculo})
    return json.dumps(arrayData)

@app.route('/vehiculos', methods = ['GET'])
def getAllVehiculos():
    data = Vehiculo.query.all()
    arrayData = []
    
    #TOFIX, falta meter la fecha, al ponerla, peta, datatime is not serializable
    for i in data:
        arrayData.append({'id':i.id,'matricula':i.matricula,'marca':i.marca,'modelo':i.modelo,'id_cliente':i.id_cliente,'Tipo':i.Tipo})
    return json.dumps(arrayData)
    

#todos los recursos de 1 registro concreto
@app.route('/vehiculos/<int:vehiculoId>/ficheros', methods=['GET'])    
def getAllFicherosFromVehiculo(vehiculoId):
    data = Fichero.query.filter_by(id_Vehiculo=vehiculoId)
    arrayData = []
    #TOFIX
    for i in data:
        arrayData.append({'id':i.id,'nombre':i.nombre,'tipo':i.tipo,'id_Vehiculo':i.id_Vehiculo})
    return json.dumps(arrayData)

@app.route('/cliente/<int:clienteId>/vehiculos', methods = ['GET'])
def getAllVehiculosFromCliente(clienteId):
    data = Vehiculo.query.filter_by(id_cliente=clienteId)
    arrayData = []

    for i in data:
        arrayData.append({'id':i.id,'matricula':i.matricula,'marca':i.marca,'modelo':i.modelo,'id_cliente':i.id_cliente,'Ti    po':i.Tipo})
    return json.dumps(arrayData)

#1 registro por concreto
@app.route('/cliente/<int:id>', methods = ['GET'])
def getOneClient(id):
    data = Cliente.query.filter_by(id=id)
    arrayData = []
    arrayData.append({'id':data[0].id,'nombres':data[0].nombres,'ciudad':data[0].ciudad,'sexo':data[0].sexo,'telefono':data[0].telefono,'direccion':data[0].direccion,'provincia':data[0].provincia})
    return json.dumps(arrayData)


@app.route('/fichero/<int:fileId>', methods=['GET'])
def getOneFileById(fileId):
    data = Fichero.query.filter_by(id=fileId)
    arrayData = []
    arrayData.append({'id':data[0].id,'nombre':data[0].nombre,'tipo':data[0].tipo,'id_Vehiculo':data[0].id_Vehiculo})
    return json.dumps(arrayData)


@app.route('/vehiculo/<int:carId>', methods=['GET'])
def getOneCar(carId):
    data = Vehiculo.query.filter_by(id=carId)
    arrayData = []

    #toFIX; falta la fecha
    #TOFIX, si pongo un id que no existe, peta, INDEX OUT OF ERROR
    arrayData.append({'id':data[0].id,'matricula':data[0].matricula,'marca':data[0].marca,'modelo':data[0].modelo,'id_cliente':data[0].id_cliente,'Tipo':data[0].Tipo})
    return json.dumps(arrayData)



#POST
@app.route('/nuevo/cliente', methods = ['POST'])
def addCliente():
    #TEST COMMAND = curl -i -d '{"nombres":"testiee","ciudad":"Granada","sexo":"M","telefono":"123321123","fecha_nacimiento":"2000-06-23","direccion":"una random","provincia":"ninguna"}' -H "Content-Type: application/json" -X POST 127.0.0.1:8080/nuevo/cliente
    nombre = request.get_json(force=True)['nombres']
    ciudad = request.get_json(force=True)['ciudad']
    sexo = request.get_json(force=True)['sexo']
    telefono = request.get_json(force=True)['telefono']
    fecha_nacimiento = request.get_json(force=True)['fecha_nacimiento']
    direccion = request.get_json(force=True)['direccion']
    provincia = request.get_json(force=True)['provincia']

    nuevo = Cliente(nombre,ciudad,sexo,telefono,fecha_nacimiento,direccion, provincia)
    db.session.add(nuevo)
    db.session.commit()
    
    return "CLientee insertado con ID : {}".format(nuevo.id)



@app.route('/ficheros', methods = ['POST'])
def addFichero():
    #TEST COMMAND = curl -i -d '{"nombre":"POSTPRUEBA","tipo":"FacturaPOST","id_Vehiculo":1}' -H "Content-Type: application/json" -X POST 127.0.0.1:8080/ficheros
    nombre = request.get_json(force=True)['nombre']
    tipo = request.get_json(force=True)['tipo']
    id_Vehiculo = request.get_json(force=True)['id_Vehiculo']
    
    nuevo = Fichero(nombre, tipo, id_Vehiculo)
    db.session.add(nuevo)
    db.session.commit()
    
    #FIX this
    #return request.get_json(force=True)["nombre"]
    return "INSERTADO"


#data[0].fecha_fabricacion = data[0].fecha_fabricacion.replace(year=2012)
#test = datetime.strptime('2018-02-08', '%Y-%m-%d')
@app.route('/nuevo/vehiculo', methods = ['POST'])
def addVehiculo():
    #TEST COMMAND = curl -i -d '{"matricula":"1233-JU","fecha_fabricacion":"2018-02-08","marca":"Ford","modelo":"focus","id_cliente":1,"Tipo":2}' -H "Content-Type: application/json" -X POST 127.0.0.1:8080/nuevo/vehiculo
    matricula = request.get_json(force=True)['matricula']
    fecha = request.get_json(force=True)['fecha_fabricacion']
    marca = request.get_json(force=True)['marca']
    modelo = request.get_json(force=True)['modelo']
    id_cliente = request.get_json(force=True)['id_cliente']
    tipo = request.get_json(force=True)['Tipo']

    nuevo = Vehiculo(matricula, fecha, marca, modelo, id_cliente, tipo)
    db.session.add(nuevo)
    db.session.commit()
    
    return "Vehiculo Insertado con ID = {}".format(nuevo.id)





#PUT
@app.route('/editar/cliente', methods = ['PUT'])
def updateCliente():
    #TEST COMMAND = curl -i -d '{"id":6,"nombres":"testiee","ciudad":"Granada","sexo":"M","telefono":"123321123","fecha_nacimiento":"2000-06-23","direccion":"una random","provincia":"ninguna"}' -H "Content-Type: application/json" -X PUT 127.0.0.1:8080/editar/cliente
    id = request.get_json(force=True)['id']
    editar = Cliente.query.filter_by(id=id).first()
    editar.nombres = request.get_json(force=True)['nombres']
    editar.ciudad = request.get_json(force=True)['ciudad']
    editar.sexo = request.get_json(force=True)['sexo']
    editar.telefono = request.get_json(force=True)['telefono']
    editar.fecha_nacimiento = request.get_json(force=True)['fecha_nacimiento']
    editar.direccion = request.get_json(force=True)['direccion']
    editar.provincia = request.get_json(force=True)['provincia']
    editar.data = "updated!"
    db.session.commit()

    return "Cliente editado"



@app.route('/ficheros', methods = ['PUT'])
def updateFichero():
    #TEST COMMAND = curl -i -d '{"id":19,"nombre":"POSTPRUEBA","tipo":"FacturaPOST","id_Vehiculo":1}' -H "Content-Type: application/json" -X POST 127.0.0.1:8080/ficheros

    id = request.get_json(force=True)['id']
    editar = Fichero.query.filter_by(id=id).first()
    editar.nombre = request.get_json(force=True)['nombre']
    editar.tipo = request.get_json(force=True)['tipo']
    editar.id_Vehiculo = request.get_json(force=True)['id_Vehiculo']
    editar.data = "updated!"
    db.session.commit()

    return "EDITADO"

@app.route('/editar/vehiculo', methods = ['PUT'])
def updateVehiculo():
    #TEST COMMAND = curl -i -d '{"id":12,"matricula":"1233-JU","fecha_fabricacion":"2018-02-08","marca":"Ford","modelo":"focus","id_cliente":1,"Tipo":2}' -H "Content-Type: application/json" -X PUT 127.0.0.1:8080/editar/vehiculo
    
    id = request.get_json(force=True)['id']
    editar = Vehiculo.query.filter_by(id=id).first()
    editar.matricula = request.get_json(force=True)['matricula']
    editar.fecha_fabricacion = request.get_json(force=True)['fecha_fabricacion']
    editar.marca = request.get_json(force=True)['marca']
    editar.modelo = request.get_json(force=True)['modelo']
    editar.id_cliente = request.get_json(force=True)['id_cliente']
    editar.Tipo = request.get_json(force=True)['Tipo']
    editar.data = "updated!"
    db.session.commit()
    
    return "VEHICULO EDITADO"


#DELETE
@app.route('/borrar/cliente', methods = ['DELETE'])
def deleteClient():
    #TEST COMMAND = curl -i -d '{"id":5}' -H "Content-Type: application/json" -X DELETE 127.0.0.1:8080/borrar/cliente
    id = request.get_json(force=True)['id']
    borrar = Cliente.query.filter_by(id=id).first()
    db.session.delete(borrar)
    db.session.commit()

    return "Cliente borrado"

@app.route('/ficheros', methods = ['DELETE'])
def deleteFichero():
    #TEST COMMAND = curl -i -d '{"id":19}' -H "Content-Type: application/json" -X DELETE 127.0.0.1:8080/ficheros

    id = request.get_json(force=True)['id']
    borrar = Fichero.query.filter_by(id=id).first()
    db.session.delete(borrar)
    db.session.commit()
    
    return "BORRADO"

@app.route('/borrar/vehiculo', methods = ['DELETE'])
def deleteVehiculo():
    #TEST COMMAND = curl -i -d '{"id":13}' -H "Content-Type: application/json" -X DELETE 127.0.0.1:8080/borrar/vehiculo
    id = request.get_json(force=True)['id']
    borrar = Vehiculo.query.filter_by(id=id).first()
    db.session.delete(borrar)
    db.session.commit()

    return "Vehiculo Borrado"





if __name__ == '__main__':
   app.run(debug=True, port=8080)
