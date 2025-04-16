import requests
import json
import configparser

# Config dosyasını oku
config = configparser.ConfigParser()
config.read("secret.cfg")

# Sunucu adresini config dosyasından al
url = config["ollama"]["url"]

payload = {
    "model": "deepseek-r1:7b",
    "prompt": "What is the capital of France?",
    "parameters": {
        "max_tokens": 128,
        "temperature": 0.7
    }
}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers, timeout=10)  # 10 saniye zaman aşımı
    response.raise_for_status()
    print("Yanıt:", response.text)
except requests.exceptions.Timeout:
    print("Bağlantı zaman aşımına uğradı.")
except requests.exceptions.RequestException as e:
    print("Bir hata oluştu:", e)