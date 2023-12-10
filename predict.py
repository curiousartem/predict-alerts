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

model_filename = input("Provide the model filename: ")
if model_filename == "":
    model_filename = 'apm.pkl'

model_filepath = f'models/{model_filename}'
if not os.path.exists(model_filepath):
    print(f"Model file {model_filepath} not found. Please provide a valid model filename.")
    exit()

def loading_animation():
    with tqdm(total=10, desc=f'Loading model {model_filename}') as pbar:
        for _ in range(10):
            time.sleep(0.01)
            pbar.update(1)

# Display loading animation while loading the model
loading_animation()

# Load the trained model
model = load(model_filepath)

# Function to create features for the next N days
def create_features_for_prediction(start_date, periods):
    # Create a date range for the next N days, hourly frequency
    prediction_times = pd.date_range(start=start_date, periods=periods, freq='H')

    # Build a DataFrame with the prediction times
    features = pd.DataFrame({
        'hour': prediction_times.hour,
        'day_of_week': prediction_times.dayofweek,
        'month': prediction_times.month,
        'day_of_month': prediction_times.day,
        'week_of_year': prediction_times.isocalendar().week,
        'is_weekend': prediction_times.dayofweek >= 5,
        'season': prediction_times.month % 12 // 3 + 1,
        'time_decay': [1] * len(prediction_times)  # Set time_decay to 1 for all future data points
    })

    return features, prediction_times


# Function to make predictions
def make_predictions(model, features):
    # Use the model to make predictions
    predictions = model.predict(features)
    return predictions

def main():
    try:
        # Request user input for the current date
        current_date_input = input("Enter the current date (MM/DD/YYYY): ")
        if current_date_input in ["0/0/0", "", None]:
            current_date = datetime.datetime.now()
        else:
            current_date = datetime.datetime.strptime(current_date_input, "%m/%d/%Y")

        days_to_predict = input('Predict alerts for how many days? Default is 7: ')
        try:
            days_to_predict = int(days_to_predict)
        except ValueError:
            print("Invalid input. Defaulting to 7 days into the future.")
            days_to_predict = 7

        # Create features for the prediction period
        features, prediction_times = create_features_for_prediction(current_date, periods=days_to_predict*24)

        # Make predictions for the prediction period
        alert_predictions = make_predictions(model, features)

        # Combine the predictions with the prediction times
        predictions_df = pd.DataFrame({
            'prediction_time': prediction_times,
            'predicted_alert_count': alert_predictions
        })

        # Allow user to set a threshold or use a default value
        alert_threshold_input = input('Enter a threshold for alerts (<100%): ')
        try:
            alert_threshold = float(alert_threshold_input) / 100
        except ValueError:
            print("Invalid input. Defaulting to top 10% of results.")
            alert_threshold = predictions_df['predicted_alert_count'].quantile(0.9)

        # Filter to get times when an alert is predicted to happen above the threshold
        alert_times = predictions_df[predictions_df['predicted_alert_count'] >= alert_threshold]

        # Sort the predicted alert times by predicted alert count
        alert_times = alert_times.sort_values(by='predicted_alert_count', ascending=False)

        if alert_times.empty:
            print("No high-probability alerts predicted for the next 7 days.")
        else:
            print("Predicted high-probability alert times for the next 7 days:")
            print(alert_times)
            print(f"In total, there is expected to be {len(alert_times)} alerts with a chance higher than {alert_threshold*100}% in the next 7 days.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
