import pandas as pd
import streamlit as st

df = pd.read_csv('parking-qa/parking_observations.csv')

df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(['spot_id', 'timestamp']).reset_index(drop=True)
df['prev_vehicle_present'] = df.groupby('spot_id')['vehicle_present'].shift(1)
df['prev_timestamp'] = df.groupby('spot_id')['timestamp'].shift(1)
df['time_since_prev'] = (df['timestamp'] - df['prev_timestamp']).dt.total_seconds() / 60

#Check for error situations
df['implausible_flip'] = (df['vehicle_present'] != df['prev_vehicle_present']) & (df['time_since_prev'] < 2)

df['low_confidence'] = df['confidence'] < 0.6

#Set Needs Review Message
df['needs_review'] = df['implausible_flip'] | df['low_confidence']

st.title('Parking Observation QA Dashboard')
#Set columns for visualization
col1, col2 = st.columns(2)
col1.metric('Total Records', len(df)) and col2.metric('Flagged for Review', int(df['needs_review'].sum()))
st.subheader('Flagged Records')
st.dataframe(df[df['needs_review']][['spot_id', 'timestamp', 'vehicle_present', 'obstruction', 'confidence', 'implausible_flip', 'low_confidence']])

st.subheader('Flagged Readings by Obstruction Type')
st.bar_chart(df[df['needs_review']]['obstruction'].value_counts())

st.dataframe(df)
