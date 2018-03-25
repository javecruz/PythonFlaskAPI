from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from src.models.cliente import Cliente

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
    return jsonify({'message' : 'It works'})

@app.route('/clientes',methods=['GET'])
def getAllClientes():
    data = Cliente.query.all()
    return data

if __name__ == '__main__':
    app.run(debug=True, port=8080)
