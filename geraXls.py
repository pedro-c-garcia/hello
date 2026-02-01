import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Defina os índices que você quer buscar
indices = ['^GSPC', '^DJI', '^IXIC', '^RUT']
nomes_indices = ['S&P 500', 'Dow Jones', 'Nasdaq', 'Russell 2000']

# Obtenha as cotações dos índices do último mês
data_inicio = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
data_fim = datetime.today().strftime('%Y-%m-%d')

cotacoes = {}
for indice in indices:
    ticker = yf.Ticker(indice)
    cotacao = ticker.history(start=data_inicio, end=data_fim)
    cotacoes[nomes_indices[indices.index(indice)]] = cotacao['Close']
    print (cotacao)

# Cria um DataFrame com as cotações
df = pd.DataFrame(cotacoes)

# Calcula a variação percentual em relação ao S&P 500
sp500 = df['S&P 500']
for coluna in df.columns:
    if coluna != 'S&P 500':
        df[f'{coluna} (var. %)'] = ((df[coluna] - sp500) / sp500) * 100

df.index = df.index.tz_localize(None)
# Salva o DataFrame em um Excel
df.to_excel('out/cotacoes.xlsx')

print('Arquivo cotacoes.xlsx criado com sucesso!')