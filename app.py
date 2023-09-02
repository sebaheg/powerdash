import requests
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Powerdash",
    page_icon="⚡",
    layout="wide",
)

# read csv from a URL
@st.cache_data
def get_production_data(zone, variables, API_key): 
    end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_date = (datetime.now()-timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S')
    headers = {'Authorization': API_key}
    params = {'start-date': start_date, 'end-date': end_date}
    url = 'https://api.rebase.energy/energy/production/{0}/'.format(zone)

    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    data = {variable: [] for variable in variables}
    time_stamp = []
    for record in result['records']:
        for variable in variables: 
            data[variable].append(record['production'][variable])
        time_stamp.append(record['timestamp'])

    df = pd.DataFrame(index=time_stamp, data=data)
    df.index = pd.to_datetime(df.index)

    return df

API_key = 'A05Bru6X2w08Us4SI3Et2tN4SP9ZebZJ7B8OYfXhMrr'
df = get_production_data("SE-SE3", ["wind", "solar"], API_key)

st.title("⚡ Powerdash")

placeholder = st.empty()

with placeholder.container():


    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.markdown("### Solar Power in SE3 [MW]")
        fig1 = px.line(df, x=df.index, y="solar", color_discrete_sequence=["yellow"])
        st.write(fig1)

    
    with fig_col2:
        st.markdown("### Wind Power in SE3 [MW]")
        fig2 = px.line(df, x=df.index, y="wind", color_discrete_sequence=["yellow"])
        st.write(fig2)