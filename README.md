# United Airlines Operations Dashboard

## Overview

Interactive airline operations dashboard built with **Python, SQL, SQLite, Streamlit, Pandas, and Plotly**. It uses simulated U.S. flight data to analyze on-time performance, average delays, cancellations, delay reasons, airline comparisons, monthly trends, and airport-level operational risks.

> **Disclaimer:** Independent portfolio project using simulated data. Not affiliated with or endorsed by United Airlines or any other airline.

## Top KPIs
- On-Time Percentage
- Average Delay
- Cancelled Flights
- Most Delayed Airport

## Charts
- Delay Reasons
- Delays by Airline
- Delays by Month
- Top 10 Most Delayed Airports
- Airport Performance Scorecard

## Interactive Filters
- Month
- Airline
- Origin Airport

## Technologies Used
- Python
- SQL
- SQLite
- Streamlit
- Plotly
- Pandas

## Run the Project
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generate_data.py
python setup_database.py
streamlit run app.py
```

## Suggested Resume Bullet
Built a SQL and Streamlit airline operations dashboard analyzing more than 15,000 simulated flight records across on-time performance, cancellations, delay causes, airline comparisons, monthly trends, and airport-level risks.
