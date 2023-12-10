# train.py
import pandas as pd
import xgboost as xgb
from joblib import dump
import requests
from io import StringIO
import random
import time
from tqdm import tqdm
import runpy
import os
from datetime import datetime, timedelta

# if the models/ dir doesn't exist, create
if 'models' not in os.listdir():
    os.mkdir('models')

# Replace this with your actual raw dataset URL from GitHub
dataset_url = 'https://raw.githubusercontent.com/Vadimkin/ukrainian-air-raid-sirens-dataset/main/datasets/official_data_en.csv'

def download_dataset(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def preprocess_data(data, end_date=None):
    # Convert the 'started_at' column to datetime and set as the index
    data['started_at'] = pd.to_datetime(data['started_at'])
    data.set_index('started_at', inplace=True)

    # If an end date is provided, filter the data up to that date
    if end_date:
        end_date = pd.to_datetime(end_date)
        data = data[data.index <= end_date]

    # Resample the data to hourly frequency, counting the number of alerts in each hour
    hourly_data = data.resample('H').size()

    # Fill missing values with 0 (assuming no alerts in those hours)
    hourly_data = hourly_data.fillna(0)

    # Convert to DataFrame for compatibility with XGBoost
    hourly_data = hourly_data.to_frame(name='alert_count')

    # Reset index to add 'started_at' as a column again
    hourly_data = hourly_data.reset_index()

    # Add time-related features (e.g., hour of the day, day of the week) for the model to learn from
    hourly_data['hour'] = hourly_data['started_at'].dt.hour
    hourly_data['day_of_week'] = hourly_data['started_at'].dt.dayofweek
    hourly_data['month'] = hourly_data['started_at'].dt.month
    hourly_data['day_of_month'] = hourly_data['started_at'].dt.day
    hourly_data['week_of_year'] = hourly_data['started_at'].dt.isocalendar().week
    hourly_data['is_weekend'] = hourly_data['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    hourly_data['season'] = hourly_data['started_at'].dt.month % 12 // 3 + 1

    # Implement a time decay factor for the 'alert_count' to give more weight to recent data
    current_date = pd.to_datetime('today', utc=True)
    hourly_data['days_since_current'] = (current_date - hourly_data['started_at']).dt.days
    hourly_data['time_decay'] = 1 / (1 + hourly_data['days_since_current'])

    # Drop the original 'started_at' column as it's not needed for training
    hourly_data = hourly_data.drop(columns=['started_at', 'days_since_current'])

    return hourly_data

def train_gbm_model(data):
    # Prepare the data for training
    X = data.drop('alert_count', axis=1)
    y = data['alert_count'] * data['time_decay']  # Apply the time decay to the target variable

    # Create the XGBoost model
    model = xgb.XGBRegressor(objective='reg:squarederror')

    # Train the model
    model.fit(X, y)

    return model

def save_model(model, filename):
    dump(model, filename)

def filter_by_region(data, region_name):
    return data[data['oblast'] == region_name]

def filter_by_relevant_seasons(data, end_date):
    current_date = pd.to_datetime(end_date)
    previous_year = current_date - pd.DateOffset(years=1)
    data['started_at'] = pd.to_datetime(data['started_at'], utc=True)  # Convert to UTC
    return data[((current_date - data['started_at']).dt.days <= 365) | (data['started_at'].dt.month == previous_year.month)]

def main():
    try:
        # Download and load the dataset
        csv_content = download_dataset(dataset_url)
        data = pd.read_csv(StringIO(csv_content.decode('utf-8')))

        # Prompt the user to enter the end date for training the model
        training_data_to = input('Enter the date until which to train the model (MM/DD/YYYY): ')

        # if training_data_to is not a valid date, default to today
        try:
            training_data_to = pd.to_datetime(training_data_to, utc=True) if training_data_to else pd.to_datetime('today', utc=True)
        except ValueError:
            print("Invalid end date format. Defaulting to today.")
            training_data_to = pd.to_datetime('today', utc=True)

        # Filter the data for the relevant seasons up to the end date
        data = filter_by_relevant_seasons(data, training_data_to)

        input_region = input('Enter the region to train the model for: ').strip()
        if not input_region:
            raise ValueError('No region entered. Exiting...')

        region_data = filter_by_region(data, input_region)
        print(f"Data points after filtering by region '{input_region}': {len(region_data)}")

        # Preprocess the data
        processed_data = preprocess_data(region_data, end_date=training_data_to)

        model_filename = input('Enter the name of the file to save the model to: ').strip()
        if not model_filename:
            model_filename = f'apm-{random.randint(100, 999)}.pkl'
            print(f'No filename provided, using a random one instead: {model_filename}')

        # Train the GBM model
        model = train_gbm_model(processed_data)

        # Save the trained model to a file
        save_model(model, f'models/{model_filename}')

        print(f"Model trained and saved to models/{model_filename}")
        print('\nNow that your model has been saved, run `python predict.py` to make predictions.')

        if input('Would you like to run this command? (yes/no): ').strip().lower() == 'yes':
            runpy.run_path('predict.py')
        else:
            print('Exiting...')
            exit()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
