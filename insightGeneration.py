import pandas as pd

# Function to calculate monthly totals for deposits and withdrawals
def calculate_monthly_totals(transactions_df):
    transactions_df['Month'] = transactions_df['Date'].dt.to_period('M')
    monthly_totals = transactions_df.groupby('Month').agg({
        'Credit': 'sum',
        'Debit': 'sum'
    }).reset_index()
    return monthly_totals

# Function to identify recurring expenses based on keywords
def identify_recurring_expenses(transactions_df):
    expense_keywords = ['rent', 'salary', 'utility', 'loan', 'medical', 'insurance', 'bill']
    recurring_expenses = transactions_df[transactions_df['Description'].str.contains('|'.join(expense_keywords), case=False, na=False)]
    return recurring_expenses

# Function to flag irregular transactions
def flag_irregular_transactions(transactions_df):
    # Calculate mean and standard deviation for credits and debits
    credit_mean = transactions_df['Credit'].mean()
    credit_std = transactions_df['Credit'].std()
    debit_mean = transactions_df['Debit'].mean()
    debit_std = transactions_df['Debit'].std()

    # Flag transactions that are more than 2 standard deviations away from the mean
    irregular_transactions = transactions_df[(transactions_df['Credit'] > credit_mean + 2 * credit_std) |
                                            (transactions_df['Debit'] > debit_mean + 2 * debit_std)]
    return irregular_transactions

# Example usage
sample_transactions = {
    "Date": pd.to_datetime(['2022-01-01', '2022-01-05', '2022-01-10', '2022-01-15']),
    "Description": ['Rent payment', 'Salary credit', 'Utility bill', 'Loan repayment'],
    "Debit": [1000, 0, 200, 500],
    "Credit": [0, 5000, 0, 0],
    "Balance": [9000, 14000, 13800, 13300]
}

df = pd.DataFrame(sample_transactions)
monthly_totals = calculate_monthly_totals(df)
recurring_expenses = identify_recurring_expenses(df)
irregular_transactions = flag_irregular_transactions(df)

print("Monthly Totals:\n", monthly_totals)
print("Recurring Expenses:\n", recurring_expenses)
print("Irregular Transactions:\n", irregular_transactions)
