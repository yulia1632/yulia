import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("ev_charging_stations.csv")  # Replace with your file

# Initialize session state for user ID
if "ID" not in st.session_state:
    st.session_state["ID"] = "Noname"

ID = st.session_state["ID"]

# Sidebar greeting
with st.sidebar:
    st.caption(f"{ID}님 접속중")

# User input form for filtering
with st.form("input"):
    region = st.multiselect("도시", data['Station Name'].apply(lambda x: x.split()[0]).unique(), help="도시를 선택하세요")
    charger_type = st.multiselect("충전기 종류", data['Charger Type'].unique(), help="충전기 종류를 선택하세요")
    capacity = st.slider("최소 충전기 용량 (개수)", min_value=0, max_value=10, value=0, step=1)
    submitted = st.form_submit_button("조회")

    if submitted:
        # Filter data based on user input
        filtered_data = data.copy()
        
        if region:
            filtered_data = filtered_data[filtered_data['Station Name'].apply(lambda x: x.split()[0]).isin(region)]
        
        if charger_type:
            filtered_data = filtered_data[filtered_data['Charger Type'].isin(charger_type)]
        
        filtered_data = filtered_data[
            (filtered_data['Fast Chargers'] >= capacity) | 
            (filtered_data['Standard Chargers'] >= capacity)
        ]
        
        if not filtered_data.empty:
            # Prepare data for visualization
            result = filtered_data.groupby(['Station Name', 'Charger Type']).agg({
                'Fast Chargers': 'sum',
                'Standard Chargers': 'sum'
            }).reset_index()

            # Plot the data
            st.subheader("충전소별 충전기 용량")
            st.dataframe(filtered_data)
            fig, ax = plt.subplots(figsize=(10, 6))
            result.plot(
                kind='bar',
                x='Station Name',
                y=['Fast Chargers', 'Standard Chargers'],
                stacked=True,
                ax=ax
            )
            ax.set_title("충전소별 충전기 용량")
            ax.set_ylabel("충전기 개수")
            ax.set_xlabel("충전소")
            st.pyplot(fig)
        else:
            st.warning("선택한 조건에 맞는 데이터가 없습니다.") 