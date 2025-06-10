from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for, flash
import os
import json

gallery_bp = Blueprint('gallery', __name__)

# --- Adicione no topo do arquivo ---
def get_campaigns_file():
    return os.path.join(current_app.root_path, 'data', 'campaigns.json')

def load_tags_from_campaigns():
    campaigns_file = get_campaigns_file()
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('tags', {})
    return {}

def save_tags_to_campaigns(tags):
    campaigns_file = get_campaigns_file()
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"campaigns": [], "tags": {}}
    data['tags'] = tags
    with open(campaigns_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_tags_file():
    # Caminho correto para a pasta DATA
    return os.path.join(current_app.root_path, 'data', 'media_tags.json')

def load_media_tags():
    tags_file = get_tags_file()
    if os.path.exists(tags_file):
        with open(tags_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_media_tags(tags):
    tags_file = get_tags_file()
    with open(tags_file, 'w', encoding='utf-8') as f:
        json.dump(tags, f, ensure_ascii=False, indent=4)

def load_gallery_json():
    path = os.path.join(current_app.root_path, 'data', 'gallery.json')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"inibicao": [], "self": [], "antena": []}

@gallery_bp.route('/media_tags', methods=['POST'])
def update_media_tag():
    data = request.get_json()
    filename = data.get('filename')
    tag = data.get('tag')
    tags = load_tags_from_campaigns()
    if tag:
        tags[filename] = tag
    elif filename in tags:
        del tags[filename]
    save_tags_to_campaigns(tags)
    return jsonify({"success": True, "tags": tags})

@gallery_bp.route('/gallery', methods=['GET', 'POST'])
def gallery():
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    if request.method == 'POST':
        if 'media_files' not in request.files:
            flash("Nenhum arquivo foi selecionado para upload.", "error")
            return redirect(url_for('gallery.gallery_page'))

        files = request.files.getlist('media_files')
        mode = request.form.get('mode')
        if mode not in ['inibicao', 'self', 'antena']:
            flash("Selecione um modo válido.", "error")
            return redirect(url_for('gallery.gallery_page'))

        # Carregar tags e galeria
        tags = load_tags_from_campaigns()
        gallery_data = load_gallery_json()

        for file in files:
            if file.filename == '':
                continue
            file.save(os.path.join(upload_folder, file.filename))
            tag = tags.get(file.filename, file.filename)
            # Evitar duplicatas
            if not any(m['filename'] == file.filename for m in gallery_data[mode]):
                gallery_data[mode].append({
                    "filename": file.filename,
                    "tag": tag
                })

        # Salvar galeria atualizada
        with open(os.path.join(current_app.root_path, 'data', 'gallery.json'), 'w', encoding='utf-8') as f:
            json.dump(gallery_data, f, ensure_ascii=False, indent=4)

        flash("Arquivos enviados com sucesso!", "success")
        return redirect(url_for('gallery.gallery_page'))

    # Listar arquivos existentes na galeria
    media_files = [file for file in os.listdir(upload_folder) if file.endswith(('png', 'jpg', 'jpeg', 'gif', 'mp4'))]
    tags = load_tags_from_campaigns()
    gallery_data = load_gallery_json()
    return render_template('gallery.html', media_files=media_files, tags=tags, gallery_data=gallery_data)

@gallery_bp.route('/gallery_page', methods=['GET'])
def gallery_page():
    """Renderiza a página da galeria de mídia."""
    mode = request.args.get('mode', 'inibicao')  # padrão: inibicao
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Listar arquivos existentes na galeria
    media_files = [file for file in os.listdir(upload_folder) if file.endswith(('png', 'jpg', 'jpeg', 'gif', 'mp4'))]
    tags = load_tags_from_campaigns()
    gallery_data = load_gallery_json()  # <-- Adicione esta linha
    filtered_media = gallery_data.get(mode, [])
    return render_template(
        'gallery.html',
        media_files=media_files,
        tags=tags,
        gallery_data={mode: filtered_media},
        selected_mode=mode
    )

@gallery_bp.route('/media_files', methods=['GET'])
def get_media_files():
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    media_files = [file for file in os.listdir(upload_folder) if file.endswith(('png', 'jpg', 'jpeg', 'gif', 'mp4'))]
    tags = load_tags_from_campaigns()
    return jsonify({"media_files": media_files, "tags": tags})
