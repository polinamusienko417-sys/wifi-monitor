import tkinter as tk
import os
import time
import subprocess
from tkinter import messagebox
log_file = "wifi_history.txt"
def get_wifi_data():
    try:
        # macOS command to get WiFi info
        process = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I")
        results = process.read()
        ssid = "Відключено"
        signal = 0
        for line in results.split('\n'):
            if " SSID:" in line:
                parts = line.split("SSID: ")
                if len(parts) > 1:
                    ssid = parts[1].strip()
            if "agrCtlRSSI:" in line:
                # Convert RSSI to signal strength (0-100%)
                rssi = int(line.split("agrCtlRSSI: ")[1].strip())
                signal = max(0, min(100, (rssi + 100) * 2))  # Convert to 0-100%
        return ssid, signal
    except:
        return "Помилка", 0
def save_to_file(ssid, signal):
    """Записує дані у файл за допомогою бібліотеки os та вбудованих функцій""" 
    timestamp = time.strftime("%H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Мережа: {ssid} | Сигнал: {signal}%\n")
def update_loop():
    """Головний цикл програми (таймер)"""
    ssid, signal = get_wifi_data()
    label_ssid.config(text=f"SSID: {ssid}")
    label_percent.config(text=f"{signal}%")
    if signal > 75:
        color = "#2ecc71" 
    elif signal > 40:
        color = "#f1c40f"
    else:
        color = "#e74c3c"
    canvas.coords(bar, 5, 5, 5 + (signal * 3.4), 35)
    canvas.itemconfig(bar, fill=color)
    log_box.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] Сигнал: {signal}%\n")
    log_box.see(tk.END)
    if int(time.time()) % 5 == 0:
        save_to_file(ssid, signal)
    if signal < 20 and ssid != "Відключено":
        label_warning.config(text="УВАГА: НИЗЬКИЙ СИГНАЛ!", fg="red")
    else:
        label_warning.config(text="")
    root.after(1000, update_loop)
def open_log_folder():
    """Відкриває папку, де лежить файл з логами"""
    subprocess.Popen(['open', os.getcwd()])
def clear_logs():
    """Видаляє файл логів через OS"""
    if os.path.exists(log_file):
        os.remove(log_file)
        log_box.delete(1.0, tk.END)
        messagebox.showinfo("Система", "Логи очищено!")
root = tk.Tk()
root.title("Wi-Fi Analizer Tool")
root.geometry("400x500")
root.config(bg="#121212")
tk.Label(root,text="Wi-Fi Monitor", font=("Arial", 18, "bold"), bg="#121212", fg="#00FF00").pack(pady=10)
label_ssid = tk.Label(root, text="SSID: Пошук...", font=("Arial", 12), bg="#121212", fg="white")
label_ssid.pack()
label_percent = tk.Label(root, text="0%", font=("Arial", 40, "bold"), bg="#121212", fg="white")
label_percent.pack()
canvas = tk.Canvas(root, width=350, height=40, bg="#333", highlightthickness=0)
canvas.pack(pady=10)
bar = canvas.create_rectangle(5, 5, 5, 35, fill="green", outline="")
label_warning = tk.Label(root, text="", font=("Arial", 10, "bold"), bg="#121212")
label_warning.pack()
tk.Label(root, text="Історія сигналу:", bg="#121212", fg="gray").pack()
log_box = tk.Text(root, width=40, height=8,bg="#222", fg="#00FF00", font=("Consolas", 9))
log_box.pack(pady=5)
btn_frame = tk.Frame(root, bg="#121212")
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Файли", command=open_log_folder, width=12).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Очистити", command=clear_logs, width=12).grid(row=0, column=1, padx=5)
update_loop()
root.mainloop()