import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta
import random
import argparse

def generate_transactions(num_rows=10000, fraud_rate=0.02, 
                          start_date='2024-01-01'):
    
    currencies = ['USD', 'CAD', 'GBP', 'EUR', 'AUD']
    countries = ['US', 'CA', 'GB', 'FR', 'AU', 'IN', 'SG']
    merchant_categories = ['retail', 'food', 'travel', 
                           'entertainment', 'crypto', 'ATM']
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    
    data = []
    for _ in range(num_rows):
        is_fraud = 1 if random.random() < fraud_rate else 0
        
        # Fraud transactions have patterns
        amount = round(random.uniform(500, 5000), 2) if is_fraud \
                 else round(random.uniform(1, 500), 2)
        
        merchant_cat = random.choice(['crypto', 'ATM']) if is_fraud \
                       else random.choice(merchant_categories)
        
        transaction = {
            'transaction_id': str(uuid.uuid4()),
            'customer_id': f'CUST_{random.randint(1000, 9999)}',
            'merchant_id': f'MERCH_{random.randint(100, 999)}',
            'merchant_category': merchant_cat,
            'amount': amount,
            'currency': random.choice(currencies),
            'timestamp': start + timedelta(
                seconds=random.randint(0, 86400*30)),
            'country': random.choice(countries),
            'is_fraud': is_fraud
        }
        data.append(transaction)
    
    df = pd.DataFrame(data)
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=10000)
    parser.add_argument('--fraud_rate', type=float, default=0.02)
    parser.add_argument('--start_date', type=str, 
                        default='2024-01-01')
    parser.add_argument('--output', type=str, 
                        default='transactions.csv')
    args = parser.parse_args()
    
    df = generate_transactions(args.rows, args.fraud_rate, 
                               args.start_date)
    df.to_csv(f'data/sample/{args.output}', index=False)
    print(f"Generated {len(df)} transactions")
    print(f"Fraud rate: {df['is_fraud'].mean():.2%}")
    print(f"Date range: {df['timestamp'].min()} "
          f"to {df['timestamp'].max()}")