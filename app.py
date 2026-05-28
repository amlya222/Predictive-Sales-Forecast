from io import BytesIO
import base64

from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

DATA_FILE = "sales_data_sample.csv"


def load_sales_data():
    df = pd.read_csv(DATA_FILE, encoding='latin1')
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
    df.drop_duplicates(inplace=True)
    df['YEAR_MONTH'] = df['ORDERDATE'].dt.to_period('M')
    return df


def fig_to_base64(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode('utf-8')
    return encoded


def create_trend_plot(df):
    monthly_sales = df.groupby('MONTH_ID')['SALES'].sum()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(monthly_sales.index, monthly_sales.values, marker='o', color='#1f77b4')
    ax.set_title('Monthly Sales Trend')
    ax.set_xlabel('Month')
    ax.set_ylabel('Sales')
    ax.grid(alpha=0.3)
    return fig_to_base64(fig)


def create_forecast_plot(df, forecast_data, future_labels, predictions):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(forecast_data['Month_Number'], forecast_data['SALES'], marker='o', label='Actual Sales')
    ax.plot(range(len(forecast_data), len(forecast_data) + len(predictions)), predictions, marker='o', linestyle='--', color='#ff7f0e', label='Predicted Sales')
    ax.set_title('Sales Forecast')
    ax.set_xlabel('Month Number')
    ax.set_ylabel('Sales')
    ax.grid(alpha=0.3)
    ax.legend()
    return fig_to_base64(fig)


def compute_summary(df):
    monthly_sales = df.groupby('MONTH_ID')['SALES'].sum()
    product_sales = df.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=False).reset_index()
    country_sales = df.groupby('COUNTRY')['SALES'].sum().sort_values(ascending=False).reset_index()
    forecast_data = df.groupby('YEAR_MONTH')['SALES'].sum().reset_index()
    forecast_data['YEAR_MONTH'] = forecast_data['YEAR_MONTH'].astype(str)
    forecast_data['Month_Number'] = range(len(forecast_data))

    X = forecast_data[['Month_Number']]
    y = forecast_data['SALES']
    model = LinearRegression()
    model.fit(X, y)
    future_months = pd.DataFrame({'Month_Number': range(len(forecast_data), len(forecast_data) + 6)})
    predictions = model.predict(future_months)

    last_period = pd.Period(forecast_data['YEAR_MONTH'].iloc[-1], freq='M')
    future_labels = [(last_period + i).strftime('%Y-%m') for i in range(1, 7)]
    forecast_table = [
        {'period': period, 'prediction': float(pred)}
        for period, pred in zip(future_labels, predictions)
    ]

    summary = {
        'shape': df.shape,
        'columns': list(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'top_products': product_sales.head(8).to_dict(orient='records'),
        'top_countries': country_sales.head(8).to_dict(orient='records'),
        'forecast_table': forecast_table,
        'trend_plot': create_trend_plot(df),
        'forecast_plot': create_forecast_plot(df, forecast_data, future_labels, predictions),
        'sales_sample': df.head(8).to_dict(orient='records')
    }
    return summary


@app.route('/')
def index():
    df = load_sales_data()
    summary = compute_summary(df)
    return render_template('index.html', summary=summary)


if __name__ == '__main__':
    app.run(debug=True)
