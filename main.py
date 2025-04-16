import configparser
from ollama_manager import OllamaYoneticisi
from calendar_manager import TakvimYoneticisi
from prompt import generate_prompt


def main():
    # Config dosyasını oku
    config = configparser.ConfigParser()
    config.read('secret.cfg')
    user_credential_file = config['google']['user_credential_file']
    token_file = config['google']['token_file']

    # Yöneticileri oluştur
    takvim = TakvimYoneticisi(user_credential_file, token_file)
    ollama_yoneticisi = OllamaYoneticisi()

    while True:
        print("\n--- Randevu Yönetim Sistemi ---")
        print("1. Randevu Ekle")
        print("2. Randevuları Listele")
        print("3. Randevu Sil")
        print("4. Randevu Güncelle")
        print("5. Doğal Dil Komutu (AI ile)")
        print("6. Çıkış")

        secim = input("Lütfen bir seçim yapın (1-6): ").strip()

        if secim == '1':
            baslik = input("Randevu Başlığı: ").strip()
            yer = input("Yer: ").strip()
            aciklama = input("Açıklama: ").strip()
            baslangic = input("Başlangıç Zamanı (YYYY-MM-DDTHH:MM:SS): ").strip()
            bitis = input("Bitiş Zamanı (YYYY-MM-DDTHH:MM:SS): ").strip()
            takvim.randevu_ekle(baslik, yer, aciklama, baslangic, bitis)

        elif secim == '2':
            takvim.randevulari_listele()

        elif secim == '3':
            etkinlik_id = input("Silmek istediğiniz randevunun ID'si: ").strip()
            takvim.randevu_sil(etkinlik_id)

        elif secim == '4':
            etkinlik_id = input("Güncellemek istediğiniz randevunun ID'si: ").strip()
            baslik = input("Yeni Başlık (boş bırakabilirsiniz): ").strip() or None
            aciklama = input("Yeni Açıklama (boş bırakabilirsiniz): ").strip() or None
            baslangic = input("Yeni Başlangıç Zamanı (YYYY-MM-DDTHH:MM:SS, boş bırakabilirsiniz): ").strip() or None
            bitis = input("Yeni Bitiş Zamanı (YYYY-MM-DDTHH:MM:SS, boş bırakabilirsiniz): ").strip() or None
            takvim.randevu_guncelle(etkinlik_id, baslik, aciklama, baslangic, bitis)

        elif secim == '5':
            komut = input("Doğal dilde bir komut girin: ").strip()
            prompt = generate_prompt(komut)  # Generate prompt function call
            cevap = ollama_yoneticisi.mesaj_gonder(prompt)
            print("Ollama's response:", cevap)

            # If an appointment addition is requested, extract details and add the appointment
            if "add" in komut.lower():
                try:
                    details = cevap.split("|")  # Extract details from response
                    if len(details) == 5:
                        title, location, description, start_time, end_time = [info.strip() for info in details]
                        takvim.randevu_ekle(title, location, description, start_time, end_time)
                    else:
                        print("Incomplete information received from AI. Please try manual input.")
                except Exception as e:
                    print("An error occurred:", e)

        elif secim == '6':
            print("Exiting the program... Goodbye!")
            break

        else:
            print("Invalid selection. Please enter a number between 1 and 6.")


if __name__ == '__main__':
    main()
"""Ollama’nın gerçekten fonksiyonu çağırması için entegrasyon kodunu kontrol etmelisin (örneğin, doğal dil
 girişini Python çağrılarına çevirmesi için özel bir exec() veya fonksiyon çağırma mekanizması var mı?)."""