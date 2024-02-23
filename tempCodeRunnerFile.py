from flask import Flask, render_template, request, jsonify
import datetime as dt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load and preprocess the expense data
expense_df = pd.read_csv("expense_data_1.csv")
expense_df = expense_df.drop(['Subcategory', 'Note.1', 'Account.1', 'Currency', 'INR'], axis=1)
expense_df = expense_df.dropna()
expense_df = expense_df.drop(expense_df.loc[expense_df['Income/Expense'].isin(['Income'])].index)
expense_df['Date'] = pd.to_datetime(expense_df['Date'])
expense_df['Date'] = expense_df['Date'].map(dt.datetime.toordinal)

# Train the linear regression model
model = LinearRegression()
category_code = {'Food': 0, 'Other': 1, 'Transportation': 2, 'Apparel': 3, 'Household': 4,
                 'Social Life': 5, 'Education': 6, 'Self-development': 7, 'Beauty': 8, 'Gift': 9}
expense_df['category_code'] = expense_df['Category'].map(category_code)
inputs, targets = expense_df[['category_code', 'Date']], expense_df['Amount']
model.fit(inputs, targets)

# Function to predict expense
def predict_expense(date, category_code):
    date_ordinal = dt.datetime.strptime(date, '%Y-%m-%d').toordinal()
    input_data = np.array([[category_code, date_ordinal]])
    predicted_expense = model.predict(input_data)[0]
    return predicted_expense

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    date = data['date']
    category_code = int(data['category_code'])
    predicted_expense = predict_expense(date, category_code)
    return jsonify({'prediction': predicted_expense})

if __name__ == '__main__':
    app.run(debug=True)
