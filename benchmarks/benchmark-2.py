import pandas as pd

# Actual alerts
actual_alerts = [
    "13:47 07.12.23", "12:41 07.12.23",
    "14:40 06.12.23", "12:51 06.12.23",
    "15:00 03.12.23", "14:47 03.12.23",
    "14:37 03.12.23", "13:02 03.12.23",
    "13:48 02.12.23", "12:07 02.12.23",
    "12:26 01.12.23", "11:00 01.12.23",
    "07:49 01.12.23", "07:04 01.12.23",
]

# Model predictions based on the provided high-probability alert times
predictions = [
    "2023-12-01 00:00:00", "2023-12-02 00:00:00",
    "2023-12-02 12:00:00", "2023-12-02 22:00:00",
    "2023-12-03 00:00:00", "2023-12-03 12:00:00",
    "2023-12-04 00:00:00", "2023-12-04 10:00:00",
    "2023-12-05 00:00:00", "2023-12-05 12:00:00",
    "2023-12-06 00:00:00", "2023-12-06 12:00:00",
    "2023-12-07 00:00:00", "2023-12-07 12:00:00",
    "2023-12-05 10:00:00", "2023-12-05 22:00:00",
    "2023-12-06 10:00:00",
]

# Convert actual alerts and predictions to pandas datetime
actual_alerts_dt = pd.to_datetime(actual_alerts, format="%H:%M %d.%m.%y")
predictions_dt = pd.to_datetime(predictions)

# Define the time window for a hit (3 hours)
time_window = pd.Timedelta(hours=3)

# Initialize lists to store hits and false alarms
accurate_predictions = []
false_alarm_predictions = []

# Check each prediction if it is a hit or a false alarm
for prediction in predictions_dt:
    if any(abs(prediction - actual_alerts_dt) <= time_window):
        accurate_predictions.append(prediction)
    else:
        false_alarm_predictions.append(prediction)

# Check for omissions
omissions = len(actual_alerts_dt) - len(accurate_predictions)

# Calculate accuracy metrics
precision = len(accurate_predictions) / len(predictions_dt) if not predictions_dt.empty else 0
recall = len(accurate_predictions) / len(actual_alerts_dt) if not actual_alerts_dt.empty else 0
# Corrected calculation for the redefined accuracy
accuracy = len(accurate_predictions) / len(actual_alerts_dt) if not actual_alerts_dt.empty else 0

# Print the accurate predictions
print("Accurate Predictions (Hits):")
for hit in accurate_predictions:
    print(hit.strftime('%Y-%m-%d %H:%M:%S'))

# Print the benchmark results
benchmark_results = {
    "Total Predictions": len(predictions_dt),
    "Total Actual Alerts": len(actual_alerts_dt),
    "Hits": len(accurate_predictions),
    "False Alarms": len(false_alarm_predictions),
    "Omissions": omissions,
    "Accuracy": f'{accuracy*100:.2f}%',
    "Precision": f'{precision*100:.2f}%',
}

benchmark_df = pd.DataFrame([benchmark_results])
print(benchmark_df)
