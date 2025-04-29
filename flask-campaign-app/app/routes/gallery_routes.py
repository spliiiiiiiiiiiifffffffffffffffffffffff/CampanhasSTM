from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for
import os

gallery_bp = Blueprint('gallery', __name__)

@gallery_bp.route('/gallery', methods=['GET', 'POST'])
def gallery():
    """Renderiza a página da galeria de mídia e lida com uploads."""
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    if request.method == 'POST':
        # Lidar com o upload de arquivos
        if 'media_files' not in request.files:
            return "Nenhum arquivo enviado.", 400

        files = request.files.getlist('media_files')
        for file in files:
            if file.filename == '':
                continue  # Ignorar arquivos sem nome
            file.save(os.path.join(upload_folder, file.filename))

        return redirect(url_for('gallery.gallery'))

    # Listar arquivos existentes na galeria
    media_files = [file for file in os.listdir(upload_folder) if file.endswith(('png', 'jpg', 'jpeg', 'gif', 'mp4'))]
    return jsonify(media_files)  # Retorna as mídias como JSON para uso dinâmico

@gallery_bp.route('/gallery_page', methods=['GET'])
def gallery_page():
    """Renderiza a página da galeria de mídia."""
    upload_folder = os.path.join(current_app.static_folder, 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Listar arquivos existentes na galeria
    media_files = [file for file in os.listdir(upload_folder) if file.endswith(('png', 'jpg', 'jpeg', 'gif', 'mp4'))]
    return render_template('gallery.html', media_files=media_files)
