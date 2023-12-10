# Before you read

## Metrics

Here are the definitions of the metrics used to evaluate the model(s)/their versions:

- **Total Predictions**: The total number of alerts predicted by the model.
- **Total Actual Alerts**: The total number of actual air raid alerts that occurred.
- **Hits (Accurate Predictions)**: The number of predictions that correctly matched the actual alerts.
- **False Alarms**: The number of predictions that did not correspond to any actual alert.
- **Omissions**: The number of actual alerts that the model failed to predict.
- **Accuracy**: The ratio of hits to the total number of actual alerts (redefined for this specific context).
- **Precision**: The ratio of hits to the total number of predictions made by the model.

# 🛠️ Benchmarks

# Benchmark Results (10th of December, 2023) - 2 & 3

This model update features multiple performance and other updates. This update features the improvement of prediction accuracy and precision up to ~36%.
> ⚠️ **Warning:** Please note that all models generated with an older version will break, as this update contains breaking changes and you will face compatibility issues when trying to predict with an older model.

## Data and Prediction Timeframe

The data used for benchmarking was collected from November 1, 2023, up until November 30, 2023. The benchmark calculations were performed with the current date set as December 1st, 2023, and predictions were calculated for the subsequent 7 days.
Data about existing air raid alerts was taken from [https://kyiv.digital/storage/air-alert/stats.html](https://kyiv.digital/storage/air-alert/stats.html).

## Updated Benchmark Results

The following results were obtained from the latest run of the benchmark script (the model used is available at `benchmarks/benchmark-model-3.pkl`):

| Total Predictions | Total Actual Alerts | Hits | False Alarms | Omissions | Accuracy  | Precision |
|-------------------|---------------------|------|--------------|-----------|-----------|-----------|
| 17                | 14                  | 5 ✨  | 12 ✨        | 9 ✨      | 35.71% ✨ | 29.41% ✨  |

## Analysis

The updated model has shown significant improvement in prediction accuracy and precision, with an accuracy of 35.71% and a precision of 29.41%. This indicates that the model now correctly predicts actual alerts approximately 35.71% of the time, with a higher precision rate.

This is a huge improvement from the previous model accuracy of only 21.43% and a precision of 17.65%.

The changes made that impacted this improvement were the addition of code that calculated seasonal data and provided it to the model in the training. This impacted the model's performance crucially as GBM models perform better when more data is given for the model to rely on. In next updates, even more data will be provided like patterns of air raid alerts because of specific dangers, like MiG-31k departures which often have a pattern that the model can rely on.

---

# Benchmark Results (10th of December, 2023)

This document provides an overview of the benchmark results for the Air Raid Alert Prediction System. The benchmarks are designed to evaluate the performance of the predictive model in terms of its ability to accurately forecast air raid alerts.

## Benchmarking Methodology

The benchmarking process involves running the model against a set of historical data to simulate the prediction of air raid alerts. The model's predictions are then compared to actual historical events to determine the accuracy, precision, and recall of the model.

## Data and Prediction Timeframe

The data used for benchmarking was collected from November 1, 2023, up until November 30, 2023. The benchmark calculations were performed with the current date set as November 30, 2023, and predictions were calculated for the subsequent 7 days.
Data about existing air raid alerts was taken from [https://kyiv.digital/storage/air-alert/stats.html](https://kyiv.digital/storage/air-alert/stats.html).

## Current Benchmark Results

The following results were obtained from the latest run of the benchmark script (the model used is available at `benchmarks/benchmark-model-1.pkl`):

| Total Predictions | Total Actual Alerts | Hits | False Alarms | Omissions | Accuracy | Precision | Recall |
|-------------------|---------------------|------|--------------|-----------|----------|-----------|--------|
| 17                | 14                  | 3    | 14           | 11        | 21.43%   | 17.65%    | 21.43% |

## Analysis

The current model has an accuracy of 21.43%, with a precision of 17.65% and a recall of 21.43%. This indicates that the model correctly predicts an actual alert approximately 21.43% of the time. However, there is a high number of false alarms and omissions, suggesting that the model's reliability for predicting air raid alerts is low in its current state. Please note that this project is currently in its early development stages and generated model quality will be improved over time.
