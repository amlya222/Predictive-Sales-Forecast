# Predictive Sales Forecast

A small sales forecasting project with a Flask frontend built on a sample sales dataset.

## What it includes

- `app.py` — Flask application serving the dashboard
- `templates/index.html` — HTML dashboard template
- `static/style.css` — styling for the dashboard
- `sales_data_sample.csv` — source sales dataset
- `requirements.txt` — Python dependencies

## Features

- loads sales data from `sales_data_sample.csv`
- computes sales summaries for product lines and countries
- shows a monthly sales trend chart
- trains a linear regression model on monthly sales
- displays a 6-month sales forecast table and plot

## Setup

1. Create or activate a Python virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Run

```powershell
python app.py
```

Then open `http://127.0.0.1:5000/` in your browser.

## Notes

- `understanding.py` is not required by the Flask frontend and can be removed if you only need the web app.
- The app uses `matplotlib` to generate charts and embeds them directly into the HTML page.
