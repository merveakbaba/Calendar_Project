import requests
import configparser
import json

from prompt import generate_prompt  #prompt oluşturma fonksiyonunu içe aktarma

class OllamaYoneticisi:
    def __init__(self, config_file="secret.cfg"): #config dosyası parametre olarak alınabiliyor,böylece esneklik sağlandı
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.url = self.config["ollama"]["url"]  #url yi alma

    def mesaj_gonder(self, mesaj):
        prompt = generate_prompt(mesaj)  # kullanıcinın mesajına uygun promt yazma
        payload = { # api isteği için model ve parametre kelendi
            "model": "deepseek-r1:7b",  # modeli belirtme
            "prompt": prompt,  #  gönderilecek mesaj
            "parameters": {
                "max_tokens": 128,  #cevabın max uzunlu
                #"temperature": 0.7 # cevabın çeşitliliğinin kontrol etmek için (gerekli mi bilmiyorum)
            }
        }
        headers = {"Content-Type": "application/json"}  # JSON formatında veri gönderiliyor(header eklendi)

        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=10)  # apiye istekte bulunma, timeout eklendi api bi sure yanıt vermezse sonlanır

            response.raise_for_status()  #HTTP hatası olup olmadığını kontrol etme

            response_lines = response.text.strip().split("\n")  # cevabi işeyebilemsi için parça parça bölmek gerekiyor(bazı apiler jsonu birden fazla satırda döndürebiliyor)
            tam_cevap = ""

            for line in response_lines:
                try:
                    json_data = json.loads(line)  # JSON formatındaki her satırı ayrıştırma işlemi
                    tam_cevap += json_data.get("response", "")  #respomse bilgisini alma
                except json.JSONDecodeError:
                    continue  # json hata verirse atla.

            return tam_cevap.strip() if tam_cevap else "Ollama'dan beklenen formatta yanıt alınamadı"

        except requests.exceptions.Timeout:
            return "Bağlantı zaman aşımına uğradı."  #cevap gelmezse hata döndür
        except requests.exceptions.RequestException as e:
            return f"Bir hata oluştu: {e}"  #HTTP hataları için hata mesajı döndür
        except ValueError as ve:
            return f"Yanıtı ayrıştırırken bir hata oluştu: {ve}"  #ayrıştırma hatası için hata yönetimi eklendi
