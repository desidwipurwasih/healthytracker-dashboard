import streamlit as st
import pandas as pd
from food_data import load_data, append_data, overwrite_data
from datetime import date

st.set_page_config(page_title="HealthyTracker", layout="wide")
st.title("🥗 HealthyTracker Dashboard")

st.sidebar.header("Tambah Catatan Makan")
with st.sidebar.form("input_form"):
    input_date = st.date_input("Tanggal", value=date.today())
    input_food = st.text_input("Nama Makanan")
    input_portion = st.number_input("Porsi", min_value=1, value=1)
    input_calories = st.number_input("Kalori per Porsi", min_value=0)
    submitted = st.form_submit_button("Tambah Data")

    if submitted:
        new_data = [str(input_date), input_food, input_portion, input_calories]
        append_data(new_data)
        st.success("Data berhasil ditambahkan!")

df = load_data()

st.subheader("📋 Data Konsumsi Harian")
edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

if st.button("💾 Simpan Perubahan"):
    overwrite_data(edited_df)
    st.success("Perubahan berhasil disimpan.")

# Visualisasi Kalori
st.subheader("📈 Visualisasi Kalori")
if not df.empty:
    df['Calories'] = pd.to_numeric(df['Calories'])
    df['Portion'] = pd.to_numeric(df['Portion'])
    df['Date'] = pd.to_datetime(df['Date'])

    df['Total_Calories'] = df['Portion'] * df['Calories']
    
    st.line_chart(df.groupby('Date')['Total_Calories'].sum())

    st.bar_chart(df.groupby('Food')['Total_Calories'].sum())
else:
    st.info("Belum ada data konsumsi yang dimasukkan.")
