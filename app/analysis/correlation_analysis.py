import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gdown

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


def correlation_analysis():
    st.title("Correlation Analysis")

    # Specify file paths for the three regions directly
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
                data = pd.read_csv(output)

                # Remove the 'Comments' column if it exists
                if 'Comments' in data.columns:
                    data = data.drop(columns=['Comments'])

                if "Timestamp" in data.columns:
                    # Convert the 'Timestamp' column to datetime objects (using the correct format)
                    data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%Y-%m-%d %H:%M:%S')

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
