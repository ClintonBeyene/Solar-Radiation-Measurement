import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# Ensure the correct path for module imports
os.getcwd()
os.path.abspath("../")
sys.path.insert(0, os.path.abspath("./"))
from scripts.fetch_data import DataFolderProcessor

# Correlation Analysis Class
class CorrelationAnalysis:
    def __init__(self, df):
        self.df = df

    def analyze(self):
        # Calculate correlation matrix
        correlation_matrix = self.df.corr()

        # Plot correlation matrix
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        ax.set_title('Correlation Matrix')

        st.pyplot(fig)

# Example usage
processor = DataFolderProcessor()
csv_files = processor.csv_files

def correlation_analysis():
    st.title("Correlation Analysis")

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
                    # Drop the Timestamp column for correlation analysis
                    data = data.drop(columns=["Timestamp"])

                    # Initialize CorrelationAnalysis class
                    corr_analysis = CorrelationAnalysis(data)

                    # Perform correlation analysis
                    corr_analysis.analyze()
                else:
                    st.write(f"Timestamp column not found in the dataset for {region}.")
            except FileNotFoundError:
                st.write(f"File not found at path: {file_path}")

def main():
    correlation_analysis()

if __name__ == "__main__":
    main()
