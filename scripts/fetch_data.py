import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

class DataFolderProcessor:
    
    def __init__(self, folder_name='app/data'):
        self.current_directory = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path of the current directory
        self.data_folder_path = os.path.join(self.current_directory, "..", folder_name)  # Construct the absolute path to the 'data' folder
        
        # Check if the directory exists
        if not os.path.exists(self.data_folder_path):
            os.makedirs(self.data_folder_path)
            print(f"Created directory: {self.data_folder_path}")
        
        self.csv_files = [f for f in os.listdir(self.data_folder_path) if f.endswith('.csv')]

    def process_file(self, csv_file):
        file_path = os.path.join(self.data_folder_path, csv_file)
        df = pd.read_csv(file_path)
        return df
    