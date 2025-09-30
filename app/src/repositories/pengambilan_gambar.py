from typing import List, Dict, Any
from app.src.model.schemas.Pengambilan_gambar import Gambar
from app import db

# Ambil semua gambar
def get_all_gambar_repository() -> List[Gambar]:
    return Gambar.query.order_by(Gambar.waktu.desc()).all()

# Ambil gambar berdasarkan ID
def get_gambar_by_id_repository(gambar_id: int) -> Gambar:
    return Gambar.query.get(gambar_id)

# Tambah gambar baru
def create_gambar_repository(data: Dict[str, Any]) -> Gambar:
    gambar = Gambar(
        img=data.get("img"),
        waktu=data.get("waktu"),
        keterangan=data.get("keterangan", "")  # Tambahkan support kolom keterangan
    )
    db.session.add(gambar)
    db.session.commit()
    return gambar

# Hapus gambar berdasarkan ID
def delete_gambar_repository(gambar_id: int) -> bool:
    gambar = Gambar.query.get(gambar_id)
    if gambar:
        db.session.delete(gambar)
        db.session.commit()
        return True
    return False

# Hapus gambar-gambar lama sebelum tanggal tertentu
def delete_old_gambar_repository(tanggal_batas):
    deleted = Gambar.query.filter(Gambar.waktu < tanggal_batas).delete()
    db.session.commit()
    return deleted
