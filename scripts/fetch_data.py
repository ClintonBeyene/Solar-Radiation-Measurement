import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

class DataFolderProcessor:
    
    def __init__(self, folder_name='app/data'):
        self.current_directory = os.getcwd()
        self.data_folder_path = os.path.join(self.current_directory, folder_name)
        self.csv_files = [f for f in os.listdir(self.data_folder_path) if f.endswith('.csv')]

    def process_file(self, csv_file):
        file_path = os.path.join(self.data_folder_path, csv_file)
        df = pd.read_csv(file_path)
        return df
