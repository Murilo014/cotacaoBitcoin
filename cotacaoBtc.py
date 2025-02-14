import tkinter as tk
from tkinter import ttk
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import time

# Adicionando um cache para as requisições
# Variáveis para cache
CACHE_DURATION = 60
last_api_call_time = 0
cached_price = None
cached_historical_data = None


# Função para obter a cotação atual do Bitcoin
def get_bitcoin_price():
    global last_api_call_time, cached_price

    if time.time() - last_api_call_time < CACHE_DURATION and cached_price is not None:
        return cached_price
    
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        response.raise_for_status() # Verifica se a requisição foi bem sucedida 
        data = response.json()
        if 'bitcoin' in data and 'usd' in data['bitcoin']:
            cached_price = data['bitcoin'] ['usd']
            last_api_call_time = time.time()
            return cached_price
        else:
            print("Erro: Dados da API não contêm a chave 'Bitcoin' ou 'USD'.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None


# Função para obter dados históricos do Bitcoin
def get_historical_data(days):
    global last_api_call_time, cached_historical_data

    if time.time() - last_api_call_time < CACHE_DURATION and cached_historical_data is not None:
        return cached_historical_data
    try:
        url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={days}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'prices' in data:
            cached_historical_data = data['prices']
            last_api_call_time = time.time()
            return cached_historical_data
        else:
            print("Erro: Dados históricos não contém a chave 'prices'.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

# Função para atualizar o preço e o gráfico
def update_data():
    # Obtém o período selecionado
    selected_period = period_combobox.get()

    # Define o número de dias com base na seleção
    if selected_period == "Tempo Real":
        days = 1  # Últimas 24 horas
    elif selected_period == "7 Dias":
        days = 7
    elif selected_period == "30 Dias":
        days = 30
    elif selected_period == "1 Ano":
        days = 365

    # Atualiza o preço atual
    current_price = get_bitcoin_price()
    if current_price is not None:
        price_label.config(text=f"Preço do Bitcoin: ${current_price}")
    else:
        price_label.config(text="Erro ao obter o preço do Bitcoin.")

    # Obtém os dados históricos
    historical_data = get_historical_data(days)
    if historical_data is None:
        return # Irá sair da função se não houver dados hostóricos

    # Separa as datas e os preços
    dates = [datetime.fromtimestamp(price[0] / 1000) for price in historical_data]
    prices = [price[1] for price in historical_data]

    # Limpa o gráfico anterior e plota os novos dados
    ax.clear()
    ax.plot(dates, prices, label=f"Preço do Bitcoin ({selected_period})", color="blue")
    ax.set_title(f"Variação do Preço do Bitcoin ({selected_period})")
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço (USD)")
    ax.legend()
    ax.grid(True)
    canvas.draw()

    # Agenda a próxima atualização (a cada 30 segundos)
    root.after(10000, update_data)

def on_period_change(event):
    update_data()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Cotação do Bitcoin e Gráfico Histórico")

# Rótulo para mostrar o preço atual
price_label = ttk.Label(root, text="Carregando...", font=("Arial", 16))
price_label.pack(pady=10)

# Combobox para selecionar o período
period_label = ttk.Label(root, text="Selecione o período:", font=("Arial", 12))
period_label.pack(pady=5)

period_combobox = ttk.Combobox(root, values=["Tempo Real", "7 Dias", "30 Dias", "1 Ano"], state="readonly")
period_combobox.current(0)  # Define o valor padrão
period_combobox.pack(pady=5)

# Vincula a mudança de periodo a nova função criada
period_combobox.bind("<<ComboboxSelected>>", on_period_change)

# Cria uma figura do matplotlib para o gráfico
fig, ax = plt.subplots(figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Inicia a atualização dos dados
update_data()

# Inicia o loop da interface gráfica
root.mainloop()