from flask import Blueprint, render_template, redirect, request, url_for, session, flash, jsonify
import app.config as config
from app.src.utils import cards, table_rows
from app.src.routes.validation.login import login_required
from app.src.repositories.data_sensor_repositories import (
    get_all_aktivitas_sensor_repository,
    get_aktivitas_sensor_by_id_repository,
    delete_aktivitas_sensor_repository,
)
from app.src.repositories.nohp_repositories import get_all_nomor_hp
from app.src.model.schemas.aktivitas_sensor import AktivitasSensor
from app.src.repositories.pengambilan_gambar import (
    get_all_gambar_repository,
    create_gambar_repository
)
from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

# ============================ DASHBOARD ============================

@main.route('/')
@login_required
def index():
    data_sensor = get_all_aktivitas_sensor_repository()
    if data_sensor is None:
        flash("Data sensor tidak ditemukan.", "danger")
        return redirect(url_for('main.index'))
    return render_template('pages/index.html', cards=cards, table_rows=data_sensor)

# ============================ WHATSAPP ============================

@main.route('/whatsapp', methods=['GET'])
@login_required
def whatsapp():
    get_nomor_hp = get_all_nomor_hp()
    if get_nomor_hp is None:
        flash("Nomor WhatsApp tidak ditemukan.", "danger")
        return redirect(url_for('main.index'))
    return render_template('pages/notification/whatapps.html', table_rows=get_nomor_hp)

# ============================ HAPUS ============================

@main.route('/hapus', methods=['POST'])
def hapus_terpilih():
    data = request.get_json()
    ids = data.get("ids", [])
    if not ids:
        return jsonify({"error": "Tidak ada data yang dipilih."}), 400

    try:
        for sensor_id in ids:
            aktivitas = AktivitasSensor.query.get(sensor_id)
            if aktivitas:
                db.session.delete(aktivitas)

        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ============================ GALERI GAMBAR ============================

@main.route('/galeri')
@login_required
def galeri():
    data_gambar = get_all_gambar_repository()
    return render_template('pages/galeri.html', foto_rows=data_gambar)
