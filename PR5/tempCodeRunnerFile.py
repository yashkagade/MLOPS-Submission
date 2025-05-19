import pandas as pd
import matplotlib.pyplot as plt
import time
from functools import wraps
import os

# Decorator to time method execution
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"Running: {func.__name__}...")
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Completed: {func.__name__} in {end - start:.2f}s\n")
        return result
    return wrapper

class SalesDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    @timing_decorator
    def load_data(self):
        self.data = pd.read_csv(self.file_path)
        print("📄 Available columns:", list(self.data.columns))
        
        # Try to identify the date column (usually "Date" or "Invoice Date")
        possible_date_cols = ['Date', 'Invoice Date', 'date', 'Datetime']
        for col in self.data.columns:
            if col.strip() in possible_date_cols:
                self.data[col.strip()] = pd.to_datetime(self.data[col.strip()])
                self.data.rename(columns={col: 'Date'}, inplace=True)
                print(f"✅ '{col}' converted to datetime and renamed to 'Date'.")
                break
        else:
            raise KeyError("❌ No recognized date column found. Please check your dataset headers.")

    @timing_decorator
    def summarize_data(self):
        print("📊 Summary Statistics:")
        print(self.data.describe(include='all'))

    @timing_decorator
    def plot_sales_over_time(self):
        sales_by_date = self.data.groupby('Date')['Total'].sum()
        plt.figure(figsize=(10, 6))
        sales_by_date.plot(kind='line', marker='o', color='orange')
        plt.title('Total Sales Over Time')
        plt.xlabel('Date')
        plt.ylabel('Total Sales')
        plt.grid(True)
        os.makedirs('plots', exist_ok=True)
        plt.savefig('plots/sales_over_time.png')
        plt.close()
        print("📈 Plot saved to 'plots/sales_over_time.png'")

    @timing_decorator
    def run_all(self):
        self.load_data()
        self.summarize_data()
        self.plot_sales_over_time()

# 🔁 Replace with your actual path
file_path = r"C:\Users\User\OneDrive\Desktop\MlOps Assignments\python\assign_5\Supermart Grocery Sales - Retail Analytics Dataset.csv"

# 🧪 Run the full analysis
processor = SalesDataProcessor(file_path)
processor.run_all()
