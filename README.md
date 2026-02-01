# hello

Small utility to fetch recent index quotes and save them to an Excel file.

## Quick start

1. Activate the project's virtual environment (PowerShell):

   & D:\\GitHub\\hello\\.venv\\Scripts\\Activate.ps1

2. Install dependencies:

   pip install -r requirements.txt

3. Run the script (defaults: last 30 days, output `out/cotacoes.xlsx`):

   python geraXls.py

4. Example: custom date range and output path

   python geraXls.py --start 2025-12-01 --end 2025-12-31 --output out/dec_cotacoes.xlsx

Notes:
- Ensure that `out/` exists or let the script create it; the script will create the output directory if necessary.
- The script prints fetched history for each ticker and saves an Excel file with raw closes and percentage variations relative to S&P 500.
