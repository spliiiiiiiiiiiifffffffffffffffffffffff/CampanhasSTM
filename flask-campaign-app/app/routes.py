from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import json
import re

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Predefined users
USERS = {
    'admin': 'adminpassword',
    'client': 'clientpassword'
}

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@main.route('/')
def home():
    return render_template('login.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            if username == 'admin' or username == 'client':
                return redirect(url_for('main.campanhaconfig'))  # Redireciona para campanhaconfig
        else:
            flash('Credenciais inválidas. Tente novamente.')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic here (e.g., save user to the database)
        username = request.form['username']
        password = request.form['password']
        flash('Registration successful! Please log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/gallery', methods=['GET', 'POST'])
def gallery():
    upload_folder = os.path.join(current_app.static_folder, 'uploads')  # Caminho absoluto para o diretório de uploads

    # Certifique-se de que o diretório existe
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Lidar com uploads de arquivos
    if request.method == 'POST':
        if 'media_files' in request.files:
            files = request.files.getlist('media_files')
            
            # Verificar se o número de arquivos excede o limite
            if len(files) > 5:
                flash('Você pode enviar no máximo 5 arquivos por vez.')
                return redirect(url_for('main.gallery'))

            for file in files:
                if file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(upload_folder, filename))
                else:
                    flash(f'O arquivo {file.filename} não é válido.')
            flash('Arquivos enviados com sucesso!')
            return redirect(url_for('main.gallery'))

    # Listar arquivos no diretório
    media_files = []
    try:
        media_files = os.listdir(upload_folder)
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")

    return render_template('gallery.html', media_files=media_files)

@main.route('/campaign_config', methods=['GET', 'POST'])
def campaign_config():
    return redirect(url_for('main.campanhaconfig'))

@main.route('/campanhaconfig', methods=['GET', 'POST'])
def campanhaconfig():
    upload_folder = os.path.join(current_app.static_folder, 'uploads')  # Caminho absoluto para o diretório de uploads

    # Certifique-se de que o diretório existe
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Listar arquivos no diretório
    media_files = []
    try:
        media_files = os.listdir(upload_folder)
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")

    # Filtrar apenas arquivos permitidos
    media_files = [file for file in media_files if allowed_file(file)]

    return render_template('campanhaconfig.html', media_files=media_files)

@main.route('/saved_campaigns', methods=['GET'])
def saved_campaigns():
    # Caminho para os arquivos JSON
    MACHINES_FILE = os.path.join(current_app.root_path, 'data', 'machines.json')
    CAMPAIGNS_FILE = os.path.join(current_app.root_path, 'data', 'campaigns.json')
    ASSOCIATIONS_FILE = os.path.join(current_app.root_path, 'data', 'associations.json')
    UPLOAD_FOLDER = os.path.join(current_app.static_folder, 'uploads')

    # Carregar máquinas
    try:
        with open(MACHINES_FILE, 'r') as file:
            machines = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        machines = []

    # Carregar campanhas
    try:
        with open(CAMPAIGNS_FILE, 'r') as file:
            campaigns = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        campaigns = []

    # Carregar associações
    try:
        with open(ASSOCIATIONS_FILE, 'r') as file:
            associations = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        associations = []

    # Listar arquivos de mídia
    try:
        media_files = [file for file in os.listdir(UPLOAD_FOLDER) if allowed_file(file)]
    except FileNotFoundError:
        media_files = []

    # Garantir que todas as variáveis sejam listas válidas
    machines = machines if isinstance(machines, list) else []
    campaigns = campaigns if isinstance(campaigns, list) else []
    associations = associations if isinstance(associations, list) else []
    media_files = media_files if isinstance(media_files, list) else []

    return render_template(
        'saved_campaigns.html',
        machines=machines,
        campaigns=campaigns,
        associations=associations,
        media_files=media_files,
        enumerate=enumerate
    )

def get_campaigns_file():
    return os.path.join(current_app.root_path, 'data', 'campaigns.json')

