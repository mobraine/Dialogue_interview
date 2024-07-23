import pandas as pd
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional
import tqdm as notebook_tqdm
import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = str(1)
from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor

# the global data source, if not provided by the user initially
data_global = pd.read_csv('data/data_training.csv')

# model zero-shot forcast
def get_model_forecast(days):
    global data_global # Declare data_global as global
    data_global['id'] = 'H1'
    data_local = data_global.drop(columns='Unnamed: 0')

    # define the input to the time-series prediction model
    train_data = TimeSeriesDataFrame.from_data_frame(
        data_local,
        id_column="id",
        timestamp_column="slot_start_time"
    )

    # define model
    predictor = TimeSeriesPredictor(
        prediction_length=24 * days,
        freq='h',
        path="trained_model",
        target="demand",
        eval_metric="MASE",
    )

    # dummy fit function
    predictor.fit(
        train_data,
        presets="chronos_tiny",
        # presets=''
        time_limit=600,
    )

    predictions = predictor.predict(train_data)

    # return dict(zip(predictions['timestamp'], predictions['mean']))
    return dict(zip(predictions.index.get_level_values('timestamp'), predictions['mean']))

app = FastAPI()

class InferenceResponse(BaseModel):
    forecast: Dict[datetime, float]

@app.get("/v1/inference", response_model=InferenceResponse)
async def inference(days_to_forecast: Optional[float] = 30):
    try:
        if days_to_forecast <= 0:
            raise HTTPException(status_code=400, detail="days_to_forecast must be a positive integer")
        
        forecast = get_model_forecast(days_to_forecast)
        return InferenceResponse(forecast=forecast)
    # except ValueError:
    #     raise HTTPException(status_code=400, detail="Invalid value for days_to_forecast, must be an integer")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/v1/update-data")
async def update_data(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

        data_global = pd.read_csv(file.file)
        
        if 'demand' not in data_global.columns:
            raise HTTPException(status_code=400, detail="Invalid data format. Please include demand column.")
        elif 'slot_start_time' not in data_global.columns:
            raise HTTPException(status_code=400, detail="Invalid data format. Please include slot_start_time column.")
        
        data_global.to_csv('data/data_training.csv', index=False)
        return {"message": "Data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
