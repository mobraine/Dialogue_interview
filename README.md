# Dialogue Demand forecast API

A FastAPI application for future demand inference using Transformer-based models and historic data updates.

## Setup Instructions

1. Install dependencies:
   
pip install autogluon.timeseries

pip install fastapi

2. Run the server:

uvicorn main:app --reload

3. Test the model inference and data update:

Go to http://127.0.0.1:8000/docs, for the Inference or Update Data drop down panel, select "try it out" to provide your own input of `days_to_forecast` or upload your own data formatted accorindly to 

## API Documentation

### GET /v1/inference

- **Description**: Get the output from the model.
- **Parameters**:
    - `days_to_forecast` (float): Number of days to forecast. Default is 30. The output of the model provides the hourly forecast of 24 * `days_to_forecast`. Currently 1-2 day infers within a reasonable amount of time.
- **Response**:
    - JSON object with keys representing forecast time stamps and values representing the mean of the probabilistic forecasts.
- **Error Handling**:
    - 400: Invalid `days_to_forecast` parameter.
    - 500: Server error.

### POST /v1/update-data

- **Description**: Replace the data provided to the training model.
- **Expected Data Format**: CSV file with two columns: `slot_start_time` and `demand`.
- **Response**:
    - 200: Data updated successfully.
- **Error Handling**:
    - 400: Invalid file format.
    - 500: Server error.
