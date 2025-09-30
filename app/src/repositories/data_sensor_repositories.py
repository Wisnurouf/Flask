from typing import List, Dict, Any
from app.src.model.schemas.aktivitas_sensor import AktivitasSensor
from app import db

# Ambil semua data aktivitas sensor
def get_all_aktivitas_sensor_repository() -> list:
    return AktivitasSensor.query.order_by(AktivitasSensor.waktu.desc()).all()

# Ambil data aktivitas berdasarkan ID
def get_aktivitas_sensor_by_id_repository(sensor_id: int) -> AktivitasSensor:
    return AktivitasSensor.query.get(sensor_id)

# Tambah data aktivitas baru ke database
def create_aktivitas_sensor_repository(data: Dict[str, Any]) -> AktivitasSensor:
    aktivitas = AktivitasSensor(**data)
    db.session.add(aktivitas)
    db.session.commit()
    return aktivitas

# Hapus semua data sebelum tanggal tertentu
def delete_old_aktivitas_sensor_repository(tanggal_batas):
    deleted = AktivitasSensor.query.filter(AktivitasSensor.waktu < tanggal_batas).delete()
    db.session.commit()
    return deleted

# Hapus 1 data berdasarkan ID
def delete_aktivitas_sensor_repository(sensor_id: int) -> bool:
    aktivitas = AktivitasSensor.query.get(sensor_id)
    if aktivitas:
        db.session.delete(aktivitas)
        db.session.commit()
        return True
    return False

