# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""
Prepares raw data and provides training and test datasets.
"""

import argparse
from pathlib import Path
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import mlflow

def parse_args():
    '''Parse input arguments'''

    parser = argparse.ArgumentParser("prep")  # Create an ArgumentParser object
    parser.add_argument("--raw_data", type=str, help="Path to raw data")  # Specify the type for raw data (str)
    parser.add_argument("--train_data", type=str, help="Path to train dataset")  # Specify the type for train data (str)
    parser.add_argument("--test_data", type=str, help="Path to test dataset")  # Specify the type for test data (str)
    parser.add_argument("--test_train_ratio", type=float, default=0.2, help="Test-train ratio")  # Specify the type (float) and default value (0.2) for test-train ratio
    args = parser.parse_args()

    return args

def main(args):  # Write the function name for the main data preparation logic
    '''Read, preprocess, split, and save datasets'''
    print(f"Raw data path: {args.raw_data}")
    print(f"Train dataset output path: {args.train_data}")
    print(f"Test dataset path: {args.test_data}")
    print(f"Test-train ratio: {args.test_train_ratio}")
    
    # Reading Data
    df = pd.read_csv(args.raw_data)

    # ------- WRITE YOUR CODE HERE -------

    # Step 1: Perform label encoding to convert categorical features into numerical values for model compatibility.  
    # Note: We should ideally use one-hot encoding here as there's no inherent order between the categories
    # However, as we're using a decision tree model, label encoding also works here
    label_encoder = LabelEncoder()
    df['Segment'] = label_encoder.fit_transform(df['Segment'])
    
    # Step 2: Split the dataset into training and testing sets using train_test_split with specified test size and random state.  
    train_df, test_df = train_test_split(df, test_size=args.test_train_ratio, random_state=42)

    # Step 3: Save the training and testing datasets as CSV files in separate directories for easier access and organization.  
    train_output_path = os.path.join(args.train_data, "train.csv")
    test_output_path = os.path.join(args.test_data, "test.csv")

    print(f"Saving training data to: {train_output_path}")
    print(f"Saving testing data to: {test_output_path}")

    train_df.to_csv(train_output_path, index=False)
    test_df.to_csv(test_output_path, index=False)

    # Step 4: Log the number of rows in the training and testing datasets as metrics for tracking and evaluation.  
    mlflow.log_metric('train size', train_df.shape[0])
    mlflow.log_metric('test size', test_df.shape[0])

if __name__ == "__main__":
    mlflow.start_run()

    # Parse Arguments
    args = parse_args()  # Call the function to parse arguments

    lines = [
        f"Raw data path: {args.raw_data}",  # Print the raw_data path
        f"Train dataset output path: {args.train_data}",  # Print the train_data path
        f"Test dataset path: {args.test_data}",  # Print the test_data path
        f"Test-train ratio: {args.test_train_ratio}",  # Print the test_train_ratio
    ]

    for line in lines:
        print(line)
    
    main(args)

    mlflow.end_run()
