#model ve manager birleşimi deneme

import requests  # http istekleri için kütüphane
import configparser  # cfg dosyalarını okumak için kütüphane

# cfg dosyasını oku
config = configparser.ConfigParser()
config.read("secret.cfg")

class OllamaYoneticisi:
    def __init__(self):
        self.url = config["ollama"]["url"]

    def mesaj_gonder(self, mesaj):  # cevabı json formatında döner
        try:
            response = requests.post(self.url, json={"message": mesaj})
            if response.status_code == 200:
                return response.json()
            else:
                return f"Ollama API hatası: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Ollama API'ye bağlanılamadı: {e}"

# örnek
def main():
    url = "http://178.233.128.84:12436/api/models"
    payload = {
        "model": "deepseek-r1:7b",
        "prompt": "saat kaç",
        "parameters": {
            "max_tokens": 128,
            "temperature": 0.7
        }
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)  # 10 saniyelik zaman aşımı
        response.raise_for_status()  # http hatalarını kontrol etme
        print("Yanıt:", response.json())
    except requests.exceptions.Timeout:
        print("Bağlantı zaman aşımına uğradı.")
    except requests.exceptions.RequestException as e:
        print("Bir hata oluştu:", e)

if __name__ == "__main__":
    ollama_manager = OllamaYoneticisi()
    mesaj = "test mesajı."
    print(ollama_manager.mesaj_gonder(mesaj))

    main()
