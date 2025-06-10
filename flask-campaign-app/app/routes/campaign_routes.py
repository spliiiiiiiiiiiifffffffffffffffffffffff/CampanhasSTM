from flask import Blueprint, render_template, request, jsonify, current_app, send_file
import zipfile
import shutil
import io
import os
import json
import codecs

campaign_bp = Blueprint('campaign', __name__)
association_bp = Blueprint('association', __name__)

def get_campaigns_file():
    """Retorna o caminho do arquivo campaigns.json."""
    return os.path.join(current_app.root_path, 'data', 'campaigns.json')

def get_gallery_file():
    return os.path.join(current_app.root_path, 'data', 'gallery.json')

@campaign_bp.route('/campaign_config', methods=['GET', 'POST'])
def campaign_config():
    """Renderiza a página de configuração de campanhas."""
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    media_files = [file for file in os.listdir(upload_folder) if file.endswith(('png', 'jpg', 'jpeg', 'gif', 'mp4'))]
    return render_template('campanhaconfig.html', media_files=media_files)

@campaign_bp.route('/save_campaign', methods=['POST'])
def save_campaign():
    """Salva uma nova campanha ou atualiza uma existente."""
    data = request.get_json()
    campaigns_file = get_campaigns_file()

    # Garante que o campo 'mode' está presente
    if 'mode' not in data:
        data['mode'] = 'self'  # Default, se não vier do frontend

    # Carregar campanhas existentes
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns_data = json.load(file)
        campaigns = campaigns_data.get("campaigns", [])
        tags = campaigns_data.get("tags", {})
    else:
        campaigns = []
        tags = {}

    # Atualizar campanha existente ou adicionar nova
    updated = False
    for i, campaign in enumerate(campaigns):
        if campaign['name'] == data['name']:
            campaigns[i] = data
            updated = True
            break

    if not updated:
        campaigns.append(data)

    # Salvar de volta no formato correto
    with open(campaigns_file, 'w', encoding='utf-8') as file:
        json.dump({"campaigns": campaigns, "tags": tags}, file, ensure_ascii=False, indent=4)

    update_campaign_status(data['name'], updated_value=1)
    return {"message": "Campanha salva com sucesso!"}, 200

@campaign_bp.route('/list_campaigns', methods=['GET'])
def list_campaigns():
    """Retorna a lista de campanhas salvas."""
    campaigns_file = get_campaigns_file()

    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns = json.load(file)
    else:
        campaigns = []

    return jsonify(campaigns), 200

@campaign_bp.route('/delete_campaign/<string:campaign_name>', methods=['DELETE'])
def delete_campaign(campaign_name):
    """Exclui uma campanha pelo nome."""
    campaigns_file = get_campaigns_file()

    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns = json.load(file)
    else:
        return jsonify({"message": "Nenhuma campanha encontrada."}), 404

    # Filtrar campanhas para excluir a correspondente
    updated_campaigns = [campaign for campaign in campaigns if campaign['name'] != campaign_name]

    if len(updated_campaigns) == len(campaigns):
        return jsonify({"message": f"Campanha '{campaign_name}' não encontrada."}), 404

    with open(campaigns_file, 'w') as file:
        json.dump(updated_campaigns, file, indent=4)

    return jsonify({"message": f"Campanha '{campaign_name}' excluída com sucesso!"}), 200

@campaign_bp.route('/edit_campaign/<string:campaign_name>', methods=['PUT'])
def edit_campaign(campaign_name):
    """Edita as mídias associadas a uma campanha existente."""
    data = request.get_json()
    campaigns_file = get_campaigns_file()

    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns = json.load(file)
    else:
        return {"message": "Nenhuma campanha encontrada."}, 404

    # Atualizar a campanha correspondente
    updated = False
    for i, campaign in enumerate(campaigns):
        if campaign['name'] == campaign_name:
            campaigns[i]['ads'] = data.get('ads', [])
            updated = True
            break

    if not updated:
        return {"message": f"Campanha '{campaign_name}' não encontrada."}, 404

    with open(campaigns_file, 'w') as file:
        json.dump(campaigns, file, indent=4)

    # Atualizar o campo 'updated' para todos os tokens associados à campanha
    update_campaign_status(campaign_name, updated_value=1)

    return {"message": f"Mídias da campanha '{campaign_name}' atualizadas com sucesso!"}, 200

