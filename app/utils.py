import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import seaborn as sns
import sys
os.getcwd()
os.path.abspath("../")
sys.path.insert(0, os.path.abspath("./"))
from scripts.fetch_data import DataFolderProcessor

# Time Series Analysis Class
class TimeSeriesAnalysis:
    def __init__(self, df):
        self.df = df

    def analyze(self, time_column, column1):
        self.df[time_column] = pd.to_datetime(self.df[time_column])
        self.df.set_index(time_column, inplace=True)

        fig, ax = plt.subplots()
        ax.plot(self.df.index, self.df[column1])
        ax.set_xlabel(time_column)
        ax.set_ylabel(column1)

        st.pyplot(fig)

# Example usage
processor = DataFolderProcessor()
csv_files = processor.csv_files

def time_series_analysis():
    st.title("Time Series Analysis")

    # Specify file paths for the three regions directly
    file_paths = {
        "Benin-Malanville": os.path.join(processor.data_folder_path, "cleaned_cleaned_benin-malanville.csv"),
        "Sierra Leone-Bumbuna": os.path.join(processor.data_folder_path, "cleaned_cleaned_sierraleone-bumbuna.csv"),
        "Togo-Dapaong_QC": os.path.join(processor.data_folder_path, "cleaned_cleaned_togo-dapaong_qc.csv")
    }

    # Print the data folder path for debugging
    print("Data folder path:", processor.data_folder_path)

    # Create columns for each region's analysis horizontally
    col1, col2, col3 = st.columns(3)

    for idx, (region, file_path) in enumerate(file_paths.items(), start=1):
        with col1 if idx % 3 == 1 else col2 if idx % 3 == 2 else col3:
            st.subheader(region)
            try:
                # Print the file path for debugging
                print(f"Loading data from: {file_path}")
                data = pd.read_csv(file_path)

                if "Timestamp" in data.columns:
                    # Initialize TimeSeriesAnalysis class
                    ts_analysis = TimeSeriesAnalysis(data)

                    # Perform time series analysis
                    selectable_columns = [col for col in data.columns if col != "Timestamp"]
                    unique_key = f"{region}_{file_path}"

                    # Display select box for column selection
                    selected_column = st.selectbox(f"Select Column {region}", selectable_columns, key=unique_key)

                    # Analyze time series data based on selection
                    ts_analysis.analyze("Timestamp", selected_column)
                else:
                    st.write(f"Timestamp column not found in the dataset for {region}.")
            except FileNotFoundError:
                st.write(f"File not found at path: {file_path}")


def main():
    time_series_analysis()

if __name__ == "__main__":
    main()
