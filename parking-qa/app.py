import pandas as pd
import streamlit as st

df = pd.read_csv('parking_observations.csv')

st.title('Parking Observation QA Dashboard')
st.dataframe(df)
