from flask import Blueprint, request, jsonify, send_from_directory
from app.src.repositories.pengambilan_gambar import (
    get_all_gambar_repository,
    get_gambar_by_id_repository,
    create_gambar_repository,
    delete_gambar_repository
)
import os
from datetime import datetime
import requests

gambar_bp = Blueprint('gambar_bp', __name__)

# Folder penyimpanan gambar
UPLOAD_FOLDER = 'static/gambar'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Alamat URL web server lokal yang bisa diakses dari HP/WA
SERVER_HOST = 'http://10.183.7.96:5010'  # Ganti IP sesuai IP lokal Flask kamu

# Endpoint untuk GET semua gambar
@gambar_bp.route('/gambar', methods=['GET'])
def get_all_gambar():
    gambar_list = get_all_gambar_repository()
    result = [{
        "id": g.id,
        "img": g.img,
        "waktu": g.waktu.isoformat()
    } for g in gambar_list]
    return jsonify(result), 200

# Endpoint untuk GET gambar by ID
@gambar_bp.route('/gambar/<int:gambar_id>', methods=['GET'])
def get_gambar_by_id(gambar_id):
    gambar = get_gambar_by_id_repository(gambar_id)
    if gambar:
        result = {
            "id": gambar.id,
            "img": gambar.img,
            "waktu": gambar.waktu.isoformat()
        }
        return jsonify(result), 200
    return jsonify({"message": "Gambar tidak ditemukan"}), 404

# Endpoint untuk POST gambar via JSON
@gambar_bp.route('/gambar', methods=['POST'])
def post_gambar():
    data = request.get_json()
    if not data or 'img' not in data:
        return jsonify({"message": "Field 'img' wajib diisi"}), 400

    new_gambar = create_gambar_repository(data)
    return jsonify({
        "message": "Gambar berhasil disimpan",
        "data": {
            "id": new_gambar.id,
            "img": new_gambar.img,
            "waktu": new_gambar.waktu.isoformat()
        }
    }), 201

# Endpoint untuk DELETE gambar
@gambar_bp.route('/gambar/<int:gambar_id>', methods=['DELETE'])
def delete_gambar(gambar_id):
    success = delete_gambar_repository(gambar_id)
    if success:
        return jsonify({"message": "Gambar berhasil dihapus"}), 200
    return jsonify({"message": "Gambar tidak ditemukan"}), 404

# ✅ Upload gambar dari ESP32-CAM (via POST binary)
@gambar_bp.route('/upload-gambar', methods=['POST'])
def upload_gambar_esp32cam_post():
    keterangan = request.args.get('keterangan', 'tanpa_keterangan')

    if not request.data:
        return jsonify({"message": "❌ Tidak ada data gambar"}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nama_file = f"{timestamp}.jpg"
    path_file = os.path.join(UPLOAD_FOLDER, nama_file)

    with open(path_file, 'wb') as f:
        f.write(request.data)

    # Simpan metadata ke database
    data = {
        "img": nama_file,
        "waktu": datetime.now(),
        "keterangan": keterangan
    }
    new_gambar = create_gambar_repository(data)

    # Kirim notifikasi WhatsApp (jika perlu)
    try:
        url_gambar = f"{SERVER_HOST}/gambar-file/{nama_file}"
        pesan = f"Ada pergerakan! 📷\nKeterangan: {keterangan}\nGambar: {url_gambar}"
        requests.post('http://localhost:5005/send-message', json={"message": pesan})
    except Exception as e:
        print(f"❌ Gagal mengirim ke WhatsApp: {e}")

    return jsonify({
        "message": "✅ Gambar berhasil diterima & disimpan",
        "data": {
            "id": new_gambar.id,
            "img": new_gambar.img,
            "waktu": new_gambar.waktu.isoformat(),
            "keterangan": new_gambar.keterangan
        }
    }), 201

# Endpoint untuk akses gambar sebagai file statis
@gambar_bp.route('/gambar-file/<filename>')
def serve_gambar_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
