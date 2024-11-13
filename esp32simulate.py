import requests
import time
import json
import argparse

# Função para processar os argumentos de linha de comando
def parse_arguments():
    parser = argparse.ArgumentParser(description="Simula o envio de dados do ESP32")
    parser.add_argument(
        '--status', 
        choices=['on', 'off'], 
        default='off', 
        help="Defina o estado inicial do dispositivo ('on' ou 'off'). O padrão é 'off'."
    )
    return parser.parse_args()

# Função principal
def main():
    # Obtém os argumentos da linha de comando
    args = parse_arguments()
    status = args.status  # O estado inicial do dispositivo será passado aqui

    url = "http://127.0.0.1:8000/api/store"
    
    while True:
        # Obtém o timestamp atual
        counted_at = int(time.time())

        if status == "on":
            # Dados do sensor quando em operação
            sensor_data = {
                "sensor_data": {
                    "CODESP": "123",
                    "QTD": "1",
                    "COUNTED_AT": counted_at
                }
            }
            
            # Dados do dispositivo com status "on"
            device_status = {
                "device_status": {
                    "NOME": "esp2",
                    "IPADRESS": "192.168.1.10",
                    "COUNTED_AT": counted_at,
                    "MACADRESS": "10:C9:22:39:16:1C",
                    "CODESPUNI": "123",
                    "STATUS": status
                }
            }

            # Envia ambas as solicitações POST para simular o dispositivo funcionando
            response = requests.post(url, json=sensor_data)
            response2 = requests.post(url, json=device_status)
            
            # Exibe a resposta da API
            print(f"Status Code: {response.status_code}, Response: {response.text}")
            print(f"Status Code: {response2.status_code}, Response: {response2.text}")
        
        else:
            # Configura o status para "off" e envia apenas device_status
            device_status = {
                "device_status": {
                    "NOME": "esp2",
                    "IPADRESS": "192.168.1.10",
                    "COUNTED_AT": counted_at,
                    "MACADRESS": "10:C9:22:39:16:1C",
                    "CODESPUNI": "123",
                    "STATUS": status
                }
            }

            # Envia apenas o status do dispositivo como "off"
            response2 = requests.post(url, json=device_status)
            print(f"Status Code: {response2.status_code}, Response: {response2.text}")
        
        # Aguarda 5 segundos antes do próximo envio
        time.sleep(5)

# Executa o script principal
if __name__ == "__main__":
    main()

