# TitanicEDA: EDA on Titanic dataset with train.csv

import pandas as pd
import matplotlib.pyplot as plt
import os

class TitanicEDA:
    def __init__(self, filepath='train.csv'):
        self.filepath = filepath
        self.data = None
        self._prepare_output_folder()

    def _prepare_output_folder(self):
        """Create a folder for saving plots if it doesn't exist."""
        if not os.path.exists('plots'):
            os.makedirs('plots')

    def load_data(self):
        """Load Titanic dataset from the given CSV file path."""
        try:
            self.data = pd.read_csv(self.filepath)
            print("✅ Data loaded successfully!")
            print(f"Shape: {self.data.shape}")
        except FileNotFoundError:
            print("❌ File not found. Please check the file path.")

    def summary_statistics(self):
        """Print summary statistics of the dataset."""
        if self.data is not None:
            print("\n📊 Summary Statistics:\n")
            print(self.data.describe(include='all'))
        else:
            print("⚠️ Data not loaded.")

    def plot_survival_by_feature(self, feature):
        """Generate and save a plot of survival rates based on the given feature."""
        if self.data is None:
            print("⚠️ Please load the data first.")
            return

        if feature not in self.data.columns:
            print(f"⚠️ Feature '{feature}' not found.")
            return

        plt.figure(figsize=(8, 6))

        if feature == 'Age':
            # Bin ages into groups
            self.data['AgeGroup'] = pd.cut(self.data['Age'], bins=[0, 12, 18, 35, 60, 100],
                                           labels=['Child', 'Teen', 'Young Adult', 'Adult', 'Senior'])
            grouped = self.data.groupby('AgeGroup')['Survived'].mean()
            grouped.plot(kind='bar', color='lightcoral')
            plt.title('Survival Rate by Age Group')
            plt.xlabel('Age Group')
        else:
            grouped = self.data.groupby(feature)['Survived'].mean()
            grouped.plot(kind='bar', color='skyblue')
            plt.title(f'Survival Rate by {feature}')
            plt.xlabel(feature)

        plt.ylabel('Survival Rate')
        plt.tight_layout()
        filename = f"plots/survival_by_{feature}.png"
        plt.savefig(filename)
        plt.close()
        print(f"📁 Plot saved as: {filename}")

    def run_all(self):
        """Run full EDA: Load data, show stats, and create plots."""
        self.load_data()
        self.summary_statistics()
        self.plot_survival_by_feature('Pclass')
        self.plot_survival_by_feature('Sex')
        self.plot_survival_by_feature('Age')


# ✅ Run the Titanic EDA
eda = TitanicEDA(r"C:\Users\User\OneDrive\Desktop\MlOps Assignments\python\assign_1\train.csv")  # Make sure train.csv is in the same directory or provide the full path
eda.run_all()
