import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sales_data_sample.csv", encoding='latin1') #import dataset

print(df.head()) # first 5 rows of the dataset
print(df.info()) # dataset info
print(df.shape) # row and column count
print(df.columns) # review column names
print(df.isnull().sum()) # check for missing values in each column

df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
df.isnull().sum()
df.drop_duplicates(inplace=True)
monthly_sales = df.groupby('MONTH_ID')['SALES'].sum()

print(monthly_sales)

monthly_sales.plot(kind='line')

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show()


product_sales = df.groupby('PRODUCTLINE')['SALES'].sum()

print(product_sales.sort_values(ascending=False))

country_sales = df.groupby('COUNTRY')['SALES'].sum()

print(country_sales.sort_values(ascending=False))

df['YEAR_MONTH'] = df['ORDERDATE'].dt.to_period('M')

forecast_data = df.groupby('YEAR_MONTH')['SALES'].sum().reset_index()

forecast_data['YEAR_MONTH'] = forecast_data['YEAR_MONTH'].astype(str)

print(forecast_data.head())

forecast_data['Month_Number'] = range(len(forecast_data))
from sklearn.linear_model import LinearRegression

X = forecast_data[['Month_Number']]
y = forecast_data['SALES']

model = LinearRegression()

model.fit(X, y)
future_months = [[i] for i in range(len(forecast_data), len(forecast_data)+6)]

predictions = model.predict(future_months)

print(predictions)
plt.plot(forecast_data['Month_Number'], y, label='Actual Sales')

plt.plot(
    range(len(forecast_data), len(forecast_data)+6),
    predictions,
    label='Predicted Sales'
)

plt.legend()
plt.show()