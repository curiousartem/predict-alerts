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
import json
import os

# if the models/ dir doesn't exist, create
if 'models' not in os.listdir():
    os.mkdir('models')

# Replace this with your actual raw dataset URL from GitHub
dataset_url = 'https://raw.githubusercontent.com/Vadimkin/ukrainian-air-raid-sirens-dataset/main/datasets/official_data_en.csv'
model_filename = 'apm.pkl'

def download_dataset(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def preprocess_data(data, start_date=None, end_date=None):
    # Convert the 'started_at' column to datetime and set as the index
    data['started_at'] = pd.to_datetime(data['started_at'])
    data.set_index('started_at', inplace=True)

    # If a start date is provided, filter the data from that date onwards
    if start_date:
        start_date = pd.to_datetime(start_date)
        data = data[data.index >= start_date]

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

    # Drop the original 'started_at' column as it's not needed for training
    hourly_data = hourly_data.drop(columns=['started_at'])

    return hourly_data

def train_gbm_model(data):
    # Prepare the data for training
    X = data.drop('alert_count', axis=1)
    y = data['alert_count']
    
    # Create the XGBoost model
    model = xgb.XGBRegressor(objective='reg:squarederror')

    # Train the model
    model.fit(X, y)

    return model

def save_model(model, filename):
    dump(model, filename)

# Add this function to filter the dataset
def filter_by_region(data, region_name):
    return data[data['oblast'] == region_name]

# Modify the main function to include the filtering step
def main():
    try:
        # Download and load the dataset
        csv_content = download_dataset(dataset_url)
        data = pd.read_csv(StringIO(csv_content.decode('utf-8')))
        
        # Prompt the user to enter the start date for training the model
        training_data_from = input('Enter the date from which to train the model (MM/DD/YYYY): ')

        # Prompt the user to enter the end date for training the model
        training_data_to = input('Enter the date until which to train the model (MM/DD/YYYY): ')

        # if training_data_from is not a valid date, default to one month prior
        try:
            training_data_from = pd.to_datetime(training_data_from, utc=True) if training_data_from else pd.to_datetime('today', utc=True) - pd.DateOffset(months=1)
        except ValueError:
            print("Invalid start date format. Defaulting to one month prior.")
            training_data_from = pd.to_datetime('today', utc=True) - pd.DateOffset(months=1)

        # if training_data_to is not a valid date, default to today
        try:
            training_data_to = pd.to_datetime(training_data_to, utc=True) if training_data_to else pd.to_datetime('today', utc=True)
        except ValueError:
            print("Invalid end date format. Defaulting to today.")
            training_data_to = pd.to_datetime('today', utc=True)

        # Ensure the end date is after the start date
        if training_data_to < training_data_from:
            print("End date must be after start date. Setting end date to today.")
            training_data_to = pd.to_datetime('today', utc=True)

        # Filter the data for the specified date range
        data['started_at'] = pd.to_datetime(data['started_at'], utc=True)  # Convert to UTC
        data = data[(data['started_at'] >= training_data_from) & (data['started_at'] <= training_data_to)]
        print(f"Data points after filtering by date range: {len(data)}")

        
        input_region = ''
        def request_region_name():
            while True:
                input_region = input('Enter the region to train the model for: ')
                if input_region:
                    return input_region
                else:
                    print('You entered an invalid region. Please try again.')
        input_region = request_region_name()


        kyiv_data = filter_by_region(data, input_region)
        print(f"Data points after filtering by region '{input_region}': {len(kyiv_data)}")


        # Preprocess the data
        processed_data = preprocess_data(kyiv_data)

        model_filename = input('Enter the name of the file to save the model to: ')
        if model_filename == "":
            model_filename = f'apm-{random.randint(100, 999)}.pkl'
            print('No filename provided, using a random one instead.')

        def loading_animation():
            with tqdm(total=10, desc=f'Training {model_filename}') as pbar:
                for _ in range(10):
                    time.sleep(0.01)
                    pbar.update(1)
        loading_animation()
        # Train the GBM model
        model = train_gbm_model(processed_data)

        # Save the trained model to a file
        save_model(model, f'models/{model_filename}')

        print(f"Model trained and saved to {model_filename}")
        print('\nNow that your model has been saved, run `python3 predict.py` to make predictions.')

        if input('Would you like to run this command? (yes/no): ').lower() == 'yes':
            runpy.run_path('predict.py')
        else:
            print('Exiting...')
            exit()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