@campaign_bp.route('/saved_campaigns', methods=['GET'])
def saved_campaigns():
    """Renderiza a página de campanhas salvas."""
    campaigns_file = get_campaigns_file()
    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')
    machines_file = os.path.join(current_app.root_path, 'data', 'machines.json')

    # Carregar campanhas
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns_data = json.load(file)
        campaigns = campaigns_data.get("campaigns", [])  # <-- Pegue só o array!
    else:
        campaigns = []

    # Carregar associações
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
    else:
        associations = []

    # Carregar máquinas
    if os.path.exists(machines_file):
        with open(machines_file, 'r') as file:
            machines = json.load(file)
    else:
        machines = {}

    token_to_machine = {token: {"name": machine_data['name']} for token, machine_data in machines.items()}
    for assoc in associations:
        machine_info = token_to_machine.get(assoc['machine_token'], {})
        assoc['machine_name'] = machine_info.get('name', 'Desconhecido')

    return render_template('saved_campaigns.html', campaigns=campaigns, associations=associations, machines=machines)

    # Carregar associações
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
    else:
        return jsonify({"error": "Nenhuma associação encontrada."}), 404


    # Carregar campanhas
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns = json.load(file)
    else:
        return jsonify({"error": "Nenhuma campanha encontrada."}), 404

    # Filtrar campanhas associadas
    user_campaigns = [campaign for campaign in campaigns if campaign['name'] in associated_campaigns]

   

    # Criar arquivos ZIP para cada campanha associada
    zip_folder = os.path.join(current_app.static_folder, 'zips')
    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder)

    for campaign in user_campaigns:
        campaign_name = campaign['name']
        zip_path = os.path.join(zip_folder, f"{campaign_name}.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for ad in campaign['ads']:
                for media_file in ad['media']:
                    media_path = os.path.join(upload_folder, media_file)
                    if os.path.exists(media_path):
                        zipf.write(media_path, arcname=media_file)

        # Atualizar o campo "updated" no arquivo getcampaigns.json
        if os.path.exists(getcampaigns_file):
            with open(getcampaigns_file, 'r') as file:
                getcampaigns_data = json.load(file)

            # Verificar se a campanha foi atualizada
            campaign_media = []
            for ad in campaign['ads']:
                campaign_media.extend(ad['media'])

            if set(campaign_media) != set(getcampaigns_data.get('files', [])):
                getcampaigns_data['updated'] = 1  # Campanha foi atualizada
                getcampaigns_data['files'] = campaign_media
            else:
                getcampaigns_data['updated'] = 0  # Campanha não foi atualizada

            getcampaigns_data['campaign_name'] = campaign_name

            with open(getcampaigns_file, 'w') as file:
                json.dump(getcampaigns_data, file, indent=4)

        # Retornar o arquivo ZIP da campanha
        return send_file(zip_path, as_attachment=True)

    # Carregar associações
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
    else:
        return jsonify({"error": "Nenhuma associação encontrada."}), 404


    # Carregar campanhas
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns = json.load(file)
    else:
        return jsonify({"error": "Nenhuma campanha encontrada."}), 404

    # Encontrar a campanha correspondente
    campaign = next((c for c in campaigns if c['name'] == campaign_name), None)
    if not campaign:
        return jsonify({"error": f"Campanha '{campaign_name}' não encontrada."}, 404)

    associated_campaigns = [
        assoc['campaign_name'] for assoc in associations if assoc['machine_token'] == machine_token
    ]
    if campaign_name not in associated_campaigns:
        return jsonify({"error": f"A campanha '{campaign_name}' não está associada ao token fornecido."}), 403

    # Criar o arquivo ZIP para a campanha
    zip_folder = os.path.join(current_app.static_folder, 'zips')
    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder)

    zip_path = os.path.join(zip_folder, f"{campaign_name}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for ad in campaign['ads']:
            for media_file in ad['media']:
                media_path = os.path.join(upload_folder, media_file)
                if os.path.exists(media_path):
                    zipf.write(media_path, arcname=media_file)

    # Atualizar o campo "updated" no arquivo getcampaigns.json
    if os.path.exists(getcampaigns_file):
        with open(getcampaigns_file, 'r') as file:
            getcampaigns_data = json.load(file)
        if getcampaigns_data.get('campaign_name') == campaign_name:
            getcampaigns_data['updated'] = 0  # Marcar como baixado
            with open(getcampaigns_file, 'w') as file:
                json.dump(getcampaigns_data, file, indent=4)

    # Retornar o arquivo ZIP da campanha
    return send_file(zip_path, as_attachment=True)

@campaign_bp.route('/download_campaigns/<string:machine_token>', methods=['GET'])
def download_campaign_by_token(machine_token):
    """Faz o download do arquivo ZIP da campanha associada ao token fornecido e atualiza o campo 'updated'."""
    getcampaigns_file = os.path.join(current_app.static_folder, 'getcampaigns.json')
    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')
    campaigns_file = get_campaigns_file()
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    zip_folder = os.path.join(current_app.static_folder, 'zips')

    # Verificar se os arquivos necessários existem
    if not os.path.exists(associations_file) or not os.path.exists(campaigns_file):
        return jsonify({"error": "Arquivos necessários não encontrados."}), 404

    # Carregar associações
    with open(associations_file, 'r') as file:
        associations = json.load(file)

    # Verificar se o token está associado a alguma campanha
    associated_campaign = next((assoc['campaign_name'] for assoc in associations if assoc['machine_token'] == machine_token), None)
    if not associated_campaign:
        return jsonify({"error": "Nenhuma campanha associada ao token fornecido."}), 404

    # Carregar campanhas
    with open(campaigns_file, 'r') as file:
        campaigns = json.load(file)

    # Encontrar a campanha correspondente
    campaign = next((c for c in campaigns if c['name'] == associated_campaign), None)
    if not campaign:
        return jsonify({"error": f"Campanha '{associated_campaign}' não encontrada no arquivo 'campaigns.json'."}), 404

    # Criar o arquivo ZIP para a campanha
    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder)

    zip_path = os.path.join(zip_folder, f"{associated_campaign}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for ad in campaign['ads']:
            for media_file in ad['media']:
                media_path = os.path.join(upload_folder, media_file)
                if os.path.exists(media_path):
                    zipf.write(media_path, arcname=media_file)

    # Atualizar o campo 'updated' para o token específico
    with open(getcampaigns_file, 'r') as file:
        try:
            getcampaigns_data = json.load(file)
        except json.JSONDecodeError:
            getcampaigns_data = {}

    if machine_token in getcampaigns_data:
        getcampaigns_data[machine_token]["updated"] = 0
        current_app.logger.info(f"Campo 'updated' atualizado para 0 para o token {machine_token}.")
    else:
        current_app.logger.warning(f"Token {machine_token} não encontrado no arquivo 'getcampaigns.json'.")

    with open(getcampaigns_file, 'w') as file:
        json.dump(getcampaigns_data, file, indent=4)
        current_app.logger.info(f"Arquivo 'getcampaigns.json' salvo com sucesso.")

    # Retornar o arquivo ZIP da campanha
    return send_file(zip_path, as_attachment=True)

@campaign_bp.route('/get_campaigns_status', methods=['GET'])
def get_campaigns_status():
    """Retorna o JSON 'getcampaigns.json'."""
    getcampaigns_file = os.path.join(current_app.static_folder, 'getcampaigns.json')

    # Verificar se o arquivo necessário existe
    if not os.path.exists(getcampaigns_file):
        return jsonify({"error": "Arquivo 'getcampaigns.json' não encontrado."}), 404

    # Carregar os dados de getcampaigns.json
    with open(getcampaigns_file, 'r') as file:
        getcampaigns_data = json.load(file)

    return jsonify(getcampaigns_data), 200

@campaign_bp.route('/get_campaigns_status/<string:machine_token>', methods=['GET'])
def get_campaigns_status_by_token(machine_token):
    """Retorna os dados de 'getcampaigns.json' específicos para o token fornecido."""
    getcampaigns_file = os.path.join(current_app.static_folder, 'getcampaigns.json')
    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')
    campaigns_file = get_campaigns_file()

    # Verificar se os arquivos necessários existem
    if not os.path.exists(getcampaigns_file):
        return jsonify({"error": "Arquivo 'getcampaigns.json' não encontrado."}), 404
    if not os.path.exists(associations_file):
        return jsonify({"error": "Arquivo 'associations.json' não encontrado."}), 404
    if not os.path.exists(campaigns_file):
        return jsonify({"error": "Arquivo 'campaigns.json' não encontrado."}), 404

    # Carregar associações
    with open(associations_file, 'r') as file:
        associations = json.load(file)

    # Verificar se o token está associado a alguma campanha
    associated_campaign = next((assoc['campaign_name'] for assoc in associations if assoc['machine_token'] == machine_token), None)
    if not associated_campaign:
        return jsonify({"error": "Nenhuma campanha associada ao token fornecido."}), 404

    # Carregar campanhas
    with open(campaigns_file, 'r') as file:
        campaigns = json.load(file)

    # Encontrar a campanha correspondente
    campaign = next((c for c in campaigns if c['name'] == associated_campaign), None)
    if not campaign:
        return jsonify({"error": f"Campanha '{associated_campaign}' não encontrada no arquivo 'campaigns.json'."}), 404

    # Obter todas as mídias associadas à campanha
    campaign_media = []
    for ad in campaign.get('ads', []):
        campaign_media.extend(ad.get('media', []))

    # Carregar os dados de getcampaigns.json
    with open(getcampaigns_file, 'r') as file:
        try:
            getcampaigns_data = json.load(file)
        except json.JSONDecodeError:
            getcampaigns_data = {}

    # Atualizar o campo 'updated' apenas se necessário
    if machine_token in getcampaigns_data:
        if getcampaigns_data[machine_token].get("files") != campaign_media:
            getcampaigns_data[machine_token]["updated"] = 1
            getcampaigns_data[machine_token]["files"] = campaign_media
        else:
            getcampaigns_data[machine_token]["updated"] = 0
    else:
        # Adicionar o token se não existir
        getcampaigns_data[machine_token] = {
            "updated": 1,
            "campaign_name": associated_campaign,
            "files": campaign_media
        }

    # Salvar as alterações no arquivo getcampaigns.json
    with open(getcampaigns_file, 'w') as file:
        json.dump(getcampaigns_data, file, indent=4)

    # Retornar os dados específicos do token
    return jsonify(getcampaigns_data[machine_token]), 200

@association_bp.route('/get_campaigns_status_by_token', methods=['POST'])
def get_campaigns_status():
    """Retorna as campanhas associadas ao token da máquina que acessou a rota."""
    # Caminhos dos arquivos necessários
    campaigns_file = os.path.join(current_app.root_path, 'data', 'campaigns.json')
    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')

    # Obter o token enviado pelo cliente
    data = request.get_json()
    machine_token = data.get('machine_token')

    if not machine_token:
        return jsonify({"error": "Token da máquina não fornecido."}), 400

    # Verificar se o token é válido
    if not os.path.exists(associations_file):
        return jsonify({"error": "Arquivo 'associations.json' não encontrado."}), 404

    with open(associations_file, 'r') as file:
        associations = json.load(file)

    # Filtrar as campanhas associadas ao token
    associated_campaigns = [
        assoc['campaign_name'] for assoc in associations if assoc['machine_token'] == machine_token
    ]

    if not associated_campaigns:
        return jsonify({"error": "Nenhuma campanha associada ao token fornecido."}), 404

    # Verificar se o arquivo campaigns.json existe
    if not os.path.exists(campaigns_file):
        return jsonify({"error": "Arquivo 'campaigns.json' não encontrado."}), 404

    with open(campaigns_file, 'r') as file:
        campaigns_data = json.load(file)

    # Filtrar os detalhes das campanhas associadas
    campaigns = [campaign for campaign in campaigns_data if campaign['name'] in associated_campaigns]

    return jsonify({"campaigns": campaigns}), 200

@association_bp.route('/get_campaigns_status_by_token', methods=['POST'])
def get_campaigns_status_by_token():
    """Retorna as campanhas associadas ao token da máquina que acessou a rota."""
    # Caminhos dos arquivos necessários
    campaigns_file = os.path.join(current_app.root_path, 'data', 'campaigns.json')
    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')

    # Obter o token enviado pelo cliente
    data = request.get_json()
    machine_token = data.get('machine_token')

    if not machine_token:
        return jsonify({"error": "Token da máquina não fornecido."}), 400

    # Verificar se o token é válido
    if not os.path.exists(associations_file):
        return jsonify({"error": "Arquivo 'associations.json' não encontrado."}), 404

    with open(associations_file, 'r') as file:
        associations = json.load(file)

    # Filtrar as campanhas associadas ao token
    associated_campaigns = [
        assoc['campaign_name'] for assoc in associations if assoc['machine_token'] == machine_token
    ]

    if not associated_campaigns:
        return jsonify({"error": "Nenhuma campanha associada ao token fornecido."}), 404

    # Verificar se o arquivo campaigns.json existe
    if not os.path.exists(campaigns_file):
        return jsonify({"error": "Arquivo 'campaigns.json' não encontrado."}), 404

    with open(campaigns_file, 'r') as file:
        campaigns_data = json.load(file)

    # Filtrar os detalhes das campanhas associadas
    campaigns = [campaign for campaign in campaigns_data if campaign['name'] in associated_campaigns]

    return jsonify({"campaigns": campaigns}), 200

def update_campaign_status(campaign_name, machine_token=None, updated_value=1):
    """
    Atualiza o campo 'updated' no arquivo getcampaigns.json.
    - Se machine_token for fornecido, atualiza apenas para aquele token.
    - Caso contrário, atualiza para todos os tokens associados à campanha.
    """
    getcampaigns_file = os.path.join(current_app.static_folder, 'getcampaigns.json')
    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')

    # Verificar se os arquivos necessários existem
    if not os.path.exists(getcampaigns_file):
        with open(getcampaigns_file, 'w') as file:
            json.dump({}, file)  # Criar um arquivo vazio se não existir

    if not os.path.exists(associations_file):
        return {"error": "Arquivo 'associations.json' não encontrado."}

    # Carregar os dados de getcampaigns.json
    with open(getcampaigns_file, 'r') as file:
        try:
            getcampaigns_data = json.load(file)
        except json.JSONDecodeError:
            getcampaigns_data = {}

    # Carregar as associações
    with open(associations_file, 'r') as file:
        associations = json.load(file)

    # Atualizar o campo 'updated'
    if machine_token:
        # Atualizar apenas o token específico
        if machine_token in getcampaigns_data:
            getcampaigns_data[machine_token]["updated"] = updated_value
        else:
            # Adicionar o token se não existir
            getcampaigns_data[machine_token] = {
                "updated": updated_value,
                "campaign_name": campaign_name,
                "files": []
            }
    else:
        # Atualizar todos os tokens associados à campanha
        for assoc in associations:
            if assoc['campaign_name'] == campaign_name:
                token = assoc['machine_token']
                if token in getcampaigns_data:
                    getcampaigns_data[token]["updated"] = updated_value
                else:
                    # Adicionar o token se não existir
                    getcampaigns_data[token] = {
                        "updated": updated_value,
                        "campaign_name": campaign_name,
                        "files": []
                    }

    # Salvar as alterações no arquivo getcampaigns.json
    with open(getcampaigns_file, 'w') as file:
        json.dump(getcampaigns_data, file, indent=4)

@campaign_bp.route('/media_files_by_mode/<string:mode>', methods=['GET'])
def get_media_files_by_mode(mode):
    """Retorna todas as mídias da galeria para o modo especificado."""
    gallery_file = get_gallery_file()
    if os.path.exists(gallery_file):
        with open(gallery_file, 'r', encoding='utf-8') as f:
            gallery_data = json.load(f)
    else:
        gallery_data = {"inibicao": [], "self": [], "antena": []}
    if mode not in gallery_data:
        return jsonify({"media_files": []})
    return jsonify({"media_files": gallery_data[mode]})

@campaign_bp.route('/media_files/<string:campaign_name>', methods=['GET'])
def get_campaign_media_files(campaign_name):
    campaigns_file = get_campaigns_file()
    gallery_file = get_gallery_file()
    upload_folder = os.path.join(current_app.static_folder, 'uploads')

    # Carregar campanhas
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r', encoding='utf-8') as file:
            campaigns_data = json.load(file)
        campaigns = campaigns_data.get("campaigns", [])
        tags = campaigns_data.get("tags", {})
    else:
        return jsonify({"error": "Nenhuma campanha encontrada."}), 404

    # Encontrar a campanha e seu modo
    campaign = next((c for c in campaigns if c['name'] == campaign_name), None)
    if not campaign:
        return jsonify({"error": f"Campanha '{campaign_name}' não encontrada."}), 404

    mode = campaign.get('mode', 'self')  # Default para 'self'

    # Carregar mídias do modo correto em gallery.json
    if os.path.exists(gallery_file):
        with open(gallery_file, 'r', encoding='utf-8') as f:
            gallery_data = json.load(f)
        media_list = gallery_data.get(mode, [])
    else:
        media_list = []

    # Filtrar apenas arquivos que existem fisicamente
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    upload_media = set(os.listdir(upload_folder))
    media_files = [media['filename'] for media in media_list if media['filename'] in upload_media]

    return jsonify({"media_files": media_files, "tags": tags})
