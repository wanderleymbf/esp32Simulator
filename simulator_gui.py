import requests
import time
import threading
import tkinter as tk
from tkinter import scrolledtext

default_url = "http://127.0.0.1:8000/api/store"
url = default_url
default_codeespuni = "123"
codeespuni = default_codeespuni

status = "off"
is_running = False  

def send_data():
    global is_running
    while is_running:
        counted_at = int(time.time())

        if status == "on":
            sensor_data = {
                "sensor_data": {
                    "CODESP": codeespuni,
                    "QTD": "1",
                    "COUNTED_AT": counted_at
                }
            }

            device_status = {
                "device_status": {
                    "NOME": "esp2",
                    "IPADRESS": "10.0.0.1",
                    "COUNTED_AT": counted_at,
                    "MACADRESS": "00:00:00:00:00:00",
                    "CODESPUNI": codeespuni,
                    "STATUS": status
                }
            }

            response = requests.post(url, json=sensor_data)
            response2 = requests.post(url, json=device_status)

            console_output(f"Sensor Data - Status Code: {response.status_code}, Response: {response.text}")
            console_output(f"Device Status - Status Code: {response2.status_code}, Response: {response2.text}")
        
        else:
            device_status = {
                "device_status": {
                    "NOME": "esp2",
                    "IPADRESS": "10.0.0.1",
                    "COUNTED_AT": counted_at,
                    "MACADRESS": "00:00:00:00:00:00",
                    "CODESPUNI": codeespuni,
                    "STATUS": status
                }
            }
            response2 = requests.post(url, json=device_status)
            console_output(f"Device Status - Status Code: {response2.status_code}, Response: {response2.text}")
        
        time.sleep(5)

def iniciar_contagem():
    global status, is_running
    status = "on"
    is_running = True
    console_output("Iniciando contagem...")
    threading.Thread(target=send_data, daemon=True).start()

def parar_linha():
    global status, is_running
    status = "off"
    is_running = False
    console_output("Parando contagem... Enviando status off para a API.")

    counted_at = int(time.time())
    device_status = {
        "device_status": {
            "NOME": "esp2",
            "IPADRESS": "10.0.0.1",
            "COUNTED_AT": counted_at,
            "MACADRESS": "00:00:00:00:00:00",
            "CODESPUNI": codeespuni,
            "STATUS": status
        }
    }
    response2 = requests.post(url, json=device_status)
    console_output(f"Device Status - Status Code: {response2.status_code}, Response: {response2.text}")

def atualizar_url():
    global url
    new_url = url_entry.get()
    if new_url:
        url = new_url
        console_output(f"URL da API atualizada para: {url}")
    else:
        console_output("URL inválida! Mantendo a URL padrão.")

def atualizar_codeespuni():
    global codeespuni
    new_codeespuni = codeespuni_entry.get()
    if new_codeespuni:
        codeespuni = new_codeespuni
        console_output(f"CODESPUNI atualizado para: {codeespuni}")
    else:
        console_output("CODESPUNI inválido! Mantendo o valor padrão.")

def console_output(message):
    console.insert(tk.END, message + "\n")
    console.see(tk.END)

button_style = {
    'font': ('Arial', 10, 'bold'),
    'bg': '#4CAF50',
    'fg': 'white',
    'activebackground': '#45a049',
    'activeforeground': 'white',
    'relief': 'flat',
    'bd': 4,
    'padx': 8,
    'pady': 6,
    'width': 12
}

red_button_style = {
    **button_style,
    'bg': '#e53935',
    'activebackground': '#d32f2f'
}

entry_style = {
    'font': ('Arial', 12),
    'width': 30,
    'bd': 3,
    'relief': 'groove'
}

root = tk.Tk()
root.title("Simulador ESP32")
root.geometry("550x500")
root.config(bg="#f0f0f0")
root.resizable(False, False)

title = tk.Label(root, text="Simulador ESP32", font=("Arial", 16, 'bold'), bg="#f0f0f0", fg="#333333")
title.pack(pady=20)


url_frame = tk.Frame(root, bg="#f0f0f0")
url_frame.pack(pady=5)

url_label = tk.Label(url_frame, text="URL da API:", font=("Arial", 10), bg="#f0f0f0", fg="#333333")
url_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
url_entry = tk.Entry(url_frame, **entry_style)
url_entry.insert(0, default_url)
url_entry.grid(row=0, column=1, padx=5, pady=5)
update_url_button = tk.Button(url_frame, text="Salvar", command=atualizar_url, **button_style)
update_url_button.grid(row=0, column=2, padx=5, pady=5)

codeespuni_frame = tk.Frame(root, bg="#f0f0f0")
codeespuni_frame.pack(pady=5)

codeespuni_label = tk.Label(codeespuni_frame, text="CODESPUNI:", font=("Arial", 10), bg="#f0f0f0", fg="#333333")
codeespuni_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
codeespuni_entry = tk.Entry(codeespuni_frame, **entry_style)
codeespuni_entry.insert(0, default_codeespuni)
codeespuni_entry.grid(row=0, column=1, padx=5, pady=5)
update_codeespuni_button = tk.Button(codeespuni_frame, text="Salvar", command=atualizar_codeespuni, **button_style)
update_codeespuni_button.grid(row=0, column=2, padx=5, pady=5)


action_button_frame = tk.Frame(root, bg="#f0f0f0")
action_button_frame.pack(pady=15)

start_button = tk.Button(action_button_frame, text="Iniciar Contagem", command=iniciar_contagem, **button_style)
start_button.grid(row=0, column=0, padx=5)
stop_button = tk.Button(action_button_frame, text="Parar Linha", command=parar_linha, **red_button_style)
stop_button.grid(row=0, column=1, padx=5)

console = scrolledtext.ScrolledText(root, width=60, height=10, bg="black", fg="white", wrap=tk.WORD, font=("Courier", 10))
console.pack(pady=10)

root.mainloop()
	
