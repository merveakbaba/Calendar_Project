#kullanıcı arayüzü
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from calendar_manager import TakvimYoneticisi

class AppointmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Randevu Yönetimi")
        self.calendar_manager = TakvimYoneticisi()

        # Başlık
        self.label = ttk.Label(root, text="Randevu Ekle", font=("Arial", 16))
        self.label.grid(row=0, column=1, pady=20)

        # Başlık input
        self.summary_label = ttk.Label(root, text="Başlık:")
        self.summary_label.grid(row=1, column=0, sticky="e", padx=10)
        self.summary_entry = ttk.Entry(root)
        self.summary_entry.grid(row=1, column=1)

        # Yer input
        self.location_label = ttk.Label(root, text="Yer:")
        self.location_label.grid(row=2, column=0, sticky="e", padx=10)
        self.location_entry = ttk.Entry(root)
        self.location_entry.grid(row=2, column=1)

        # Açıklama input
        self.description_label = ttk.Label(root, text="Açıklama:")
        self.description_label.grid(row=3, column=0, sticky="e", padx=10)
        self.description_entry = ttk.Entry(root)
        self.description_entry.grid(row=3, column=1)

        # Tarih seçici
        self.start_date_label = ttk.Label(root, text="Başlangıç Tarihi:")
        self.start_date_label.grid(row=4, column=0, sticky="e", padx=10)
        self.start_date_entry = Calendar(root)
        self.start_date_entry.grid(row=4, column=1, pady=5)

        # Başlangıç saati seçici
        self.start_time_label = ttk.Label(root, text="Başlangıç Saati:")
        self.start_time_label.grid(row=5, column=0, sticky="e", padx=10)
        self.start_hour = ttk.Spinbox(root, from_=0, to=23, width=5, format="%02.0f")
        self.start_hour.grid(row=5, column=1, pady=5, sticky="w", padx=10)
        self.start_minute = ttk.Spinbox(root, from_=0, to=59, width=5, format="%02.0f")
        self.start_minute.grid(row=5, column=1, pady=5, sticky="e", padx=10)

        # Bitiş Tarihi
        self.end_date_label = ttk.Label(root, text="Bitiş Tarihi:")
        self.end_date_label.grid(row=6, column=0, sticky="e", padx=10)
        self.end_date_entry = Calendar(root)
        self.end_date_entry.grid(row=6, column=1, pady=5)

        # Bitiş saati
        self.end_time_label = ttk.Label(root, text="Bitiş Saati:")
        self.end_time_label.grid(row=7, column=0, sticky="e", padx=10)
        self.end_hour = ttk.Spinbox(root, from_=0, to=23, width=5, format="%02.0f")
        self.end_hour.grid(row=7, column=1, pady=5, sticky="w", padx=10)
        self.end_minute = ttk.Spinbox(root, from_=0, to=59, width=5, format="%02.0f")
        self.end_minute.grid(row=7, column=1, pady=5, sticky="e", padx=10)

        # Randevu ekleme butonu
        self.add_button = ttk.Button(root, text="Randevu Ekle", command=self.add_event)
        self.add_button.grid(row=8, column=0, columnspan=2, pady=20)

    def add_event(self):
        summary = self.summary_entry.get()
        location = self.location_entry.get()
        description = self.description_entry.get()

        # Başlangıç ve bitiş tarihleri ile saatleri
        start_date = self.start_date_entry.get_date()
        start_time = f"{self.start_hour.get()}:{self.start_minute.get()}"
        end_date = self.end_date_entry.get_date()
        end_time = f"{self.end_hour.get()}:{self.end_minute.get()}"

        # Tarih ve saatleri birleştirerek datetime formatına dönüştürme işlmei
        start_datetime = f"{start_date} {start_time}"
        end_datetime = f"{end_date} {end_time}"

        # Randevu ekleme işlemi
        self.calendar_manager.add_event(summary, location, description, start_datetime, end_datetime)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentApp(root)
    root.mainloop()
