import streamlit as st
from utils import time_series_analysis
from analysis.correlation_analysis import correlation_analysis
from analysis.analyse_solar_iradiance import analyze_solar_irradiance_patterns
import pandas as pd

def main():
    st.title("MoonLight Energy Solutions Data Analysis Dashboard")
    st.text("To identifying high-potential regions for solar installation and enhancing operational efficiency and sustainability")
    st.subheader("- Time Series Analysis")
    st.subheader("- Correlation Analysis")
    st.subheader("- Analyze Solar Irradiance Patterns")

    # Perform time series analysis
    time_series_analysis()
     
    # correlation analysis
    correlation_analysis()
    
    # analyze_solar_irradiance_patterns
    analyze_solar_irradiance_patterns()


if __name__ == "__main__":
    main()

