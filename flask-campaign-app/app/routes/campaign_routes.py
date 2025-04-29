from flask import Blueprint, render_template, request, jsonify, current_app
from flask import send_file, jsonify
import zipfile
import shutil
import io
import os
import json

campaign_bp = Blueprint('campaign', __name__)

def get_campaigns_file():
    """Retorna o caminho do arquivo campaigns.json."""
    return os.path.join(current_app.root_path, 'data', 'campaigns.json')

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

    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns = json.load(file)
    else:
        campaigns = []

    # Atualizar campanha existente ou adicionar nova
    updated = False
    for i, campaign in enumerate(campaigns):
        if campaign['name'] == data['name']:
            campaigns[i] = data
            updated = True
            break

    if not updated:
        campaigns.append(data)

    with open(campaigns_file, 'w') as file:
        json.dump(campaigns, file, indent=4)

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
            campaigns = json.load(file)
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
        machines = []

    return render_template('saved_campaigns.html', campaigns=campaigns, associations=associations, machines=machines)

@campaign_bp.route('/download_campaigns', methods=['GET'])
def download_campaigns():
    """Faz o download de todas as campanhas associadas ao IP do usuário como arquivos ZIP."""
    user_ip = request.remote_addr  # Obtém o IP do usuário
    associations_file = os.path.join(current_app.root_path, 'data', 'associations.json')
    campaigns_file = get_campaigns_file()
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    getcampaigns_file = os.path.join(current_app.static_folder, 'getcampaigns.json')

    # Carregar associações
    if os.path.exists(associations_file):
        with open(associations_file, 'r') as file:
            associations = json.load(file)
    else:
        return jsonify({"error": "Nenhuma associação encontrada."}), 404

    # Filtrar campanhas associadas ao IP do usuário
    associated_campaigns = [
        assoc['campaign_name'] for assoc in associations if assoc['machine_ip'] == user_ip
    ]

    # Carregar campanhas
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r') as file:
            campaigns = json.load(file)
    else:
        return jsonify({"error": "Nenhuma campanha encontrada."}), 404

    # Filtrar campanhas associadas
    user_campaigns = [campaign for campaign in campaigns if campaign['name'] in associated_campaigns]

    # Criar arquivos ZIP para cada campanha
    zip_folder = os.path.join(current_app.static_folder, 'zips')
    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder)

    zip_files = []
    for campaign in user_campaigns:
        campaign_name = campaign['name']
        zip_path = os.path.join(zip_folder, f"{campaign_name}.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for ad in campaign['ads']:
                for media_file in ad['media']:
                    media_path = os.path.join(upload_folder, media_file)
                    if os.path.exists(media_path):
                        zipf.write(media_path, arcname=media_file)
        zip_files.append(zip_path)

    # Atualizar o campo "updated" no arquivo getcampaigns.json
    if os.path.exists(getcampaigns_file):
        with open(getcampaigns_file, 'r') as file:
            getcampaigns_data = json.load(file)

        # Atualizar os arquivos baixados e marcar como atualizado
        current_files = [media for campaign in user_campaigns for ad in campaign['ads'] for media in ad['media']]
        if set(current_files) != set(getcampaigns_data.get('files', [])):
            getcampaigns_data['updated'] = 1  # Alteração detectada
        else:
            getcampaigns_data['updated'] = 0  # Nenhuma alteração

        getcampaigns_data['files'] = current_files

        with open(getcampaigns_file, 'w') as file:
            json.dump(getcampaigns_data, file, indent=4)

    # Criar um ZIP contendo todos os arquivos ZIP das campanhas
    all_campaigns_zip = os.path.join(zip_folder, 'all_campaigns.zip')
    with zipfile.ZipFile(all_campaigns_zip, 'w') as zipf:
        for zip_file in zip_files:
            zipf.write(zip_file, arcname=os.path.basename(zip_file))

    # Retornar o arquivo ZIP contendo todas as campanhas
    return send_file(
        all_campaigns_zip,
        mimetype='application/zip',
        as_attachment=True,
        download_name='all_campaigns.zip'
    )

