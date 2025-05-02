from flask import Blueprint, render_template, jsonify, request, current_app
import os
import json

association_bp = Blueprint('association', __name__)

def get_machines_file():
    return os.path.join(current_app.root_path, 'data', 'machines.json')

@association_bp.route('/cad_maquina', methods=['GET'])
def cad_maquina():
    """Renderiza a página de cadastro de máquinas."""
    return render_template('cad_maquina.html')

@association_bp.route('/save_association', methods=['POST'])
def save_association():
    """Salva associações de IPs a uma campanha e remove os desmarcados."""
    data = request.get_json()
    campaign_name = data.get('campaign_name')
    machine_ips = data.get('machine_ips', [])
    unselected_ips = data.get('unselected_ips', [])

    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')

    # Carregar associações existentes
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
    else:
        associations = []

    # Remover os IPs desmarcados da campanha atual
    associations = [
        assoc for assoc in associations
        if not (assoc['campaign_name'] == campaign_name and assoc['machine_ip'] in unselected_ips)
    ]

    # Adicionar os IPs selecionados à campanha atual
    for ip in machine_ips:
        if not any(assoc['campaign_name'] == campaign_name and assoc['machine_ip'] == ip for assoc in associations):
            associations.append({'campaign_name': campaign_name, 'machine_ip': ip})

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
    """Retorna a lista de associações registradas."""
    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')

    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
        return jsonify(associations), 200
    else:
        return jsonify({"error": "Arquivo associations.json não encontrado."}), 404

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
    """Salva um IP no arquivo machines.json."""
    data = request.get_json()
    machine_ip = data.get('machine_ip')

    if not machine_ip:
        return {"message": "Nenhum IP fornecido."}, 400

    machines_file = get_machines_file()

    # Carregar máquinas existentes
    if os.path.exists(machines_file):
        with open(machines_file, 'r') as file:
            machines = json.load(file)
    else:
        machines = []

    # Adicionar o IP se ainda não existir
    if machine_ip not in machines:
        machines.append(machine_ip)
        with open(machines_file, 'w') as file:
            json.dump(machines, file, indent=4)
        return {"message": f"IP {machine_ip} salvo com sucesso!"}, 200
    else:
        return {"message": f"IP {machine_ip} já existe."}, 400