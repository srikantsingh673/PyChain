from flask import Flask, jsonify, request
from blocks import PyChain
import json
import os
import requests

app = Flask(__name__)

PEERS_FILE = 'peers.json'

def load_peers():
    if os.path.exists(PEERS_FILE):
        with open(PEERS_FILE, 'r') as f:
            return set(json.load(f))
    print("peer: load", set())
    return set()

def save_peers(peers):
    with open(PEERS_FILE, 'w') as f:
        json.dump(list(peers), f)

blockchain = PyChain()
blockchain.nodes = load_peers()

@app.route('/mine_block', methods=['POST'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    # Broadcast the new block to all peers
    print("blockchain.nodes :", blockchain.nodes)
    for node in blockchain.nodes:
        print("node:", node)
        try:
            url = f"{node}/add_block"
            print("url:", url)
            res = requests.post(url, json={'block': block})
            print("res:", res.text)
        except Exception:
            pass  # Ignore errors for simplicity
    response = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/register_node', methods=['POST'])
def register_node():
    data = request.get_json()
    nodes = data.get('nodes')
    if nodes is None or not isinstance(nodes, list):
        return jsonify({'message': 'Please provide a list of node addresses.'}), 400
    for node in nodes:
        blockchain.add_node(node)
    # Save peers to file
    save_peers(blockchain.nodes)
    return jsonify({'message': 'Nodes registered successfully.', 'total_nodes': list(blockchain.nodes)}), 201


@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.get_json()
    block = data.get('block')
    if not block:
        return jsonify({'message': 'No block data provided.'}), 400
    # Simple validation: check previous_hash and proof
    last_block = blockchain.get_previous_block()
    print("last_block:", last_block )
    print("block:", blockchain.hash(last_block) )
    if block['previous_hash'] != blockchain.hash(last_block):
        return jsonify({'message': 'Invalid previous hash.'}), 400
    if not blockchain.is_chain_valid(blockchain.chain + [block]):
        return jsonify({'message': 'Invalid block.'}), 400
    blockchain.chain.append(block)
    return jsonify({'message': 'Block added to chain.'}), 201


@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    longest_chain = None
    max_length = len(blockchain.chain)
    for node in blockchain.nodes:
        try:
            response = requests.get(f"{node}/get_chain")
            if response.status_code == 200:
                data = response.json()
                length = data['length']
                chain = data['chain']
                if length > max_length and blockchain.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        except Exception:
            pass  # Ignore errors for simplicity
    if longest_chain:
        blockchain.chain = longest_chain
        return jsonify({'message': 'Chain was replaced.', 'new_chain': blockchain.chain}), 200
    else:
        return jsonify({'message': 'Current chain is already the longest.', 'chain': blockchain.chain}), 200


@app.route('/get_peers', methods=['GET'])
def get_peers():
    # Always reload peers from file in case of external changes
    blockchain.nodes = load_peers()
    return jsonify({'peers': list(blockchain.nodes)}), 200


app.run(host='0.0.0.0', port=5000, debug=True)

