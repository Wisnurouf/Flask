from app import create_app, socketio
import threading

# ✅ Import layanan MQTT (jalan di background)
from app.src.services.mqtt_service import run_mqtt_service

# ===============================
# Inisialisasi Flask App
# ===============================
app = create_app()

# ===============================
# Jalankan layanan MQTT di thread terpisah
# ===============================
def start_background_services():
    threading.Thread(
        target=lambda: run_mqtt_service(app.app_context()),
        daemon=True
    ).start()

# ===============================
# Jalankan Flask App (socketio)
# ===============================
if __name__ == "__main__":
    start_background_services()
    socketio.run(
        app,
        debug=False,
        host="0.0.0.0",
        port=5010,
        use_reloader=False,
        allow_unsafe_werkzeug=True  # hanya untuk pengembangan
    )
