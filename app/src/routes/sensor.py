from flask import Blueprint, request, jsonify
from app.src.repositories.data_sensor_repositories import delete_aktivitas_sensor_repository

sensor = Blueprint('sensor', __name__)

@sensor.route('/sensor/delete', methods=['POST'])
def sensor_delete():
    ids = request.json.get('ids', [])  # daftar ID yang mau dihapus
    deleted_count = 0

    for aktivitas_id in ids:
        if delete_aktivitas_sensor_repository(aktivitas_id):
            deleted_count += 1

    return jsonify({'success': True, 'deleted': deleted_count})
