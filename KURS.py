import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("kurs_qabul.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS qabul (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ism TEXT NOT NULL,
    familiya TEXT NOT NULL,
    telefon TEXT NOT NULL,
    kurs_nomi TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS fanlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nomi TEXT NOT NULL
)
''')
conn.commit()

def bazaga_saqlash(ism, familiya, telefon, kurs_nomi):
    cursor.execute("INSERT INTO qabul (ism, familiya, telefon, kurs_nomi) VALUES (?, ?, ?, ?)",
                   (ism, familiya, telefon, kurs_nomi))
    conn.commit()

def fanni_bazaga_qosh(nomi):
    cursor.execute("INSERT INTO fanlar (nomi) VALUES (?)", (nomi,))
    conn.commit()

def malumotni_olish():
    cursor.execute("SELECT ism, familiya, telefon, kurs_nomi FROM qabul")
    return cursor.fetchall()

root = tk.Tk()
root.title("Kursga O'quvchi Qabul")

fan_label = tk.Label(root, text="Qaysi fanlarni tanlaysiz?", font=("Arial", 12))
fan_label.pack(pady=5)

fan_frame = tk.Frame(root)
fan_frame.pack(pady=5)

fan_entries = []

def fan_qoshish():
    fan_entry = tk.Entry(fan_frame, width=40, font=("Arial", 10))
    fan_entry.pack(pady=2)
    fan_entries.append(fan_entry)

    def saqlash_va_yangilash():
        nomi = fan_entry.get().strip()
        if nomi:
            fanni_bazaga_qosh(nomi)
            messagebox.showinfo("Muvaffaqiyatli", f"Fan '{nomi}' bazaga qo'shildi!")
            fan_entry.delete(0, tk.END)

    save_button = tk.Button(fan_frame, text="Saqlash", command=saqlash_va_yangilash, bg="#FFD700", fg="black", font=("Arial", 8))
    save_button.pack(pady=2)

fan_qoshish()
add_fan_button = tk.Button(root, text="Fan qo'shish", command=fan_qoshish, bg="#FFD700", fg="black", font=("Arial", 10, "bold"))
add_fan_button.pack(pady=5)

ism_label = tk.Label(root, text="Ismingiz:", font=("Arial", 12))
ism_label.pack(pady=5)
ism_entry = tk.Entry(root, width=40, font=("Arial", 10))
ism_entry.pack(pady=5)

familiya_label = tk.Label(root, text="Familiyangiz:", font=("Arial", 12))
familiya_label.pack(pady=5)
familiya_entry = tk.Entry(root, width=40, font=("Arial", 10))
familiya_entry.pack(pady=5)

telefon_label = tk.Label(root, text="Telefon raqamingiz:", font=("Arial", 12))
telefon_label.pack(pady=5)
telefon_entry = tk.Entry(root, width=40, font=("Arial", 10))
telefon_entry.pack(pady=5)

def submit():
    ism = ism_entry.get().strip()
    familiya = familiya_entry.get().strip()
    telefon = telefon_entry.get().strip()
    kurs_nomi = ", ".join([entry.get().strip() for entry in fan_entries if entry.get().strip()])

    if not (ism and familiya and telefon and kurs_nomi):
        messagebox.showerror("Xatolik", "Iltimos, barcha maydonlarni to'ldiring!")
        return

    bazaga_saqlash(ism, familiya, telefon, kurs_nomi)
    messagebox.showinfo("Muvaffaqiyatli", f"{ism} {familiya} kursga muvaffaqiyatli yozildi!")

    ism_entry.delete(0, tk.END)
    familiya_entry.delete(0, tk.END)
    telefon_entry.delete(0, tk.END)
    for entry in fan_entries:
        entry.delete(0, tk.END)

    jadvalni_yangilash()

table_frame = tk.Frame(root)
table_frame.pack(pady=20)

columns = ("Ism", "Familiya", "Telefon", "Kurs")
table = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120, anchor="center")

table.pack(fill=tk.BOTH, expand=True)

def jadvalni_yangilash():
    for row in table.get_children():
        table.delete(row)
    for ism, familiya, telefon, kurs_nomi in malumotni_olish():
        table.insert("", tk.END, values=(ism, familiya, telefon, kurs_nomi))
yozilish_button = tk.Button(root, text="Kursga Yozilish", command=submit, bg="#32CD32", fg="white", font=("Arial", 12, "bold"))
yozilish_button.pack(pady=10)
jadvalni_yangilash()
root.mainloop()
conn.close()
