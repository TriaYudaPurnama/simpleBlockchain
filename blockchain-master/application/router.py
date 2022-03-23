#!/usr/bin/env python3
from application import *

# from application.blockchain import *

@app.route('/identity/new', methods=['GET'])
def new_identity():
    blockchain.add_identity_assets()
    response = {
        'result': 'done'
    }    
    return jsonify(response), 200


@app.route('/car/new', methods=['GET'])
def new_car():
    blockchain.add_car_assets()
    response = {
        'result': 'done'
    }  
    return jsonify(response), 200


@app.route('/money/new', methods=['GET'])
def new_money():
    blockchain.add_initial_money()
    response = {
        'result': 'done'
    }    
    return jsonify(response), 200

@app.route('/costnew', methods=['GET'])
def new_cost():
    blockchain.insert_asset_cost()
    response = {
        'result': 'done'
    }  
    return jsonify(response), 200

@app.route('/cost', methods=['GET'])
def find_cost():    
    var_reg_number = request.args.get('reg_number')
    print(str(var_reg_number))
    cost = blockchain.find_asset_cost(str(var_reg_number))
    response = {
        'cost': cost  
    }  
    return jsonify(response), 200


@app.route('/transaction', methods=['GET'])
def new_transaction():    
    blockchain.request_transaction()
    response = {
        'result': 'done'  
    }  
    return jsonify(response), 200


@app.route('/transfercar', methods=['GET'])
def transfer_car(): 
    var_reg_number = request.args.get('reg_number')
    var_buyer_name = request.args.get('name')   
    blockchain.transfer_car(var_reg_number,var_buyer_name)
    response = {
        'result': 'car successfully transferred'  
    }  
    return jsonify(response), 200
