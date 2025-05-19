from fastapi import FastAPI, Query
from typing import List
from wine_filter import WineDataFilter
import pandas as pd

app = FastAPI(title="Wine Quality Filter API")

wine_filter = WineDataFilter()

@app.get("/filter")
def filter_wine(quality: int = Query(..., ge=0, le=10), features: List[str] = Query(...)):
    filtered_df = wine_filter.filter_by_quality(quality)
    
    if filtered_df.empty:
        return {"message": f"No wines found with quality {quality}"}
    
    image_path = wine_filter.plot_distribution(filtered_df, features, quality)
    return {
        "filtered_data": filtered_df[features].head(10).to_dict(orient="records"),
        "visualization": image_path
    }
