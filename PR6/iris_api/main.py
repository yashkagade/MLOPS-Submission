from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from iris_data_filter import IrisDataFilter
import matplotlib.pyplot as plt
import os

app = FastAPI()

iris_filter = IrisDataFilter("iris.csv")  # Ensure this matches your CSV file name

@app.get("/")
def read_root():
    unique_species = iris_filter.df['Species'].unique().tolist()
    return {"Available species": unique_species}

@app.get("/filter-iris/")
def filter_iris(species: str = Query("all", description="Species: Iris-setosa, Iris-versicolor, Iris-virginica, or all")):
    filtered_data = iris_filter.filter_by_species(species)
    
    print(f"Filtered rows: {len(filtered_data)}")  # Debug info

    if filtered_data.empty:
        return {"error": f"No data found for species: {species}"}

    # Plot feature distributions
    plt.figure(figsize=(10, 6))
    features = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']
    
    for feature in features:
        plt.hist(filtered_data[feature], bins=15, alpha=0.6, label=feature)

    plt.title(f"Feature Distribution for: {species}")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    os.makedirs("static", exist_ok=True)
    plot_path = "static/dist_plot.png"
    plt.savefig(plot_path)
    plt.close()

    return {
        "filtered_count": len(filtered_data),
        "visualization": "/visualization",
        "sample_data": filtered_data.head(5).to_dict(orient="records")
    }

@app.get("/visualization")
def get_visualization():
    return FileResponse("static/dist_plot.png", media_type="image/png")
