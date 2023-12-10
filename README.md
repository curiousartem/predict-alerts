# ARAPS (Air Raid Alert Prediction System)

## Overview

This project provides a set of tools for predicting air raid alerts in Ukraine. It uses historical data to train a [GBM (Gradient Boosting Model)](https://en.wikipedia.org/wiki/Gradient_boosting) that can forecast the likelihood of future air raid alerts. The system is designed to be interactive, allowing users to specify parameters for both training and prediction processes.

The project consists of three Python scripts:

- `predict.py`: For making predictions using a pre-trained model.
- `train.py`: For training the model on historical air raid alert data.
- `erase-models.py`: For deleting all pre-trained models from the system.

Additionally, there is a `models/` folder intended to store the trained models.

## Quick Start

1. Clone the repository to your local machine.
2. Ensure you have Python 3.6+ installed.
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Run `train.py` to train a new model based on the latest data.
5. Use `predict.py` to make predictions with the trained model.
6. If needed, run `erase-models.py` to remove all models from the `models/` directory.

## Requirements

Before running the scripts, you must have the following packages installed:

- pandas
- joblib
- tqdm
- xgboost
- requests

You can install these packages using `pip`:

```sh
pip install pandas joblib tqdm xgboost requests
```

## Usage

### Training the Model

Run `train.py` from the command line to start the training process. The script will prompt you to provide a date from which to train the model, and a specific region to focus on, and the filename for the model. After training, it will save the model to the `models/` directory with the provided filename or a randomly generated one.

### Making Predictions

Execute `predict.py` to use a trained model for predictions. You will be asked to provide the model filename and other parameters such as the current date and the number of days to predict. The script will then display the predicted high-probability alert times.

### Erasing Models

When you run `erase-models.py`, it will ask for confirmation before deleting all files within the `models/` directory. This is useful for clearing out old models.

## Project Structure

- `predict.py`: Contains the logic for loading a trained model and making predictions.
- `train.py`: Handles the downloading of the dataset, preprocessing, training the model, and saving it.
- `erase-models.py`: Provides a simple script to clear all trained models.
- `models/`: A directory intended to store trained model files.

## How It Works

ARAPS operates by utilizing historical air raid alert data to train a machine learning model, which can then predict the likelihood of future alerts. Here's a breakdown of how each component of the system contributes to its overall operation:

### Data Acquisition and Preprocessing

The system begins with the acquisition of historical air raid data. This data is obtained via a URL pointing to a dataset, typically in CSV format, which contains records of past air raid alerts. The `train.py` script is responsible for downloading this dataset.

Once downloaded, the data is preprocessed to be suitable for machine learning. This involves:

- Converting timestamps to a datetime format.
- Resampling the data to an hourly frequency to count the number of alerts within each hour.
- Filling in missing values to ensure a continuous timeline.
- Extracting time-related features such as the hour of the day and the day of the week, which are crucial for the model to identify patterns.

### Model Training

The preprocessed data is used to train a Gradient Boosting Machine (GBM) model, specifically an implementation provided by the XGBoost library. This model is chosen for its effectiveness in handling tabular data and its ability to capture complex nonlinear relationships.

The training process involves:

- Splitting the data into features (the time-related aspects) and the target variable (the number of alerts).
- Feeding this data into the XGBoost model, which learns to predict the target variable based on the features.
- The model learns by minimizing the difference between its predictions and the actual number of alerts, adjusting its internal parameters accordingly.

### Model Prediction

With a trained model, the `predict.py` script is used to make predictions:

- The user specifies the current date and the number of days into the future for which to predict air raid alerts.
- The script generates features for the specified time period (the next 7 days by default), considering the hour and the day of the week for each time slot.
- The trained model uses these features to predict the likelihood of an air raid alert for each hour in the prediction range.

### Thresholding and Alert Prediction

To determine which times are most likely to have an air raid alert, a threshold is applied:

- Predictions that represent the likelihood of an alert are filtered by a threshold, which is set at the 90th percentile by default. This means only the top 10% of predictions with the highest likelihood are considered as potential alerts.
- Users can adjust this threshold to be more or less conservative based on their needs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project was created by Artem.
- Special thanks to [Vadym Klymenko](https://github.com/Vadimkin) for the [Ukrainian air raid sirens dataset,](https://github.com/Vadimkin/ukrainian-air-raid-sirens-dataset) which is used to train the models.

## Support

For support, please open an issue on the project's GitHub repository.

## Contributing

Contributions are welcome. Please read `CONTRIBUTING.md` for details on how to contribute to this project.

## Contact

For any queries or further assistance, please contact Artem at [artem@curiousity.one](mailto:artem@curiousity.one).

---

Copyright (c) 2023 Artem Curious. All rights reserved.