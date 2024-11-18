import streamlit as st
import pandas as pd

# Ensure session information is set
if "ID" not in st.session_state:
    st.session_state["ID"] = "Noname"

ID = st.session_state["ID"]

# Sidebar to display user info
with st.sidebar:
    st.caption(f"{ID}님 안녕하세요. 환영합니다!")

# Load and preprocess the dataset
# Replace 'ev_charging_stations.csv' with the actual file path for your data
data = pd.read_csv("ev_charging_stations.csv")
data = data.copy().fillna(0)

# Create a calculated column for bubble sizes
data['total_capacity'] = data['Fast Chargers'] * 500 + data['Standard Chargers'] * 4

# Map a color based on charger type
charger_color = {'Fast': '#09d99a', 'Standard': '#ebbb37', 'Mixed': '#42a5f5'}
data['color'] = data.copy()['Charger Type'].map(charger_color)

# Display map
st.title("전기차 충전소 현황")
st.map(data,
       latitude="Latitude",
       longitude="Longitude",
       size="total_capacity",
       color="color")

# Display data table (optional)
st.subheader("충전소 데이터")
st.dataframe(data)
