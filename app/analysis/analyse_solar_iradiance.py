import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.fetch_data import DataFolderProcessor

# Function to get the absolute path of the data folder
def get_data_folder_path():
    current_file_path = os.path.abspath(__file__)
    parent_directory = os.path.dirname(os.path.dirname(current_file_path))
    data_folder_path = os.path.join(parent_directory, "data")
    return data_folder_path

# Load dataset from file
def load_dataset(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        st.error(f"File not found at path: {file_path}")
        return None

# Handle missing values
def handle_missing_values(data):
    st.subheader("Handling Missing Values")
    st.write("Number of missing values in each column:")
    st.write(data.isnull().sum())
    data = data.dropna()  # You can also use other methods like fillna()
    return data

# Analyze Solar Irradiance Patterns
def analyze_solar_irradiance_patterns():
    st.title("Analyze Solar Irradiance Patterns")

    # Specify file paths for the three regions directly
    processor = DataFolderProcessor()
    csv_files = processor.csv_files
    # Specify file paths for the three regions directly
    file_paths = {
        "Benin-Malanville": os.path.join(processor.data_folder_path, "cleaned_cleaned_benin-malanville.csv"),
        "Sierra Leone-Bumbuna": os.path.join(processor.data_folder_path, "cleaned_cleaned_sierraleone-bumbuna.csv"),
        "Togo-Dapaong_QC": os.path.join(processor.data_folder_path, "cleaned_cleaned_togo-dapaong_qc.csv")
    }
    print(file_paths)  # Print file paths for debugging

    # Select a region to analyze
    selected_region = st.selectbox("Select Region", list(file_paths.keys()))

    # Load and preprocess the selected dataset
    data = load_dataset(file_paths[selected_region])

    # Check if 'Timestamp' column exists in the dataset
    if data is not None and "Timestamp" in data.columns:
        # Exclude 'Timestamp', 'Comments', and 'ModA' columns from the dropdown options
        excluded_columns = ["Timestamp", "Comments"]
        selectable_columns = [col for col in data.columns if col not in excluded_columns]

        # Handle missing values
        data = handle_missing_values(data)

        # Calculate summary statistics for the dataset
        st.subheader("Summary Statistics")
        stats = data.describe()
        st.write(stats)

        # Create a single select dropdown for choosing the solar irradiance column
        selected_column = st.selectbox("Select Solar Irradiance Column", selectable_columns)

        # Perform time series analysis for the selected solar irradiance column
        st.subheader(f"Time Series Analysis for {selected_column}")
        time_series_analysis(data, "Timestamp", selected_column)

        # Display correlation matrix
        st.subheader("Correlation Matrix")
        corr_matrix = data.corr()

        # Plot the heatmap
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        # Plot histograms
        st.subheader("Histograms")
        for col in selectable_columns:
            st.write(f"Histogram for {col}")
            fig, ax = plt.subplots()
            ax.hist(data[col].dropna(), bins=30)
            ax.set_title(f"Histogram for {col}")
            st.pyplot(fig) 

    else:
        st.error("Timestamp column not found in the dataset.")

# Time Series Analysis Function
def time_series_analysis(data, time_column, column1):
    data[time_column] = pd.to_datetime(data[time_column])
    data.set_index(time_column, inplace=True)

    fig, ax = plt.subplots()
    ax.plot(data.index, data[column1])
    ax.set_xlabel(time_column)
    ax.set_ylabel(column1)

    st.pyplot(fig)

# Main function to run the app
def main():
    analyze_solar_irradiance_patterns()

# Run the app
if __name__ == "__main__":
    main()