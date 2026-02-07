from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf
import io

from flask import Flask, jsonify, render_template, request, send_file

# Defina os indices que voce quer buscar
indices = ['^GSPC', '^DJI', '^IXIC', '^RUT']
nomes_indices = ['S&P 500', 'Dow Jones', 'Nasdaq', 'Russell 2000']

app = Flask(__name__)


def _padrao_datas():
    hoje = datetime.today()
    inicio = hoje - timedelta(days=30)
    return inicio.strftime('%Y-%m-%d'), hoje.strftime('%Y-%m-%d')


def _parse_data(valor: str, padrao: str) -> str:
    if not valor:
        return padrao
    try:
        return datetime.strptime(valor, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError as exc:
        raise ValueError('Formato de data invalido. Use YYYY-MM-DD.') from exc


def _buscar_cotacoes(data_inicio: str, data_fim: str) -> pd.DataFrame:
    cotacoes = {}
    for i, indice in enumerate(indices):
        ticker = yf.Ticker(indice)
        cotacao = ticker.history(start=data_inicio, end=data_fim)
        if not cotacao.empty:
            cotacoes[nomes_indices[i]] = cotacao['Close']

    df = pd.DataFrame(cotacoes)
    sp500 = df.get('S&P 500')
    if sp500 is not None:
        for coluna in df.columns:
            if coluna != 'S&P 500':
                df[f'{coluna} (var. %)'] = ((df[coluna] - sp500) / sp500) * 100

    df.index = df.index.tz_localize(None)
    return df


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/indices')
def indices_page():
    data_inicio, data_fim = _padrao_datas()
    return render_template('indices.html', data_inicio=data_inicio, data_fim=data_fim)


@app.route('/api/quotes')
def api_quotes():
    padrao_inicio, padrao_fim = _padrao_datas()
    try:
        data_inicio = _parse_data(request.args.get('start'), padrao_inicio)
        data_fim = _parse_data(request.args.get('end'), padrao_fim)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    df = _buscar_cotacoes(data_inicio, data_fim)
    if df.empty:
        return jsonify(
            {
                'start': data_inicio,
                'end': data_fim,
                'labels': [],
                'series': {},
                'columns': [],
                'rows': [],
            }
        )

    labels = [idx.strftime('%Y-%m-%d') for idx in df.index]
    series = {
        coluna: [None if pd.isna(v) else float(v) for v in df[coluna].tolist()]
        for coluna in df.columns
        if '(var. %)' not in coluna
    }

    columns = ['Data'] + list(df.columns)
    rows = []
    for idx, row in df.iterrows():
        linha = [idx.strftime('%Y-%m-%d')]
        for valor in row.tolist():
            linha.append(None if pd.isna(valor) else float(valor))
        rows.append(linha)

    return jsonify(
        {
            'start': data_inicio,
            'end': data_fim,
            'labels': labels,
            'series': series,
            'columns': columns,
            'rows': rows,
        }
    )


@app.route('/api/export')
def api_export():
    padrao_inicio, padrao_fim = _padrao_datas()
    try:
        data_inicio = _parse_data(request.args.get('start'), padrao_inicio)
        data_fim = _parse_data(request.args.get('end'), padrao_fim)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    df = _buscar_cotacoes(data_inicio, data_fim)
    if df.empty:
        return jsonify({'error': 'Sem dados para exportar.'}), 400

    buffer = io.BytesIO()
    df.to_excel(buffer, index=True)
    buffer.seek(0)
    filename = f'cotacoes_{data_inicio}_a_{data_fim}.xlsx'
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )


if __name__ == '__main__':
    app.run(debug=True)
