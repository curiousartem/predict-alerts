from datetime import datetime, timedelta
import numpy as np

# Raw predictions with potential duplicates
raw_predictions = [
    "2023-12-01 00:00:00", "2023-12-07 00:00:00",
    "2023-12-02 00:00:00", "2023-12-02 22:00:00",
    "2023-12-02 12:00:00", "2023-12-06 12:00:00",
    "2023-12-01 12:00:00", "2023-12-07 12:00:00",
    "2023-12-04 00:00:00", "2023-12-05 00:00:00",
    "2023-12-06 00:00:00", "2023-12-03 00:00:00",
    "2023-12-03 12:00:00", "2023-12-04 12:00:00",
    "2023-12-05 12:00:00", "2023-12-05 10:00:00",
    "2023-12-04 10:00:00",
]

# Convert to datetime objects and sort
prediction_datetimes = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in raw_predictions]
prediction_datetimes.sort()

# Group by date and calculate average time
grouped_predictions = {}
for pred in prediction_datetimes:
    date_key = pred.date()
    if date_key not in grouped_predictions:
        grouped_predictions[date_key] = []
    grouped_predictions[date_key].append(pred)

# Calculate average time for each date
averaged_predictions = []
for date, times in grouped_predictions.items():
    avg_hour = np.mean([t.hour + t.minute / 60.0 for t in times])
    avg_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=avg_hour)
    averaged_predictions.append(avg_time.strftime("%Y-%m-%d %H:%M:%S"))

# Sort the final averaged predictions
averaged_predictions.sort()

# Now the predictions array contains one alert per day, with the time being the average
predictions = averaged_predictions

# Output the processed predictions
print("Processed predictions with one alert per day:")
print(predictions)