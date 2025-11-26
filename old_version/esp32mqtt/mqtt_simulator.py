import json
import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import messagebox
import threading
import time
import datetime

# Variáveis globais para controle do envio de mensagens
sending = False
timer_thread = None

# Função para obter o timestamp atual em segundos
def get_current_timestamp():
    return str(int(time.mktime(datetime.datetime.now().timetuple())))

# Função para enviar mensagens MQTT
def send_mqtt_message(broker_ip, broker_port, topic1, topic2, payload1, payload2):
    client = mqtt.Client()

    def on_connect(client, userdata, flags, rc):
        print(f"Conectado ao broker com código {rc}")
        if topic1:  # Envia o topic1 (device_status) se não for None
            client.publish(topic1, payload1, qos=1)
            print(f"Enviado para {topic1}: {payload1}")
        if topic2:  # Envia o topic2 (data) se não for None
            client.publish(topic2, payload2, qos=1)
            print(f"Enviado para {topic2}: {payload2}")
        client.disconnect()

    def on_publish(client, userdata, mid):
        print(f"Mensagem com id {mid} publicada com sucesso.")

    client.on_connect = on_connect
    client.on_publish = on_publish

    try:
        client.connect(broker_ip, broker_port, 60)
        client.loop_start()
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        messagebox.showerror("Erro", f"Erro ao conectar ao broker: {e}")

# Função para enviar o `device_status` (apenas uma vez) com timestamp atualizado
def send_device_status():
    broker_ip = entry_ip.get()
    broker_port = int(entry_port.get())
    codesp = entry_codesp.get()
    topic1 = f"jws/{codesp}/device_status"
    
    timestamp = get_current_timestamp()  # Obtendo timestamp atual
    payload1 = json.dumps({
        "wifi-fails": 0,
        "macaddr": "10:06:1C:80:27:84",
        "status": "on",
        "codesp": codesp,
        "esp_name": f"esp-linha-x-{codesp}",
        "counted_at": timestamp,
        "repubs": 0,
        "ipaddr": "192.168.200.225"
    })

    # Envia o `device_status` apenas uma vez
    send_mqtt_message(broker_ip, broker_port, topic1, None, payload1, None)
    log_console.insert(tk.END, f"[INFO] Enviado para {topic1}: {payload1}\n")
    log_console.yview(tk.END)

# Função para enviar o `data` periodicamente com o intervalo configurado e timestamp atualizado
def start_sending_data():
    global sending, timer_thread

    # Definindo os tópicos
    broker_ip = entry_ip.get()
    broker_port = int(entry_port.get())
    codesp = entry_codesp.get()
    topic2 = f"jws/{codesp}/data"
    
    # Usando timestamp atualizado
    timestamp = get_current_timestamp()
    payload2 = json.dumps({
        "codesp": codesp,
        "qtd": 1,
        "counted_at": timestamp
    })

    # Inicia o envio contínuo de `data` a cada X segundos
    sending = True

    # Intervalo configurável em segundos (pega o valor do input)
    interval = int(entry_interval.get()) if entry_interval.get().isdigit() else 5  # Valor padrão de 5 segundos

    def send_data_periodically():
        while sending:
            # Atualiza o timestamp a cada envio
            timestamp = get_current_timestamp()
            payload2 = json.dumps({
                "codesp": codesp,
                "qtd": 1,
                "counted_at": timestamp
            })
            
            send_mqtt_message(broker_ip, broker_port, None, topic2, None, payload2)
            log_console.insert(tk.END, f"[INFO] Enviado {topic2}: {payload2}\n")
            log_console.yview(tk.END)
            time.sleep(interval)

    timer_thread = threading.Thread(target=send_data_periodically)
    timer_thread.start()

# Função para parar o envio de mensagens
def stop_sending():
    global sending
    sending = False
    if timer_thread is not None:
        timer_thread.join()  # Espera o thread parar

    log_console.insert(tk.END, "[INFO] Envio interrompido.\n")
    log_console.yview(tk.END)

# Função para pegar os valores da interface e chamar o envio
def on_ligar():
    send_device_status()  # Envia apenas o device_status uma vez

def on_iniciar_envio():
    start_sending_data()  # Inicia o envio do data a cada X segundos

# Criação da interface gráfica
root = tk.Tk()
root.title("Simulador MQTT")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Inputs de IP, porta e código ESP
tk.Label(frame, text="IP do Broker:").grid(row=0, column=0, padx=5, pady=5)
entry_ip = tk.Entry(frame)
entry_ip.grid(row=0, column=1, padx=5, pady=5)
entry_ip.insert(0, "192.168.1.211")  # Valor padrão

tk.Label(frame, text="Porta do Broker:").grid(row=1, column=0, padx=5, pady=5)
entry_port = tk.Entry(frame)
entry_port.grid(row=1, column=1, padx=5, pady=5)
entry_port.insert(0, "1884")  # Valor padrão

tk.Label(frame, text="Código ESP:").grid(row=2, column=0, padx=5, pady=5)
entry_codesp = tk.Entry(frame)
entry_codesp.grid(row=2, column=1, padx=5, pady=5)
entry_codesp.insert(0, "0000000")  # Valor padrão

# Input de Timestamp (não é mais necessário, pois agora pegamos o timestamp atual)
tk.Label(frame, text="Timestamp:").grid(row=3, column=0, padx=5, pady=5)
entry_timestamp = tk.Entry(frame)
entry_timestamp.grid(row=3, column=1, padx=5, pady=5)

# Input de Intervalo para envio do data (em segundos)
tk.Label(frame, text="Intervalo (segundos):").grid(row=4, column=0, padx=5, pady=5)
entry_interval = tk.Entry(frame)
entry_interval.grid(row=4, column=1, padx=5, pady=5)
entry_interval.insert(0, "5")  # Valor padrão de 5 segundos

# Botões para controlar o envio
ligar_button = tk.Button(frame, text="Ligar", command=on_ligar)
ligar_button.grid(row=5, column=0, padx=5, pady=5)

iniciar_button = tk.Button(frame, text="Iniciar Envio", command=on_iniciar_envio)
iniciar_button.grid(row=5, column=1, padx=5, pady=5)

stop_button = tk.Button(frame, text="Parar Envio", command=stop_sending)
stop_button.grid(row=5, column=2, padx=5, pady=5)

# Console de logs
log_console = tk.Text(root, height=10, width=50, bg="black", fg="white", state=tk.DISABLED)
log_console.pack(padx=10, pady=10)

root.mainloop()
