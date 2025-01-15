import pandas as pd
import re

# Function to parse text into structured transaction data
def parse_transactions(text):
   pattern = r'(\d{2}-[A-Za-z]{3}-\d{4})\s+(.*?)\s+(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d+\.\d{2})'
   transactions = []

   # Find all matching transaction lines
   for match in re.finditer(pattern, text):
       date, description, debit, credit, balance = match.groups()
       transactions.append({
           "Date": date,
           "Description": description.strip(),
           "Debit": float(debit),
           "Credit": float(credit),
           "Balance": float(balance)
       })

   return pd.DataFrame(transactions)

# Function to clean and normalize data
def clean_data(transactions_df):
   # Convert date column to datetime format
   transactions_df['Date'] = pd.to_datetime(transactions_df['Date'], format='%d-%b-%Y', errors='coerce')

   # Fill missing values in numerical columns with 0
   transactions_df.fillna({"Debit": 0.0, "Credit": 0.0, "Balance": 0.0}, inplace=True)

   # Sort transactions by date
   transactions_df.sort_values(by="Date", inplace=True)

   return transactions_df

# Example usage
sample_text = """
01-Apr-2018 IMPS-MOB/Fund Trf 1.00 2000.00 2022.62
03-Apr-2018 NACH/TP ACH Bajaj Finanac 1912.00 0.00 110.62
"""

transactions = parse_transactions(sample_text)
cleaned_data = clean_data(transactions)

print(cleaned_data)
