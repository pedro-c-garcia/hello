# Copilot / AI Agent Instructions for `hello` repository ✅

## Quick summary
- Purpose: small Python utility that fetches recent index quotes via `yfinance` and saves them to an Excel file (`out/cotacoes.xlsx`).
- Single script of interest: `geraXls.py` (Portuguese variable names & messages).

---

## How to run (Developer workflow) 🔧
1. Activate the project's virtual environment (example, PowerShell):
   - `& D:\GitHub\hello\.venv\Scripts\Activate.ps1`
2. Install dependencies (note: repository `requirements.txt` appears incomplete — `yfinance` and `pandas` are imported but not listed):
   - `pip install -r requirements.txt`
   - `pip install yfinance pandas openpyxl`
3. Run the script:
   - `python geraXls.py`
4. Output:
   - `out/cotacoes.xlsx` will be created. Ensure an `out/` directory exists before running; the script does not create the directory.

---

## Project-specific details & patterns 📋
- Language: variable names, comments and final printed message are in Portuguese — keep text/strings consistent with existing language when editing or adding features.
- Index definition: Two parallel lists are used: `indices = [...]` and `nomes_indices = [...]`. Order matters — maintain parallel order when adding/removing indices.
- Timezone handling: The script explicitly strips timezone info from the DataFrame index with `df.index = df.index.tz_localize(None)` to avoid timezone-related Excel issues.
- Output format: Excel (`DataFrame.to_excel`). Rely on `openpyxl`/Excel-compatible engines for writing.
- Logging/UX: script prints each ticker's `history` DataFrame and a final Portuguese success message. Use the same pattern for new behavior unless internationalization is introduced.

---

## Safety & correctness notes ⚠️
- Missing dependencies: `requirements.txt` currently contains many Flask-related packages but is missing `yfinance` and `pandas`. When adding new scripts, keep `requirements.txt` up to date.
- Directory creation: The script writes to `out/cotacoes.xlsx` — ensure to create `out/` or modify the script to create it programmatically.
- Index-to-name mapping: If you change to a dict mapping, update tests or call sites accordingly to avoid order-dependent bugs.

---

## Continuous Integration (CI) ✅
- There is a GitHub Actions workflow at `.github/workflows/smoke-test.yml` that runs on push and PR. It installs dependencies, runs `geraXls.py` with a short date range, verifies the output Excel file `out/ci_cotacoes.xlsx` exists, and uploads it as an artifact.
- For local smoke tests, run: `python geraXls.py --start 2025-01-01 --end 2025-01-03 --output out/ci_cotacoes.xlsx` and confirm the file exists.

---

## Small, actionable tasks an AI agent can do immediately ✅
- Add `yfinance`, `pandas`, and `openpyxl` to `requirements.txt`.
- Add a brief README snippet showing how to run `geraXls.py` and prerequisites (virtualenv activation + required packages).
- Make the script robust: check/create `out/` directory before writing and add small CLI args (optional date range, output path).

---

## Files to check when making changes 🔎
- `geraXls.py` — main behavior and examples
- `requirements.txt` — dependencies to sync

---

If anything here is unclear or you'd like the instructions to include specific coding conventions or PR/CI steps, tell me what to add and I'll update this file. 💡