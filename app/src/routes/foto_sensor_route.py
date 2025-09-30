import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime

from app.src.repositories.foto_sensor_repository import simpan_foto_sensor_repository

foto_bp = Blueprint("foto_sensor", __name__)

UPLOAD_FOLDER = os.path.join("app", "static", "uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

# Fungsi bantu validasi ekstensi file
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@foto_bp.route("/upload_gambar", methods=["POST"])
def upload_gambar():
    if "file" not in request.files:
        return jsonify({"error": "Gambar tidak ditemukan di request"}), 400

    file = request.files["file"]
    keterangan = request.form.get("keterangan", "tidak_diketahui")

    if file and allowed_file(file.filename):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        # Simpan ke database via repository
        simpan_foto_sensor_repository({
            "nama_file": filename,
            "keterangan": keterangan,
        })

        return jsonify({"success": True, "filename": filename}), 200

    return jsonify({"error": "Format file tidak didukung"}), 400
