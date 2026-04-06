import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.header("Filter Data")
    
    min_date = day_df["dteday"].min()
    max_date = day_df["dteday"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

st.title('Bike Sharing Analysis Dashboard 🚲')

col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df.cnt.sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")
with col2:
    avg_rentals = round(main_df.cnt.mean())
    st.metric("Rata-rata Harian", value=avg_rentals)
with col3:
    max_rentals = main_df.cnt.max()
    st.metric("Penyewaan Tertinggi", value=f"{max_rentals:,}")

st.divider()

st.subheader('Grafik 1: Tren Penyewaan Bulanan')
main_df['month'] = main_df['dteday'].dt.to_period('M')
monthly_df = main_df.groupby('month').agg({"cnt": "sum"}).reset_index()
monthly_df['dteday'] = monthly_df['month'].dt.strftime('%b-%y')

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_df["dteday"], monthly_df["cnt"], marker='o', linewidth=2, color="#72BCD4")
ax.set_title("Total Penyewaan Per Bulan", fontsize=15)
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader('Grafik 2: Pola Penyewaan Berdasarkan Jam')
hourly_avg = hour_df.groupby("hr").cnt.mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="hr", y="cnt", data=hourly_avg, color="#72BCD4", ax=ax)
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Rata-rata Penyewa")
st.pyplot(fig)

st.caption('Copyright (c) Willy Aldo - Project Fudamental Analisis Data Dicoding 2026')