@main.route('/save_campaign', methods=['POST'])
def save_campaign():
    data = request.get_json()
    if not data:
        return {"message": "Nenhuma campanha enviada."}, 400

    campaigns_file = get_campaigns_file()
    getcampaigns_file = os.path.join(current_app.static_folder, 'getcampaigns.json')

    # Carregar campanhas existentes
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns = json.load(file)
    else:
        campaigns = []

    # Atualizar ou adicionar a campanha
    updated = False
    for i, campaign in enumerate(campaigns):
        if campaign['name'] == data['name']:
            campaigns[i] = data
            updated = True
            break

    if not updated:
        campaigns.append(data)

    # Salvar no arquivo JSON
    with open(campaigns_file, 'w') as file:
        json.dump(campaigns, file, indent=4)

    # Atualizar o valor de `updated` no arquivo getcampaigns.json
    if os.path.exists(getcampaigns_file):
        with open(getcampaigns_file, 'r') as file:
            getcampaigns_data = json.load(file)
        getcampaigns_data["updated"] = 1  # Define como 1 após a edição
        getcampaigns_data["campaign_name"] = data['name']
        getcampaigns_data["files"] = [media for ad in data['ads'] for media in ad['media']]
        with open(getcampaigns_file, 'w') as file:
            json.dump(getcampaigns_data, file, indent=4)

    return {"message": "Campanha salva com sucesso!"}, 200

@main.route('/get_campaigns', methods=['GET'])
def get_campaigns():
    campaigns_file = get_campaigns_file()
    associations_file = get_associations_file()

    # Carregar campanhas
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns = json.load(file)
    else:
        campaigns = []

    # Carregar associações
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
    else:
        associations = []

    return jsonify({"campaigns": campaigns, "associations": associations}), 200

@main.route('/delete_campaign', methods=['POST'])
def delete_campaign():
    data = request.get_json()
    campaign_name = data.get('name')

    if not campaign_name:
        return {"success": False, "message": "Nome da campanha não fornecido."}, 400

    campaigns_file = get_campaigns_file()

    # Carregar campanhas existentes
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns = json.load(file)
    else:
        return {"success": False, "message": "Nenhuma campanha encontrada."}, 404

    # Remover a campanha pelo nome
    updated_campaigns = [c for c in campaigns if c['name'] != campaign_name]

    # Salvar as campanhas atualizadas
    with open(campaigns_file, 'w') as file:
        json.dump(updated_campaigns, file, indent=4)

    return {"success": True, "message": f"Campanha '{campaign_name}' removida com sucesso."}, 200


@main.route('/cad_maquina', methods=['GET', 'POST'])
def cad_maquina():
    MACHINES_FILE = os.path.join(current_app.root_path, 'data', 'machines.json')  # Caminho para o arquivo machines.json

    if request.method == 'POST':
        machine_id = request.form.get('machine_id')

        if not machine_id:
            flash('ID da máquina é obrigatório.')
            return redirect(url_for('main.cad_maquina'))

        # Validar formato de IP
        ip_pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$')
        if not ip_pattern.match(machine_id):
            flash('ID da máquina deve ser um endereço IP válido.')
            return redirect(url_for('main.cad_maquina'))

        # Carregar máquinas existentes
        if os.path.exists(MACHINES_FILE):
            with open(MACHINES_FILE, 'r') as file:
                machines = json.load(file)
        else:
            machines = []

        # Verificar se a máquina já está cadastrada
        if machine_id in machines:
            flash(f'Máquina {machine_id} já está cadastrada.')
        else:
            machines.append(machine_id)  # Adicionar a nova máquina
            with open(MACHINES_FILE, 'w') as file:
                json.dump(machines, file, indent=4)
            flash(f'Máquina {machine_id} cadastrada com sucesso!')

    return render_template('cad_maquina.html')

def get_associations_file():
    return os.path.join(current_app.root_path, 'data', 'associations.json')


