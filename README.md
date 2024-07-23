# Dialogue Demand forecast API

A FastAPI application for future demand inference using Transformer-based models and historic data updates.

## Setup Instructions

1. Install dependencies:
   
pip install autogluon.timeseries

pip install fastapi

2. Run the server:

uvicorn main:app --reload

## API Documentation

### GET /v1/inference

- **Description**: Get the output from the model.
- **Parameters**:
    - `days_to_forecast` (float): Number of days to forecast. Default is 30. Currently 0.125 days (3 hrs) infers within a reasonable amount of time.
- **Response**:
    - JSON object with keys representing forecast time stamps and values representing the mean of the probabilistic forecasts.
- **Error Handling**:
    - 400: Invalid `days_to_forecast` parameter.
    - 500: Server error.

### POST /v1/update-data

- **Description**: Replace the data provided to the training model.
- **Expected Data Format**: CSV file.
- **Response**:
    - 200: Data updated successfully.
- **Error Handling**:
    - 400: Invalid file format.
    - 500: Server error.
