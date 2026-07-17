import sqlite3, subprocess, sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT=Path(__file__).parent
DB=ROOT/'airline_operations.db'
st.set_page_config(page_title='United Airlines Operations Dashboard', page_icon='✈️', layout='wide')

@st.cache_resource
def get_connection():
    if not DB.exists():
        subprocess.run([sys.executable, str(ROOT/'generate_data.py')], check=True)
        subprocess.run([sys.executable, str(ROOT/'setup_database.py')], check=True)
    return sqlite3.connect(DB, check_same_thread=False)

def query(sql, params=None):
    return pd.read_sql_query(sql, get_connection(), params=params or [])

def build_filters(months, airlines, airports):
    conditions=[]; params=[]
    for column, values in [('month',months),('airline',airlines),('origin_airport',airports)]:
        if values:
            conditions.append(f"{column} IN ({','.join('?' for _ in values)})")
            params.extend(values)
    return (' WHERE '+' AND '.join(conditions) if conditions else ''), params

def add_condition(where, condition):
    return where + ' AND ' + condition if where else ' WHERE ' + condition

options=query('SELECT DISTINCT month, airline, origin_airport FROM flight_operations')
months=sorted(options['month'].unique()); airlines=sorted(options['airline'].unique()); airports=sorted(options['origin_airport'].unique())

st.title('United Airlines Operations Dashboard')
st.caption('SQL-powered airline operations portfolio project using simulated flight data. This project is not affiliated with United Airlines.')

with st.sidebar:
    st.header('Dashboard Filters')
    selected_months=st.multiselect('Month', months, months)
    selected_airlines=st.multiselect('Airline', airlines, airlines)
    selected_airports=st.multiselect('Origin Airport', airports, airports)

where, params=build_filters(selected_months, selected_airlines, selected_airports)
if not selected_months or not selected_airlines or not selected_airports:
    st.warning('Select at least one month, airline, and airport.'); st.stop()

kpis=query(f'''SELECT
ROUND(100.0*SUM(CASE WHEN cancelled=0 AND arrival_delay_minutes<=15 THEN 1 ELSE 0 END)/NULLIF(SUM(CASE WHEN cancelled=0 THEN 1 ELSE 0 END),0),2) AS on_time_pct,
ROUND(AVG(CASE WHEN cancelled=0 THEN arrival_delay_minutes END),2) AS average_delay,
SUM(cancelled) AS cancelled_flights
FROM flight_operations {where}''', params).iloc[0]

most_delayed=query(f'''SELECT origin_airport, ROUND(AVG(arrival_delay_minutes),2) AS average_delay
FROM flight_operations {add_condition(where,'cancelled=0')}
GROUP BY origin_airport ORDER BY average_delay DESC LIMIT 1''', params)

st.subheader('Top KPIs')
cols=st.columns(4)
cols[0].metric('On-Time %', f"{kpis['on_time_pct']:.2f}%")
cols[1].metric('Average Delay', f"{kpis['average_delay']:.1f} min")
cols[2].metric('Cancelled Flights', f"{int(kpis['cancelled_flights']):,}")
cols[3].metric('Most Delayed Airport', most_delayed.iloc[0]['origin_airport'] if not most_delayed.empty else 'N/A')

reasons=query(f'''SELECT delay_reason, COUNT(*) AS delayed_flights
FROM flight_operations {add_condition(where,'cancelled=0 AND arrival_delay_minutes>15')}
GROUP BY delay_reason ORDER BY delayed_flights DESC''', params)
by_airline=query(f'''SELECT airline, ROUND(AVG(arrival_delay_minutes),2) AS average_delay
FROM flight_operations {add_condition(where,'cancelled=0')}
GROUP BY airline ORDER BY average_delay DESC''', params)
left,right=st.columns(2)
with left:
    st.plotly_chart(px.bar(reasons,x='delay_reason',y='delayed_flights',text_auto=True,title='Delay Reasons'),use_container_width=True)
with right:
    st.plotly_chart(px.bar(by_airline,x='airline',y='average_delay',text_auto='.1f',title='Delays by Airline'),use_container_width=True)

by_month=query(f'''SELECT month, ROUND(AVG(arrival_delay_minutes),2) AS average_delay
FROM flight_operations {add_condition(where,'cancelled=0')}
GROUP BY month ORDER BY month''', params)
st.plotly_chart(px.line(by_month,x='month',y='average_delay',markers=True,title='Delays by Month'),use_container_width=True)

top_airports=query(f'''SELECT origin_airport, COUNT(*) AS total_flights,
ROUND(AVG(arrival_delay_minutes),2) AS average_delay,
ROUND(100.0*SUM(CASE WHEN arrival_delay_minutes>15 THEN 1 ELSE 0 END)/COUNT(*),2) AS delayed_flight_pct
FROM flight_operations {add_condition(where,'cancelled=0')}
GROUP BY origin_airport HAVING COUNT(*)>=20
ORDER BY average_delay DESC LIMIT 10''', params)
st.subheader('Top 10 Most Delayed Airports')
st.plotly_chart(px.bar(top_airports.sort_values('average_delay'),x='average_delay',y='origin_airport',orientation='h',text_auto='.1f',title='Top 10 Airports'),use_container_width=True)

scorecard=query(f'''SELECT origin_airport AS Airport, COUNT(*) AS Flights,
ROUND(100.0*SUM(CASE WHEN cancelled=0 AND arrival_delay_minutes<=15 THEN 1 ELSE 0 END)/NULLIF(SUM(CASE WHEN cancelled=0 THEN 1 ELSE 0 END),0),2) AS "On-Time %",
ROUND(AVG(CASE WHEN cancelled=0 THEN arrival_delay_minutes END),2) AS "Average Delay",
SUM(cancelled) AS Cancellations
FROM flight_operations {where}
GROUP BY origin_airport ORDER BY Flights DESC''', params)
st.subheader('Airport Performance Scorecard')
st.dataframe(scorecard,use_container_width=True,hide_index=True)

st.subheader('Operations Manager Insights')
status='🔴' if kpis['on_time_pct']<75 else ('🟡' if kpis['on_time_pct']<85 else '🟢')
st.info(f"{status} On-time performance is {kpis['on_time_pct']:.1f}%.")
if not reasons.empty:
    st.info(f"🟠 {reasons.iloc[0]['delay_reason']} is the leading delay reason with {int(reasons.iloc[0]['delayed_flights']):,} delayed flights.")
if not top_airports.empty:
    st.info(f"✈️ {top_airports.iloc[0]['origin_airport']} has the highest average delay at {top_airports.iloc[0]['average_delay']:.1f} minutes.")
if int(kpis['cancelled_flights'])>0:
    st.info(f"🔴 {int(kpis['cancelled_flights']):,} flights were cancelled in the selected period.")
