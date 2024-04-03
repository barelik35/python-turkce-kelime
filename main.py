import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
import random
import time
import requests
import datetime


current_canvas = None
last_click_time = 0
previous_keyword = None

def get_keyword_interest(keyword, country_code='TR'):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=30)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    pytrends = TrendReq(hl='tr-TR', tz=360)
    pytrends.build_payload(kw_list=[keyword], geo=country_code, timeframe=f'{start_date_str} {end_date_str}')
    interest_over_time_df = pytrends.interest_over_time()
    return interest_over_time_df

def plot_graph(keyword, interest_over_time_df):
    plt.figure(figsize=(8, 4))
    plt.plot(interest_over_time_df.index, interest_over_time_df[keyword], marker='o', color='b')
    plt.title(f"İlgiye Göre Zaman Grafiği '{keyword}'")
    plt.xlabel('Zaman')
    plt.ylabel('İlgi')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

def show_graph():
    global current_canvas, last_click_time, previous_keyword
    
    current_time = time.time()
    
    if current_time - last_click_time < 1:
        messagebox.showwarning("Uyarı", "Lütfen 1 saniye bekleyin.")
        return
    
    last_click_time = current_time

    if current_canvas:
        current_canvas.get_tk_widget().pack_forget()  

    url = "https://slowy.com.tr/domaintesterprogram/randomwordtr.php"

    response = requests.get(url)

    if response.status_code == 200:
        trending_keywords = response.text.split(',')
    else:
        messagebox.showwarning("Uyarı", "Anahtar Kelime Bulunamadı. Lütfen tekrar deneyin.")
        return

    if previous_keyword in trending_keywords:
        trending_keywords.remove(previous_keyword)
    
    if trending_keywords:
        keyword = random.choice(trending_keywords)
        previous_keyword = keyword
        
        interest_over_time_df = get_keyword_interest(keyword)
        
        if interest_over_time_df is not None and keyword in interest_over_time_df.columns:
            plot_graph(keyword, interest_over_time_df)
            
            canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            current_canvas = canvas  
        else:
            show_graph()
    else:
        messagebox.showwarning("Uyarı", "Anahtar Kelime Bulunmadı.")

root = tk.Tk()
root.title("Google Trends Grafiği")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Anahtar Kelime Çek:")
label.pack(side=tk.LEFT)

button = tk.Button(frame, text="Kelime Çek", command=show_graph)
button.pack(side=tk.LEFT)

root.mainloop()
