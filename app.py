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
def get_production_data(zone, variables): 
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

@st.cache_data
def get_consumption_data(zone):     
    url = 'https://api.rebase.energy/energy/consumption/{0}/'.format(zone)
    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    consumption, time_consumption = [], []
    for record in result['records']:
        consumption.append(record['consumption'])
        time_consumption.append(record['timestamp'])

    df_consumption = pd.DataFrame(index=time_consumption, data={"consumption": consumption})
    df_consumption.index = pd.to_datetime(df_consumption.index)

    url = 'https://api.rebase.energy/energy/consumption-forecast/{0}/'.format(zone)
    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    forecast, time_forecast = [], []
    for record in result['records']:
        forecast.append(record['value'])
        time_forecast.append(record['timestamp'])

    df_forecast = pd.DataFrame(index=time_forecast, data={"forecast": forecast})
    df_forecast.index = pd.to_datetime(df_forecast.index)

    df = pd.concat([df_consumption, df_forecast], axis=1)
    
    return df

@st.cache_data
def get_exchange_data(zone):     
    url = 'https://api.rebase.energy/energy/exchange/{0}/'.format(zone)
    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    exchange, time_exchange = [], []
    for record in result['records']:
        exchange.append(record['netFlow'])
        time_exchange.append(record['timestamp'])

    df_exchange = pd.DataFrame(index=time_exchange, data={"exchange": exchange})
    df_exchange.index = pd.to_datetime(df_exchange.index)

    url = 'https://api.rebase.energy/energy/exchange-forecast/{0}/'.format(zone)
    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    forecast, time_forecast = [], []
    for record in result['records']:
        forecast.append(record['netFlow'])
        time_forecast.append(record['timestamp'])

    df_forecast = pd.DataFrame(index=time_forecast, data={"forecast": forecast})
    df_forecast.index = pd.to_datetime(df_forecast.index)

    df = pd.concat([df_exchange, df_forecast], axis=1)
    
    return df


now = datetime.now()
end_date = (now+timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
start_date = (now-timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S')
params = {'start-date': start_date, 'end-date': end_date}

API_key = 'A05Bru6X2w08Us4SI3Et2tN4SP9ZebZJ7B8OYfXhMrr'
headers = {'Authorization': API_key}

df_production = get_production_data("SE-SE3", ["wind", "solar"])
df_consumption = get_consumption_data("SE-SE3")
df_exchange = get_exchange_data("SE-SE2___SE-SE3")

st.title("⚡ Powerdash")

placeholder = st.empty()

with placeholder.container():


    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.markdown("### Solar Power in SE3 [MW]")
        fig11 = px.line(df_production, x=df_production.index, y="solar", color_discrete_sequence=["yellow"])
        st.write(fig11)

        st.markdown("### Consumption in SE3 [MW]")
        fig1 = px.line(df_consumption, x=df_consumption.index, y=["consumption", "forecast"], color_discrete_sequence=["red", "orange"])
        st.write(fig1)
    
    with fig_col2:
        st.markdown("### Wind Power in SE3 [MW]")
        fig12 = px.line(df_production, x=df_production.index, y="wind", color_discrete_sequence=["yellow"])
        st.write(fig12)

        st.markdown("### Exchange between SE2-SE3 [MW]")
        fig22 = px.line(df_exchange, x=df_exchange.index, y=["exchange", "forecast"], color_discrete_sequence=["red", "orange"])
        st.write(fig22)