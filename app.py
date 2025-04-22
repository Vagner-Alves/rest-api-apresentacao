from flask import Flask, request, jsonify

app = Flask(__name__)

# Armazenamento em memória
items = {}

# METHOD GET
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items), 200

# METHOD GET ITEM ESPECIFICO
@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    item = items.get(item_id)
    if item:
        return jsonify({item_id: item}), 200
    return jsonify({"erro": "Item não encontrado"}), 404

# METHOD POST - Criar novo item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    item_id = data.get("id")

    if not item_id or item_id in items:
        return jsonify({"erro": "ID inválido ou duplicado"}), 400

    item = {
        "nome": data.get("nome"),
        "preco": data.get("preco"),
        "descricao": data.get("descricao")
    }

    if not item["nome"] or item["preco"] is None:
        return jsonify({"erro": "Campos obrigatórios: nome e preco"}), 400

    items[item_id] = item
    return jsonify({item_id: item}), 201

# METHOD PUT - Atualizar item existente
@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    if item_id not in items:
        return jsonify({"erro": "Item não encontrado"}), 404

    data = request.get_json()
    item = items[item_id]

    item["nome"] = data.get("nome", item["nome"])
    item["preco"] = data.get("preco", item["preco"])
    item["descricao"] = data.get("descricao", item.get("descricao"))

    return jsonify({item_id: item}), 200

# METHOD DELETE - Deletar item
@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id in items:
        deleted = items.pop(item_id)
        return jsonify({item_id: deleted}), 200
    return jsonify({"erro": "Item não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
