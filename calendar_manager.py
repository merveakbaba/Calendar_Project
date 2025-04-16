from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']

class TakvimYoneticisi:
    def __init__(self, user_credential_file='credentials.json', token_file='token.json'):
        self.service = self.kimlik_dogrula(user_credential_file, token_file)

    def kimlik_dogrula(self, user_credential_file, token_file):
        creds = None
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(user_credential_file, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_file, 'w') as token_dosyasi:
                token_dosyasi.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)

    # Randevu ekleme
    def randevu_ekle(self, baslik, yer, aciklama, baslangic, bitis):
        try:
            etkinlik = {
                'summary': baslik,
                'location': yer,
                'description': aciklama,
                'start': {'dateTime': baslangic, 'timeZone': 'Europe/Istanbul'},
                'end': {'dateTime': bitis, 'timeZone': 'Europe/Istanbul'},
            }
            sonuc = self.service.events().insert(calendarId='primary', body=etkinlik).execute()
            print('Randevu eklendi: ', sonuc.get('htmlLink'))
        except Exception as e:
            print('Randevu eklenirken bir hata oldu:', e)

    def randevulari_listele(self):
        try:
            simdi = datetime.datetime.utcnow().isoformat() + 'Z'
            sonuc = self.service.events().list(calendarId='primary', timeMin=simdi, singleEvents=True,
                                               orderBy='startTime').execute()
            etkinlikler = sonuc.get('items', [])
            if not etkinlikler:
                print('Randevu bulunamadı.')
                return

            for etkinlik in etkinlikler:
                baslangic = etkinlik['start'].get('dateTime', etkinlik['start'].get('date'))
                print(baslangic, ':', etkinlik['summary'])
        except Exception as e:
            print('Randevular listelenirken bir hata oldu:', e)

    def randevu_sil(self, etkinlik_id):
        try:
            self.service.events().delete(calendarId='primary', eventId=etkinlik_id).execute()
            print('Randevu silindi.')
        except Exception as e:
            print('Randevu silinirken bir hata oldu:', e)

    def randevu_guncelle(self, etkinlik_id, baslik=None, aciklama=None, baslangic=None, bitis=None):
        try:
            etkinlik = self.service.events().get(calendarId='primary', eventId=etkinlik_id).execute()
            if baslik:
                etkinlik['summary'] = baslik
            if aciklama:
                etkinlik['description'] = aciklama
            if baslangic:
                etkinlik['start']['dateTime'] = baslangic
            if bitis:
                etkinlik['end']['dateTime'] = bitis
            sonuc = self.service.events().update(calendarId='primary', eventId=etkinlik_id, body=etkinlik).execute()
            print('Randevu güncellendi: ', sonuc.get('htmlLink'))
        except Exception as e:
            print('Randevu güncellenirken bir hata oldu:', e)