@main.route('/save_association', methods=['POST'])
def save_association():
    data = request.get_json()
    campaign_name = data.get('campaign_name')
    machines = data.get('machines', [])

    if not campaign_name:
        return {"success": False, "message": "Nome da campanha é obrigatório."}, 400

    # Carregar associações existentes
    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
    else:
        associations = []

    # Atualizar as associações para a campanha
    associations = [assoc for assoc in associations if assoc['campaign_name'] != campaign_name]
    for machine in machines:
        associations.append({"campaign_name": campaign_name, "machine_ip": machine})

    # Salvar as associações atualizadas
    with open(associations_file, 'w') as file:
        json.dump(associations, file, indent=4)

    return {"success": True, "message": f"Máquinas associadas à campanha '{campaign_name}' com sucesso."}, 200

@main.route('/associations', methods=['GET'])
def download_associated_files():
    client_ip = request.remote_addr  # Obtém o IP do cliente
    associations_file = get_associations_file()
    campaigns_file = get_campaigns_file()
    getcampaigns_file = os.path.join(current_app.static_folder, 'getcampaigns.json')

    # Verificar se os arquivos JSON existem
    if not os.path.exists(associations_file) or not os.path.exists(campaigns_file):
        return jsonify({"error": "Arquivos de configuração não encontrados."}), 404

    # Carregar associações
    with open(associations_file, 'r') as file:
        associations = json.load(file)

    # Encontrar a campanha associada ao IP do cliente
    associated_entry = next(
        (assoc for assoc in associations if assoc['machine_ip'] == client_ip),
        None
    )

    if not associated_entry:
        return jsonify({"error": "Nenhuma campanha associada ao IP."}), 404

    associated_campaign = associated_entry['campaign_name']

    # Carregar campanhas
    with open(campaigns_file, 'r') as file:
        campaigns = json.load(file)

    # Encontrar os arquivos da campanha associada
    campaign = next(
        (camp for camp in campaigns if camp['name'] == associated_campaign),
        None
    )

    if not campaign:
        return jsonify({"error": "Campanha associada não encontrada."}), 404

    # Caminho para os arquivos de mídia
    media_folder = os.path.join(current_app.static_folder, 'uploads')

    # Criar uma lista de caminhos completos para os arquivos
    files = []
    for ad in campaign['ads']:
        for media in ad['media']:
            file_path = os.path.join(media_folder, media)
            if os.path.exists(file_path):
                files.append(file_path)

    if not files:
        return jsonify({"error": "Nenhum arquivo encontrado para a campanha associada."}), 404

    # Compactar os arquivos em um único arquivo ZIP
    zip_filename = f"{associated_campaign}_files.zip"
    zip_path = os.path.join(media_folder, zip_filename)

    import zipfile
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))  # Adiciona o arquivo ao ZIP

    # Atualizar o valor de `updated` no arquivo getcampaigns.json
    if os.path.exists(getcampaigns_file):
        with open(getcampaigns_file, 'r') as file:
            getcampaigns_data = json.load(file)
        getcampaigns_data["updated"] = 0  # Define como 0 após o download
        getcampaigns_data["campaign_name"] = associated_campaign
        getcampaigns_data["files"] = [os.path.basename(file) for file in files]
        with open(getcampaigns_file, 'w') as file:
            json.dump(getcampaigns_data, file, indent=4)

    # Retornar o arquivo ZIP para download
    return send_file(zip_path, as_attachment=True)

@main.route('/associations/gallery/<filename>', methods=['GET'])
def download_gallery_file(filename):
    # Caminho para o diretório de uploads
    upload_folder = os.path.join(current_app.static_folder, 'uploads')

    # Caminho completo do arquivo solicitado
    file_path = os.path.join(upload_folder, filename)

    # Verificar se o arquivo existe
    if not os.path.exists(file_path):
        return jsonify({"error": "Arquivo não encontrado."}), 404

    # Retornar o arquivo para download
    return send_file(file_path, as_attachment=True)

