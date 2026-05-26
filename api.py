from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('192.168.79.10', 27017)

db = client.carrosdb

colecao = db.carros

@app.route('/carros', methods=['GET'])
def listar():
    carros = []

    for carro in colecao.find({}, {'_id': 0}): # retira o campo _id para não dar erro no jsonify
        carros.append(carro)

    return jsonify(carros)


@app.route('/carros', methods=['POST'])
def criar():
    dados = request.json

    colecao.insert_one(dados)

    dados.pop('_id', None) # esse campo fazia dar erro no jsonify
    # removi ele para não dar mensagem de erro quando o POST acontece certo
    # descobri o erro no POST primeiro, mas também precisava tirar no GET

    return jsonify(dados)


@app.route('/carros/<placa>', methods=['PUT'])
def atualizar(placa):
    dados = request.json

    colecao.update_one(
        {'placa': placa},
        {'$set': dados}
    )

    return jsonify({'msg': 'atualizado'})


@app.route('/carros/<placa>', methods=['DELETE'])
def deletar(placa):
    colecao.delete_one({'placa': placa})

    return jsonify({'msg': 'deletado'})


app.run(host='0.0.0.0', port=5000)