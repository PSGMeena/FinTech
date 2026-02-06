import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_csv(filename, business_type, rows=50):
    start_date = datetime(2025, 1, 1)
    data = []
    
    # Define vocabulary based on business type
    if business_type == 'Retail':
        incomes = ['Daily Sales Cash', 'UPI Payment Received', 'Card Settlement', 'Bulk Order Advance']
        expenses = ['Inventory Purchase', 'Store Rent', 'Staff Salary', 'Electricity Bill', 'Packaging Material']
    elif business_type == 'Agri':
        incomes = ['Crop Sale - Mandi', 'Govt Subsidy Credit', 'Milk Cooperative Payout', 'Equipment Lease Income']
        expenses = ['Fertilizer Purchase', 'Tractor Diesel', 'Seed Purchase', 'Harvest Labor Payment', 'Crop Insurance Premium']
    elif business_type == 'Manufacturing':
        incomes = ['Distributor Payment', 'Export Order Advance', 'Scrap Sale', 'Finished Goods Invoice #2025']
        expenses = ['Raw Material - Steel', 'Factory Power Bill', 'Machine Maintenance', 'Logistics/Transport', 'Worker Wages']
    else:
        incomes = ['Service Fee', 'Consulting Invoice', 'Retainer Payment']
        expenses = ['Office Rent', 'Software Subscription', 'Broadband Bill', 'Travel Expense']

    balance = 50000
    
    for i in range(rows):
        date = start_date + timedelta(days=i*2)
        if i % 3 == 0: # Income event
            desc = np.random.choice(incomes)
            credit = np.random.randint(10000, 50000)
            debit = 0
        else: # Expense event
            desc = np.random.choice(expenses)
            credit = 0
            debit = np.random.randint(2000, 15000)
            
        # Add some specific triggers for AI
        if i == 10:
            desc = "Loan EMI Payment"
            debit = 12000
            credit = 0
        
        if i == 20: 
            desc = "GST Tax Payment"
            debit = 5000
            credit = 0
            
        balance = balance + credit - debit
        
        data.append({
            'Date': date.strftime('%d-%m-%Y'),
            'Description': desc,
            'Debit': debit,
            'Credit': credit,
            'Balance': balance
        })
        
    df = pd.DataFrame(data)
    
    # Ensure directory exists
    os.makedirs('static', exist_ok=True)
    path = os.path.join('static', filename)
    df.to_csv(path, index=False)
    print(f"Generated {path}")

if __name__ == "__main__":
    generate_csv('retail_sample.csv', 'Retail')
    generate_csv('agri_sample.csv', 'Agri')
    generate_csv('manufacturing_sample.csv', 'Manufacturing')
