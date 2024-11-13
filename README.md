# Simulador ESP32 GUI e CLI

Este projeto é uma simulação de um dispositivo ESP32, desenvolvido em Python com uma interface gráfica (GUI) usando `Tkinter` e um script de linha de comando (CLI) para enviar dados para uma API.


![Tela da Interface Gráfica](images/simulador_gui.png)

## Funcionalidades

- **GUI**: Interface gráfica para iniciar/parar a contagem, atualizar a URL da API e o campo `CODESPUNI`.
- **CLI**: Script de linha de comando para definir o status (`on` ou `off`) e enviar diretamente para a API.

## Requisitos

Certifique-se de ter o Python 3.x instalado. Em seguida, instale as bibliotecas necessárias:

```bash
pip install requests
```
## Estrutura dos Scripts

- **GUI**: Interface gráfica para interagir com o dispositivo simulador.
- **CLI**: Script de linha de comando para definir o status diretamente na API.

## Como Usar

### Executando a GUI

- No terminal, navegue até o diretório do projeto.

- Execute o seguinte comando para iniciar a GUI:

```bash
python3 simulador_gui.py
```

### Executando a CLI

Você também pode executar o simulador pela linha de comando para definir o status diretamente.

- **1**: Execute o script simulador_cli.py com o seguinte comando:

```bash
python3 simulador_cli.py --status on
```

- **2**: Para definir o status como off, execute:

```bash
python3 simulador_cli.py --status off
```










