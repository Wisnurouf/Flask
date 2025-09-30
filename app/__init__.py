from flask import Flask
from dotenv import load_dotenv
import app.config as config
import os
import secrets
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")  # 🔥 Inisialisasi SocketIO

def create_app():
    load_dotenv()

    # ✅ Konfigurasi agar Flask tahu lokasi folder static (di luar folder app)
    app = Flask(
        __name__,
        static_folder='../static',       # Lokasi folder fisik
        static_url_path='/static'        # URL path untuk akses gambar
    )
    
    # 🔐 Gunakan SECRET_KEY dari env jika ada, jika tidak, generate random
    app.secret_key = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = '{driver}://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'.format(
        driver=app.config['DB_DRIVER'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        host=app.config['DB_HOST'],
        port=app.config['DB_PORT'],
        database=app.config['DB_NAME'],
    )

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)  # 🔌 Pasang SocketIO ke Flask app

    # ⬇️ Tambahkan ini supaya model dikenali oleh Flask-Migrate
    from app.src.model.schemas import Pengambilan_gambar, aktivitas_sensor, nomor_hp

    # ⬇️ Import semua blueprint route
    from app.src.routes.main import main as main_blueprint
    from app.src.routes.auth import auth as auth_blueprint
    from app.src.routes.sensor import sensor as sensor_blueprint
    from app.src.routes.notification import notification as notification_blueprint
    from app.src.routes.gambar import gambar_bp  # ✅ BENAR

    # ⬇️ Daftarkan semua blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(sensor_blueprint)
    app.register_blueprint(notification_blueprint)
    app.register_blueprint(gambar_bp)

    return app
