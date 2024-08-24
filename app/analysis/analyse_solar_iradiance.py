import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import gdown

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
    file_paths = {
        "Benin-Malanville": "https://drive.google.com/uc?export=download&id=17iGCuwUFAVBt1imW6btaBQ1LiFgavX7U",
        "Sierra Leone-Bumbuna": "https://drive.google.com/uc?export=download&id=1WeJLspjEoQi8lOThfk_WDgMjNlRm9m_j",
        "Togo-Dapaong_QC": "https://drive.google.com/uc?export=download&id=11du5qHBELTV1is2jIJbBk13qcTSuT-nj"
    }

    # Select a region to analyze
    selected_region = st.selectbox("Select Region", list(file_paths.keys()))

    # Download the file from Google Drive
    output = f"{selected_region}.csv"
    gdown.download(file_paths[selected_region], output, quiet=False)

    # Load and preprocess the selected dataset
    data = load_dataset(output)

    # Check if 'Timestamp' column exists in the dataset
    if data is not None and "Timestamp" in data.columns:
        # Remove 'Comments' column if it exists
        if 'Comments' in data.columns:
            data = data.drop(columns=['Comments'])

        # Exclude 'Timestamp' from the dropdown options
        selectable_columns = [col for col in data.columns if col != "Timestamp"]
        
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

        # Convert the 'Timestamp' column to datetime objects (using the correct format)
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%Y-%m-%d %H:%M:%S') 

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

def main():
    analyze_solar_irradiance_patterns()

if __name__ == "__main__":
    main()
