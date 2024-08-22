import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats 
import matplotlib.pyplot as mpl

def fetch_data(data):
    dataframe =pd.read_csv(data)
    return dataframe