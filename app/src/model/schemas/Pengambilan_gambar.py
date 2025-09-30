from app import db
from app.src.utils.get_timezone import get_timezone

class Gambar(db.Model):
    __tablename__ = 'foto_sensor'  # ✅ Ini disesuaikan dengan nama tabel di database kamu

    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(255))  # Contoh: "20250720_210355.jpg"
    waktu = db.Column(db.DateTime(timezone=True), default=get_timezone)
    keterangan = db.Column(db.String(255))  # ✅ Tambahkan ini untuk menyimpan "masuk_kandang", dll.
