import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import seaborn as sns
import gdown
import sys

# Ensure the current working directory is correct
os.getcwd()
os.path.abspath("../")
sys.path.insert(0, os.path.abspath("./"))

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

def time_series_analysis():
    st.title("Time Series Analysis")

    # Specify file paths for the three regions directly (Google Drive links)
    file_paths = {
        "Benin-Malanville": "https://drive.google.com/uc?export=download&id=17iGCuwUFAVBt1imW6btaBQ1LiFgavX7U",
        "Sierra Leone-Bumbuna": "https://drive.google.com/uc?export=download&id=1WeJLspjEoQi8lOThfk_WDgMjNlRm9m_j",
        "Togo-Dapaong_QC": "https://drive.google.com/uc?export=download&id=11du5qHBELTV1is2jIJbBk13qcTSuT-nj"
    }

    # Create columns for each region's analysis horizontally
    col1, col2, col3 = st.columns(3)

    for idx, (region, file_path) in enumerate(file_paths.items(), start=1):
        with col1 if idx % 3 == 1 else col2 if idx % 3 == 2 else col3:
            st.subheader(region)
            try:
                # Download the file from Google Drive
                output = f"{region}.csv"
                gdown.download(file_path, output, quiet=False)

                # Load the data
                data = pd.read_csv(output, parse_dates=['Timestamp'])

                # Remove the 'Comments' column if it exists
                if 'Comments' in data.columns:
                    data = data.drop(columns=['Comments'])

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
