from app import db
from app.src.utils.get_timezone import get_timezone

class AktivitasSensor(db.Model):
    __tablename__ = 'aktivitas_sensor'

    id = db.Column(db.Integer, primary_key=True)

    # Status masing-masing sensor PIR
    pir1_status = db.Column(db.Boolean, default=False)
    pir2_status = db.Column(db.Boolean, default=False)
    pir3_status = db.Column(db.Boolean, default=False)

    # Data ultrasonik
    jarak_ultrasonik = db.Column(db.Float)  # cm

    # Hasil klasifikasi objek
    tipe_objek = db.Column(db.String(50))  # manusia / domba / tidak_diketahui

    # Status buzzer
    buzzer_status = db.Column(db.Boolean, default=False)

    # Pola Gerakan
    pola_gerakan = db.Column(db.String(50))

    # Timestamp
    waktu = db.Column(db.DateTime(timezone=True), default=get_timezone)
