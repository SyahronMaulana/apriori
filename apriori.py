import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import association_rules, apriori
import streamlit as st

df = pd.read_csv("data-transaksi2.csv")
df['date_time'] = pd.to_datetime(df['date_time'], format='%Y-%m-%d')

df['year_month_day'] = df['date_time'].dt.to_period('D')

df['year_month_day'].replace([i for i in range(1, 12 +1)], ["januari", "februari", "maret", "april", "mei", "juni", "juli", "agustus", "september", "oktober", "november", "desember"])

st.title("Apriori")