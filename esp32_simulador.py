import time
import json
import threading
import paho.mqtt.client as mqtt
from datetime import datetime
import pytz
import os

# ===========================
# CONFIG (via ambiente)
# ===========================
CODESPUNI = os.getenv("CODESPUNI", "123")
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
ESP_NAME = os.getenv("ESP_NAME", "esp2")

TOPIC_SENSOR = f"jws/{CODESPUNI}/data"
TOPIC_STATUS = f"jws/{CODESPUNI}/device_status"

# timezone Fortaleza
tz = pytz.timezone('America/Fortaleza')

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


def now_timestamp():
    return int(time.mktime(datetime.now(tz).timetuple()))


def connect():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print(f"[INFO] Conectado ao broker {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        print(f"[ERRO] Conexão MQTT falhou: {e}")


def enviar_status_on():
    status_msg = {
        "codesp": CODESPUNI,
        "ipaddr": "10.0.0.1",
        "macaddr": "00:00:00:00:00:00",
        "status": "on",
        "esp_name": ESP_NAME,
        "counted_at": now_timestamp()
    }
    client.publish(TOPIC_STATUS, json.dumps(status_msg))
    print("[MQTT] STATUS ON enviado:", status_msg)


def enviar_sensor():
    sensor_msg = {
        "codesp": CODESPUNI,
        "qtd": 1,
        "counted_at": now_timestamp()
    }
    client.publish(TOPIC_SENSOR, json.dumps(sensor_msg))
    print("[MQTT] Sensor enviado:", sensor_msg)


def loop_sensor():
    while True:
        enviar_sensor()
        time.sleep(5)


if __name__ == "__main__":
    connect()

    enviar_status_on()
    print("▶ Simulador iniciado. Enviando sensores a cada 5s...")

    loop_sensor()
