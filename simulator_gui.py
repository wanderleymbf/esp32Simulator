import time
import threading
import tkinter as tk
from tkinter import scrolledtext
import paho.mqtt.client as mqtt
import json

# ================================================
# CONFIGURAÇÕES
# ================================================
default_codeespuni = "123"
codeespuni = default_codeespuni

MQTT_BROKER = "192.168.1.212"
MQTT_PORT = 1883

MQTT_TOPIC_SENSOR = "jws/123/data"
MQTT_TOPIC_STATUS = "jws/123/device_status"

client = mqtt.Client()

status = "off"
is_running = False


# ================================================
# MQTT
# ================================================
def connect_mqtt():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        console_output(f"Conectado ao broker MQTT {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        console_output(f"Erro ao conectar MQTT: {e}")


# ================================================
# ENVIA O SENSOR A CADA 5s
# ================================================
def loop_sensor():
    global is_running, status

    connect_mqtt()

    while is_running:
        counted_at = int(time.time())

        if status == "on":
            sensor_data = {
                "codesp": codeespuni,
                "qtd": 1,
                "counted_at": counted_at
            }

            client.publish(MQTT_TOPIC_SENSOR, json.dumps(sensor_data))
            console_output(f"[MQTT] Sensor enviado: {sensor_data}")

        time.sleep(5)


# ================================================
# INICIAR — envia STATUS ON apenas uma vez
# ================================================
def iniciar_contagem():
    global status, is_running
    status = "on"
    is_running = True

    console_output("▶ Iniciando contagem... Enviando STATUS ON")

    connect_mqtt()

    counted_at = int(time.time())

    device_status = {
        "codesp": codeespuni,
        "ipaddr": "10.0.0.1",
        "macaddr": "00:00:00:00:00:00",
        "status": "on",
        "esp_name": "esp2",
        "counted_at": counted_at
    }

    client.publish(MQTT_TOPIC_STATUS, json.dumps(device_status))
    console_output(f"[MQTT] STATUS ON enviado: {device_status}")

    # inicia thread que envia sensor
    threading.Thread(target=loop_sensor, daemon=True).start()


# ================================================
# PARAR — envia STATUS OFF apenas uma vez
# ================================================
def parar_linha():
    global status, is_running
    status = "off"
    is_running = False

    console_output("⛔ Parando linha... enviando STATUS OFF")

    connect_mqtt()
    counted_at = int(time.time())

    device_status = {
        "codesp": codeespuni,
        "ipaddr": "10.0.0.1",
        "macaddr": "00:00:00:00:00:00",
        "status": "off",
        "esp_name": "esp2",
        "counted_at": counted_at
    }

    client.publish(MQTT_TOPIC_STATUS, json.dumps(device_status))
    console_output("[MQTT] STATUS OFF enviado")


# ================================================
# UI
# ================================================
def atualizar_codeespuni():
    global codeespuni
    new_codeespuni = codeespuni_entry.get()
    if new_codeespuni:
        codeespuni = new_codeespuni
        console_output(f"CODESPUNI atualizado para: {codeespuni}")
    else:
        console_output("CODESPUNI inválido!")


def console_output(message):
    console.insert(tk.END, message + "\n")
    console.see(tk.END)


root = tk.Tk()
root.title("Simulador ESP32 - MQTT")
root.geometry("550x500")
root.config(bg="#f0f0f0")
root.resizable(False, False)

title = tk.Label(root, text="Simulador ESP32 - MQTT", font=("Arial", 16, 'bold'), bg="#f0f0f0")
title.pack(pady=20)

codeespuni_frame = tk.Frame(root, bg="#f0f0f0")
codeespuni_frame.pack(pady=5)

tk.Label(codeespuni_frame, text="CODESPUNI:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
codeespuni_entry = tk.Entry(codeespuni_frame, width=30)
codeespuni_entry.insert(0, default_codeespuni)
codeespuni_entry.grid(row=0, column=1, padx=5)
tk.Button(codeespuni_frame, text="Salvar", command=atualizar_codeespuni).grid(row=0, column=2)

action_frame = tk.Frame(root, bg="#f0f0f0")
action_frame.pack(pady=20)

tk.Button(action_frame, text="Iniciar Contagem", command=iniciar_contagem).grid(row=0, column=0, padx=10)
tk.Button(action_frame, text="Parar Linha", command=parar_linha).grid(row=0, column=1, padx=10)

console = scrolledtext.ScrolledText(root, width=60, height=10, bg="black", fg="white")
console.pack(pady=20)

root.mainloop()
