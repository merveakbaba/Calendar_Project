import json
import os
import hashlib

class AuthManager:
    def __init__(self, user_file="users.json"):
        self.user_file = user_file
        if not os.path.exists(self.user_file):
            with open(self.user_file, "w") as f:
                json.dump({}, f)  # boş kullanıcı verisi. dosyanın içi en son {} oluyor.

    def sifre_hashle(self, sifre):
        return hashlib.sha256(sifre.encode()).hexdigest()

    def kullanici_kayit(self, email, sifre):
        with open(self.user_file, "r") as f:
            users = json.load(f)

        if email in users:
            return " Bu e-posta zaten kayıtlı."

        users[email] = {"password": self.sifre_hashle(sifre)}

        with open(self.user_file, "w") as f:
            json.dump(users, f, indent=4)

        return "✅ Kullanıcı başarıyla kaydedildi."

    def kullanici_giris(self, email, sifre):
        with open(self.user_file, "r") as f:
            users = json.load(f)

        if email not in users:
            return " Böyle bir kullanıcı yok."

        if users[email]["password"] != self.sifre_hashle(sifre):
            return " Şifre yanlış."

        return "✅ Giriş başarılı!"

    def kullanicilari_listele(self):
        with open(self.user_file, "r") as f:
            users = json.load(f)
        return list(users.keys())
