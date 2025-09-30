import paho.mqtt.client as paho
from paho import mqtt
import os
import time
from datetime import datetime, timedelta
import ssl
import certifi
import json
from dotenv import load_dotenv

from app import socketio
from app.src.repositories.data_sensor_repositories import create_aktivitas_sensor_repository
from app.src.services.notification_service import notify_sensor_data_Service  # ✅ Tambahan

# Load ENV
load_dotenv()

# Konfigurasi MQTT
BROKER = os.environ.get('MQTT_BROKER', '')
PORT = 8883
USERNAME = os.environ.get('MQTT_USERNAME')
PASSWORD = os.environ.get('MQTT_PASSWORD')

# Topik dari ESP32 kamu
TOPICS = [
    ("kandang/gerakan", 1),
]

client = None
app_context = None

# ✅ Simpan status sebelumnya
last_active = False

# MQTT CONNECT
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Terhubung ke MQTT Broker")
        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
            print(f"📡 Subscribed: {topic}")
    else:
        print(f"❌ Gagal koneksi MQTT, kode: {rc}")

# HANDLER untuk pesan dari ESP32
def handle_kandang_data(client, userdata, msg):
    global app_context
    global last_active

    try:
        payload = msg.payload.decode('utf-8').strip()
        print(f"📡 Data MQTT dari ESP32: {payload}")

        data = json.loads(payload)

        # Emit ke frontend via websocket
        socketio.emit("kandang_update", data)

        # ✅ Filter logika agar hanya simpan saat aktif atau perubahan status
        pir_aktif = data.get("pir1") or data.get("pir2") or data.get("pir3")
        tipe = data.get("tipe")
        objek_terdeteksi = tipe in ["manusia", "domba"]

        if pir_aktif or objek_terdeteksi:
            last_active = True
        elif last_active:
            # hanya simpan sekali waktu jadi tidak aktif
            last_active = False
        else:
            # sudah tidak aktif dan kosong → abaikan
            return

        # ✅ Simpan ke database
        with app_context:
            create_aktivitas_sensor_repository({
                "pir1_status": data.get("pir1", False),
                "pir2_status": data.get("pir2", False),
                "pir3_status": data.get("pir3", False),
                "jarak_ultrasonik": data.get("jarak", 0),
                "tipe_objek": data.get("tipe", "tidak_diketahui"),
                "buzzer_status": data.get("buzzer", False),
                "pola_gerakan": data.get("pola_gerakan"),
            })
            print("✅ Data disimpan ke database")

            # 🔔 Kirim notifikasi WhatsApp
            msg = f"🚨 Deteksi {tipe.upper()}!\nPola: {data.get('pola_gerakan', 'Tidak diketahui')}\nJarak: {data.get('jarak', 0)} cm"
            notify_sensor_data_Service(msg, app_context)

    except Exception as e:
        print(f"❌ Gagal proses data dari MQTT: {e}")

# JALANKAN SERVICE
def run_mqtt_service(app_instance):
    global client, app_context
    app_context = app_instance

    print(f"🔌 Menghubungkan ke MQTT {BROKER}:{PORT}")
    client = paho.Client(client_id="esp32_kandang_client", protocol=paho.MQTTv5)
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set(ca_certs=certifi.where(), tls_version=ssl.PROTOCOL_TLS_CLIENT)

    client.on_connect = on_connect
    client.message_callback_add("kandang/gerakan", handle_kandang_data)

    try:
        client.connect(BROKER, PORT)
        client.loop_start()
    except Exception as e:
        print(f"❌ Gagal koneksi: {e}")
        socketio.emit("mqtt_error", {"error": str(e)})
        return

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 MQTT dimatikan")
        client.disconnect()
        client.loop_stop()