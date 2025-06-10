from flask import Blueprint, render_template, jsonify, request, current_app, session, abort
import os
import json
from unidecode import unidecode  # Adicione esta importação no início do arquivo
import secrets  # Adicionado para gerar tokens

association_bp = Blueprint('association', __name__)

def generate_machine_token():
    return secrets.token_urlsafe(16)  # Gera um token seguro de 16 bytes

def get_machines_file():
    return os.path.join(current_app.root_path, 'data', 'machines.json')

@association_bp.route('/cad_maquina', methods=['GET'])
def cad_maquina():
    """Renderiza a página de cadastro de máquinas e lista campanhas/tokens."""
    if session.get('tipo') == 0:  # CLIENT
        abort(403)
    # Carregar associações
    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
    else:
        associations = []
    return render_template('cad_maquina.html', associations=associations)

@association_bp.route('/save_association', methods=['POST'])
def save_association():
    """Salva associações de tokens a uma campanha e remove os desmarcados."""
    data = request.get_json()
    campaign_name = data.get('campaign_name')
    machine_tokens = data.get('machine_tokens', [])
    unselected_tokens = data.get('unselected_tokens', [])

    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')
    machines_file = get_machines_file()

    # Carregar associações existentes
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
    else:
        associations = []

    # Carregar máquinas existentes
    if os.path.exists(machines_file):
        with open(machines_file, 'r') as file:
            machines = json.load(file)
    else:
        machines = {}

    # Criar um mapeamento de tokens para IPs
    token_to_ip = {token: machine_data['ip'] for token, machine_data in machines.items()}

    # Remover os tokens desmarcados da campanha atual
    associations = [
        assoc for assoc in associations
        if not (assoc['campaign_name'] == campaign_name and assoc['machine_token'] in unselected_tokens)
    ]

    # Adicionar os tokens selecionados à campanha atual
    for token in machine_tokens:
        if token not in [assoc.get('machine_token') for assoc in associations if assoc['campaign_name'] == campaign_name]:
            associations.append({'campaign_name': campaign_name, 'machine_token': token})

    # Salvar as associações atualizadas
    with open(associations_file, 'w') as file:
        json.dump(associations, file, indent=4)

    return {"message": "Associações atualizadas com sucesso!"}, 200

@association_bp.route('/get_machines', methods=['GET'])
def get_machines():
    """Retorna a lista de máquinas registradas."""
    machines_file = get_machines_file()

    if os.path.exists(machines_file):
        with open(machines_file, 'r') as file:
            machines = json.load(file)
        return jsonify(machines), 200
    else:
        return jsonify({"error": "Arquivo machines.json não encontrado."}), 404

@association_bp.route('/get_associations', methods=['GET'])
def get_associations():
    """Retorna a lista de associações registradas com os nomes das máquinas."""
    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')
    machines_file = get_machines_file()

    # Carregar associações existentes
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
    else:
        associations = []

    # Carregar máquinas existentes
    if os.path.exists(machines_file):
        with open(machines_file, 'r') as file:
            machines = json.load(file)
    else:
        machines = {}

    # Mapear tokens para IPs e nomes
    token_to_machine = {token: {"name": machine_data['name'], "ip": machine_data['ip']} for token, machine_data in machines.items()}

    # Atualizar associações com nomes e IPs das máquinas
    for assoc in associations:
        machine_info = token_to_machine.get(assoc['machine_token'], {})
        assoc['machine_name'] = machine_info.get('name', 'Desconhecido')
        assoc['machine_ip'] = machine_info.get('ip', 'Desconhecido')
        
    return jsonify(associations), 200

@association_bp.route('/remove_association', methods=['POST'])
def remove_association():
    """Remove a associação de um IP a uma campanha."""
    data = request.get_json()
    campaign_name = data.get('campaign_name')
    machine_ip = data.get('machine_ip')

    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')

    # Carregar associações existentes
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
    else:
        return {"message": "Nenhuma associação encontrada."}, 404

    # Remover a associação específica
    associations = [
        assoc for assoc in associations
        if not (assoc['campaign_name'] == campaign_name and assoc['machine_ip'] == machine_ip)
    ]

    # Salvar as associações atualizadas
    with open(associations_file, 'w') as file:
        json.dump(associations, file, indent=4)

    return {"message": f"Associação do IP {machine_ip} removida da campanha '{campaign_name}' com sucesso!"}, 200

@association_bp.route('/save_machine', methods=['POST'])
def save_machine():
    """Salva um IP e um nome no arquivo machines.json."""
    data = request.get_json()
    machine_name = data.get('machine_name')
    machine_ip = data.get('machine_ip')

    if not machine_name or not machine_ip:
        return {"message": "Nome ou IP da máquina não fornecido."}, 400

    machines_file = get_machines_file()

    # Carregar máquinas existentes
    if os.path.exists(machines_file):
        with open(machines_file, 'r') as file:
            machines = json.load(file)
    else:
        machines = {}

    # Gerar um token único para a máquina
    machine_token = secrets.token_urlsafe(16)

    # Verificar se o IP já está registrado
    for token, machine_data in machines.items():
        if machine_data['ip'] == machine_ip:
            return {"message": f"O IP {machine_ip} já está registrado como '{machine_data['name']}'."}, 400

    # Adicionar ou atualizar a máquina com o token
    machines[machine_token] = {
        "name": machine_name,
        "ip": machine_ip
    }

    # Salvar as máquinas atualizadas
    machines_file = os.path.join(current_app.root_path, 'data', 'machines.json')
    with open(machines_file, 'w', encoding='utf-8') as file:
        json.dump(machines, file, ensure_ascii=False, indent=4)

    return {"message": f"Máquina '{machine_name}' com IP {machine_ip} salva com sucesso!", "token": machine_token}, 200

@association_bp.route('/update_machine_ip', methods=['POST'])
def update_machine_ip():
    """Atualiza o IP de uma máquina existente."""
    data = request.get_json()
    machine_token = data.get('machine_token')
    new_ip = data.get('new_ip')

    if not machine_token or not new_ip:
        return {"message": "Token ou novo IP não fornecido."}, 400

    machines_file = get_machines_file()

    # Carregar máquinas existentes
    if os.path.exists(machines_file):
        with open(machines_file, 'r') as file:
            machines = json.load(file)
    else:
        return {"message": "Nenhuma máquina encontrada."}, 404

    # Atualizar o IP da máquina
    if machine_token in machines:
        machines[machine_token]['ip'] = new_ip
        with open(machines_file, 'w', encoding='utf-8') as file:
            json.dump(machines, file, ensure_ascii=False, indent=4)
        return {"message": f"IP da máquina atualizado para {new_ip}."}, 200
    else:
        return {"message": "Token da máquina não encontrado."}, 404