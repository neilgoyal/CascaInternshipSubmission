from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Function to prepare data for ML
def prepare_ml_data(transactions_df):
    # Selecting relevant features
    features = transactions_df[['Debit', 'Credit']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    return scaled_features

# Function to apply KMeans clustering to identify transaction patterns
def apply_kmeans(transactions_df, n_clusters=3):
    data = prepare_ml_data(transactions_df)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    transactions_df['Cluster'] = kmeans.fit_predict(data)
    return transactions_df

# Function to predict loan eligibility based on financial stability
def predict_loan_eligibility(transactions_df):
    # Simple rule-based approach for demo purposes
    total_deposits = transactions_df['Credit'].sum()
    total_withdrawals = transactions_df['Debit'].sum()

    if total_deposits > total_withdrawals * 1.5:
        return "Eligible for loan"
    else:
        return "Not eligible for loan"

# Example usage
sample_data = {
    "Date": pd.to_datetime(['2022-01-01', '2022-01-05', '2022-01-10', '2022-01-15']),
    "Description": ['Rent payment', 'Salary credit', 'Utility bill', 'Loan repayment'],
    "Debit": [1000, 0, 200, 500],
    "Credit": [0, 5000, 0, 0],
    "Balance": [9000, 14000, 13800, 13300]
}

df = pd.DataFrame(sample_data)
clustered_df = apply_kmeans(df)
eligibility = predict_loan_eligibility(df)

print("Clustered Transactions:\n", clustered_df)
print("Loan Eligibility:\n", eligibility)
