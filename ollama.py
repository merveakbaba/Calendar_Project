import requests


class OllamaYoneticisi:
    def __init__(self, url="http://178.233.128.84:12436/api/message"):
        """
        Ollama API'si için bağlantı URL'sini başlatır.

        Args:
            url (str): Ollama API'sinin URL'si.
        """
        self.url = url

    def mesaj_gonder(self, mesaj):
        def mesaj_gonder(self, mesaj):
            """
        Verilen mesajı Ollama API'sine gönderir ve yanıtı döner.

        Args:
            mesaj (str): Gönderilecek mesaj.

        Returns:
            dict or None: API yanıtı JSON formatında döner veya hata durumunda None.
        """
        try:
            response = requests.post(self.url, json={"message": mesaj})
            if response.status_code == 200:
                return response.json()  # Başarılı yanıt
            else:
                print(f"Ollama API hatası: {response.status_code} - {response.text}")
                return None  # Hatalı yanıt
        except Exception as e:
            print(f"Ollama API'ye bağlanılamadı: {e}")
            return None  # Bağlantı hatası


# Örnek kullanım
if __name__ == '__main__':
    ollama_yoneticisi = OllamaYoneticisi()

    while True:
        # Kullanıcıdan komut al
        komut = input("Bir komut girin (çıkmak için 'çık'): ")
        if komut.lower() == 'çık':
            break

        # Komutu Ollama'ya gönder
        cevap = ollama_yoneticisi.mesaj_gonder(komut)

        # Yanıtı kontrol et
        if cevap:
            print("Ollama'nın cevabı:", cevap)
        else:
            print("Ollama'dan bir cevap alınamadı.")