@main.route('/update', methods=['GET'])
def update_campaign_files():
    client_ip = request.remote_addr  # Obtém o IP do cliente
    associations_file = get_associations_file()
    campaigns_file = get_campaigns_file()
    getcampaigns_file = os.path.join(current_app.static_folder, 'getcampaigns.json')

    # Verificar se os arquivos JSON existem
    if not os.path.exists(associations_file) or not os.path.exists(campaigns_file):
        return jsonify({"error": "Arquivos de configuração não encontrados."}), 404

    # Carregar associações
    with open(associations_file, 'r') as file:
        associations = json.load(file)

    # Encontrar a campanha associada ao IP do cliente
    associated_entry = next(
        (assoc for assoc in associations if assoc['machine_ip'] == client_ip),
        None
    )

    if not associated_entry:
        return jsonify({"error": "Nenhuma campanha associada ao IP."}), 404

    associated_campaign = associated_entry['campaign_name']

    # Carregar campanhas
    with open(campaigns_file, 'r') as file:
        campaigns = json.load(file)

    # Encontrar os arquivos da campanha associada
    campaign = next(
        (camp for camp in campaigns if camp['name'] == associated_campaign),
        None
    )

    if not campaign:
        return jsonify({"error": "Campanha associada não encontrada."}), 404

    # Obter o valor de `updated` do arquivo getcampaigns.json
    if os.path.exists(getcampaigns_file):
        with open(getcampaigns_file, 'r') as file:
            getcampaigns_data = json.load(file)
        updated = getcampaigns_data.get("updated", 0)
    else:
        updated = 0

    # Criar o JSON com os dados relevantes
    output_data = {
        "updated": updated,
        "campaign_name": associated_campaign,
        "files": [media for ad in campaign['ads'] for media in ad['media']]
    }

    # Retornar os dados no formato JSON
    return jsonify(output_data), 200

def mark_campaign_updated(campaign_name):
    associations_file = get_associations_file()

    # Carregar associações existentes
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
    else:
        associations = []

    # Atualizar a variável `updated` para 1
    for assoc in associations:
        if assoc['campaign_name'] == campaign_name:
            assoc['updated'] = 1
            break

    # Salvar as associações atualizadas
    with open(associations_file, 'w') as file:
        json.dump(associations, file, indent=4)

@main.route('/reset_updated', methods=['POST'])
def reset_updated():
    getcampaigns_file = os.path.join(current_app.static_folder, 'getcampaigns.json')

    if os.path.exists(getcampaigns_file):
        with open(getcampaigns_file, 'r') as file:
            getcampaigns_data = json.load(file)
        getcampaigns_data["updated"] = 0  # Define como 0
        with open(getcampaigns_file, 'w') as file:
            json.dump(getcampaigns_data, file, indent=4)

    return {"success": True, "message": "Valor de 'updated' resetado para 0."}, 200

@main.route('/get_updated', methods=['GET'])
def get_updated():
    # Caminho para o arquivo getcampaigns.json
    getcampaigns_file = os.path.join(current_app.static_folder, 'getcampaigns.json')

    # Verificar se o arquivo existe
    if os.path.exists(getcampaigns_file):
        with open(getcampaigns_file, 'r') as file:
            getcampaigns_data = json.load(file)
        # Retornar apenas a variável "updated"
        return jsonify({"updated": getcampaigns_data.get("updated", 0)}), 200

    # Caso o arquivo não exista, retornar "updated" como 0
    return jsonify({"updated": 0}), 200

@main.route('/static/data/machines.json', methods=['GET'])
def get_machines():
    machines_file = os.path.join(current_app.root_path, 'data', 'machines.json')
    if os.path.exists(machines_file):
        with open(machines_file, 'r') as file:
            machines = json.load(file)
        return jsonify(machines)
    else:
        return jsonify({"error": "Arquivo machines.json não encontrado."}), 404
    
    
@main.route('/static/data/associations.json', methods=['GET'])
def get_associations():
    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
        return jsonify(associations)
    else:
        return jsonify({"error": "Arquivo associations.json não encontrado."}), 404
    
@main.route('/static/data/campaigns.json', methods=['GET'])
def get_campaigns_data():
    campaigns_file = os.path.join(current_app.root_path, 'data', 'campaigns.json')
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns = json.load(file)
        return jsonify(campaigns)
    else:
        return jsonify({"error": "Arquivo campaigns.json não encontrado."}), 404
