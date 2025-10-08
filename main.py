import configparser
from ollama_manager import OllamaYoneticisi
from calendar_manager import TakvimYoneticisi
from prompt import generate_prompt
from auth_manager import AuthManager


def main():
    auth = AuthManager()  # Kullanıcı yönetimi
   
    while True:
        print("\n1. Giriş Yap")
        print("2. Kayıt Ol")
        print("3. Çıkış")
        secim = input("Seçiminiz (1-3): ").strip()

        if secim == "1":
            email = input("E-posta: ").strip()
            sifre = input("Şifre: ").strip()
            result = auth.kullanici_giris(email, sifre)
            print(result)
            if "başarılı" in result:
                break

        elif secim == "2":
            email = input("E-posta: ").strip()
            sifre = input("Şifre: ").strip()
            print(auth.kullanici_kayit(email, sifre))

        elif secim == "3":
            print("Program kapandı.")
            return
        else:
            print("1-3 arasında bir rakam girin.")

    # Giriş başarılı → kullanıcının token ve credential dosyaları
    config = configparser.ConfigParser()
    config.read('secret.cfg')
    user_credential_file = config['google']['user_credential_file']
    token_file = f"token_{email}.json"  # kullanıcıya özel token dosyası

    takvim = TakvimYoneticisi(user_credential_file, token_file)
    ollama_yoneticisi = OllamaYoneticisi()

    while True:
        print("\n--- Menü ---")
        print("1. Randevu Ekle")
        print("2. Randevuları Listele")
        print("3. Randevu Sil")
        print("4. Randevu Güncelle")
        print("5. Doğal Dil Komutu (AI ile)")
        print("6. Çıkış")

        secim = input("Seçiminiz (1-6): ").strip()

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
            cevap = ollama_yoneticisi.mesaj_gonder(komut)
            print("Ollama's response:", cevap)

            # AI’den randevu ekleme talebi varsa
            if "add" in komut.lower():
                try:
                    details = cevap.split("|")
                    if len(details) == 5:
                        title, location, description, start_time, end_time = [info.strip() for info in details]
                        takvim.randevu_ekle(title, location, description, start_time, end_time)
                    else:
                        print("AI’den eksik bilgi geldi, lütfen manuel girin.")
                except Exception as e:
                    print("Hata oluştu:", e)

        elif secim == '6':
            print("Program kapandı.")
            break
        else:
            print("1-6 arasında bir rakam girin.")


if __name__ == '__main__':
    main()
