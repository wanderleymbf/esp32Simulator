import requests
import time
import json
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Simula o envio de dados do ESP32")
    parser.add_argument(
        '--status', 
        choices=['on', 'off'], 
        default='off', 
        help="Defina o estado inicial do dispositivo ('on' ou 'off'). O padrão é 'off'."
    )
    return parser.parse_args()


def main():

    args = parse_arguments()
    status = args.status  

    url = "http://127.0.0.1:8000/api/store"
    
    while True:

        counted_at = int(time.time())

        if status == "on":

            sensor_data = {
                "sensor_data": {
                    "CODESP": "123",
                    "QTD": "1",
                    "COUNTED_AT": counted_at
                }
            }
            

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


            response = requests.post(url, json=sensor_data)
            response2 = requests.post(url, json=device_status)
            

            print(f"Status Code: {response.status_code}, Response: {response.text}")
            print(f"Status Code: {response2.status_code}, Response: {response2.text}")
        
        else:

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


            response2 = requests.post(url, json=device_status)
            print(f"Status Code: {response2.status_code}, Response: {response2.text}")
        

        time.sleep(5)

# Executa o script principal
if __name__ == "__main__":
    main()

