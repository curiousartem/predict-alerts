# predict.py
import pandas as pd
from joblib import load
import datetime
import os
from tqdm import tqdm
import time

# if the models/ dir doesn't exist, create
if 'models' not in os.listdir():
    os.mkdir('models')

model_filename = f'models/{input("Provide the model filename: ")}'
if model_filename == "":
    model_filename = 'models/apm.pkl'
    if model_filename not in os.listdir():
        print(f"Model file {model_filename} not found. Please provide a valid model filename.")
        exit()

def loading_animation():
    with tqdm(total=10, desc=f'Loading model {model_filename}') as pbar:
        for _ in range(10):
            time.sleep(0.01)
            pbar.update(1)

# Display loading animation while loading the model
loading_animation()

# Load the trained model
model = load(model_filename)

# Function to create features for the next 7 days

def create_features_for_next_week():
    # Request user input for the current date
    current_date_input = input("Enter the current date (MM/DD/YYYY): ")
    
    # Check if the user inputted 0/0/0 as the date
    if current_date_input == "0/0/0" or current_date_input is None or current_date_input == "":
        # Use the current date as the current date
        current_date = datetime.datetime.now().date()
        print('The current date has been picked.')
    else:
        # Parse the user inputted date
        current_date = datetime.datetime.strptime(current_date_input, "%m/%d/%Y").date()
    
    days_to_predict = input('Predict alerts for how many days? Defaults is 7: ')
    # check if it's a valid number
    try:
        days_to_predict = int(days_to_predict)
    except ValueError:
        print("Defaulting to 7 days into the future.")
        days_to_predict = 7
    
    # Create a date range for the next 7 days, hourly frequency
    prediction_times = pd.date_range(start=current_date,
                                     periods=days_to_predict*24, # 7 days * 24 hours
                                     freq='H')
    
    # Build a DataFrame with the prediction times
    features = pd.DataFrame({
        'hour': prediction_times.hour,
        'day_of_week': prediction_times.dayofweek
    })
    
    return features, prediction_times

# Function to make predictions
def make_predictions(model, features):
    # Use the model to make predictions
    predictions = model.predict(features)
    return predictions

def main():
    # Define a threshold for alert prediction
    
    try:
        # Create features for the next 7 days
        features, prediction_times = create_features_for_next_week()

        # Make predictions for the next 7 days
        alert_predictions = make_predictions(model, features)

        # Combine the predictions with the prediction times
        predictions_df = pd.DataFrame({
            'prediction_time': prediction_times,
            'predicted_alert_count': alert_predictions
        })

        # Calculate the threshold based on the top 30% of probabilities
        alert_threshold = predictions_df['predicted_alert_count'].quantile(0.9)
        alert_threshold_input = input('Enter a threshold for alerts (<100%): ')
        try:
            alert_threshold_input = float(alert_threshold_input)/100
        except ValueError:
            print("Defaulting to top 10% of results")

        # Filter to get times when an alert is predicted to happen above the threshold
        alert_times = predictions_df[predictions_df['predicted_alert_count'] >= alert_threshold]

        # Sort the predicted alert times by predicted alert count
        alert_times = alert_times.sort_values(by='predicted_alert_count', ascending=False)

        if alert_times.empty:
            print("No high-probability alerts predicted for the next 7 days.")
        else:
            print("Predicted high-probability alert times for the next 7 days:")
            print(alert_times)
            print('')
            print(f"In total, there is expected to be {len(alert_times)} alerts with a chance higher than {alert_threshold*100}% in the next 7 days.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
