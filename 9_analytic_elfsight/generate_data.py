import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(num_rows=5000):
    np.random.seed(42)
    
    # Генерация базовых дат
    end_date = datetime(2023, 12, 31)
    dates = [end_date - timedelta(days=random.randint(0, 365)) for _ in range(num_rows)]
    
    user_ids = [f"U{str(i).zfill(5)}" for i in range(1, num_rows + 1)]
    sources = np.random.choice(['Organic', 'PPC', 'Social Media', 'Referral'], num_rows, p=[0.4, 0.3, 0.2, 0.1])
    statuses = np.random.choice(['Free Trial', 'Monthly', 'Annual', 'Inactive'], num_rows, p=[0.3, 0.4, 0.1, 0.2])
    
    sub_start_dates = []
    sub_end_dates = []
    
    for i in range(num_rows):
        start_date = dates[i] + timedelta(days=random.randint(1, 14))
        sub_start_dates.append(start_date.strftime('%Y-%m-%d'))
        
        if statuses[i] == 'Inactive':
            end = start_date + timedelta(days=random.randint(15, 60))
            sub_end_dates.append(end.strftime('%Y-%m-%d'))
        else:
            sub_end_dates.append(pd.NA)
            
    active_widgets = np.where(statuses == 'Inactive', 0, np.random.randint(1, 10, num_rows))
    widget_interactions = active_widgets * np.random.randint(10, 500, num_rows)
    time_spent = np.where(statuses == 'Annual', np.random.randint(500, 2000, num_rows), np.random.randint(10, 500, num_rows))
    countries = np.random.choice(['USA', 'UK', 'Germany', 'France', 'India', 'Brazil'], num_rows)

    df = pd.DataFrame({
        'Date': [d.strftime('%Y-%m-%d') for d in dates],
        'User ID': user_ids,
        'Registration Source': sources,
        'Subscription Status': statuses,
        'Subscription Start Date': sub_start_dates,
        'Subscription End Date': sub_end_dates,
        'Number of Active Widgets': active_widgets,
        'Number of Widget Interactions': widget_interactions,
        'Time Spent on Platform': time_spent,
        'Location': countries
    })
    
    df.to_csv('sample_data.csv', index=False)
    print("Файл sample_data.csv успешно сгенерирован!")

if __name__ == "__main__":
    generate_sample_data()