import pandas as pd
import matplotlib.pyplot as plt
import os

class WineDataFilter:
    def __init__(self, path="wine_quality.csv"):
        # Automatically detect delimiter (comma or semicolon)
        with open(path, 'r') as f:
            sample = f.readline()
            delimiter = ',' if ',' in sample else ';'
        
        self.df = pd.read_csv(path, sep=delimiter)
        self.df.columns = self.df.columns.str.strip()

        if 'quality' not in self.df.columns:
            raise ValueError("Missing 'quality' column in the dataset.")

    def filter_by_quality(self, quality: int):
        return self.df[self.df['quality'] == quality]
    
    def plot_distribution(self, df, features, quality):
        plt.figure(figsize=(10, 6))
        for feature in features:
            if feature in df.columns:
                plt.hist(df[feature], bins=20, alpha=0.5, label=feature)
            else:
                print(f"Warning: Feature '{feature}' not found in the dataset.")
        plt.legend()
        plt.title(f'Distribution of Features for Wine Quality {quality}')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        image_path = f"images/distribution_quality_{quality}.png"
        os.makedirs("images", exist_ok=True)
        plt.savefig(image_path)
        plt.close()
        return image_path
