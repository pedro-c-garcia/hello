#!/usr/bin/env python3
import argparse
import os
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

# Defina os índices que você quer buscar
indices = ['^GSPC', '^DJI', '^IXIC', '^RUT']
nomes_indices = ['S&P 500', 'Dow Jones', 'Nasdaq', 'Russell 2000']

parser = argparse.ArgumentParser(description='Baixa cotações de índices e salva em Excel.')
parser.add_argument('--start', '-s', default=(datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d'),
                    help='Data de início (YYYY-MM-DD)')
parser.add_argument('--end', '-e', default=datetime.today().strftime('%Y-%m-%d'),
                    help='Data final (YYYY-MM-DD)')
parser.add_argument('--output', '-o', default='out/cotacoes.xlsx',
                    help='Caminho do arquivo de saída (xlsx)')
args = parser.parse_args()

try:
    data_inicio = datetime.strptime(args.start, '%Y-%m-%d').strftime('%Y-%m-%d')
    data_fim = datetime.strptime(args.end, '%Y-%m-%d').strftime('%Y-%m-%d')
except ValueError:
    print('Formato de data inválido. Use YYYY-MM-DD.')
    raise SystemExit(1)

# Cria diretório de saída se necessário
out_dir = os.path.dirname(args.output) or '.'
os.makedirs(out_dir, exist_ok=True)

cotacoes = {}
for i, indice in enumerate(indices):
    ticker = yf.Ticker(indice)
    cotacao = ticker.history(start=data_inicio, end=data_fim)
    cotacoes[nomes_indices[i]] = cotacao['Close']
    print(cotacao)

# Cria DataFrame e calcula variações relativas ao S&P 500
df = pd.DataFrame(cotacoes)
sp500 = df.get('S&P 500')
if sp500 is not None:
    for coluna in df.columns:
        if coluna != 'S&P 500':
            df[f'{coluna} (var. %)'] = ((df[coluna] - sp500) / sp500) * 100

# Remove timezone do índice para evitar problemas com Excel
df.index = df.index.tz_localize(None)

# Salva o DataFrame em um Excel
df.to_excel(args.output)

print(f'Arquivo {args.output} criado com sucesso!')