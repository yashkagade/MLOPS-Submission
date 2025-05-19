import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# ⏱️ Timing Decorator
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f" {func.__name__} executed in {end - start:.4f} seconds.")
        return result
    return wrapper

# 🛍️ Sales Data Processor
class SalesDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        os.makedirs("plots", exist_ok=True)

    @timing_decorator
    def load_data(self):
        self.data = pd.read_csv(self.file_path)
        print("📄 Data loaded successfully!")
        print("📄 Available columns:", list(self.data.columns))

        if 'Order Date' in self.data.columns:
            try:
                # Attempt to parse dates with flexibility
                self.data['Order Date'] = pd.to_datetime(
                    self.data['Order Date'], errors='coerce', infer_datetime_format=True
                )
            except Exception as e:
                print("⚠️ Error converting 'Order Date' to datetime:", e)
        else:
            raise KeyError("❌ 'Order Date' column not found in dataset.")

    @timing_decorator
    def summarize_data(self):
        if self.data is not None:
            print("Summary Statistics:")
            print(self.data.describe(include='all'))
        else:
            print("⚠️ No data to summarize.")

    @timing_decorator
    def plot_sales_over_time(self):
        if self.data is None:
            print("⚠️ Load data before plotting.")
            return

        # Remove rows with invalid dates
        self.data = self.data.dropna(subset=['Order Date'])

        self.data['Month'] = self.data['Order Date'].dt.to_period('M').astype(str)
        sales_by_month = self.data.groupby('Month')['Sales'].sum()

        plt.figure(figsize=(10, 6))
        sales_by_month.plot(kind='line', marker='o', color='mediumseagreen')
        plt.title(' Total Sales Over Time')
        plt.xlabel('Month')
        plt.ylabel('Sales')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        filename = 'plots/sales_over_time.png'
        plt.savefig(filename)
        plt.close()
        print(f" Plot saved as: {filename}")

    @timing_decorator
    def run_all(self):
        self.load_data()
        self.summarize_data()
        self.plot_sales_over_time()

# ✅ Run the processor
if __name__ == "__main__":
    file_path = r"C:\Users\User\OneDrive\Desktop\MlOps Assignments\python\assign_5\Supermart Grocery Sales - Retail Analytics Dataset.csv"
    processor = SalesDataProcessor(file_path)
    processor.run_all()
