import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder

def load_furniture_data():
    if not os.path.isfile("data-transaksi2.csv"):
        df = pd.DataFrame(columns=["date_time", "Transaction", "Item"])
        df.to_csv("data-transaksi2.csv", index=False)
    else:
        df = pd.read_csv("data-transaksi2.csv")
    return df

def append_transaction_data(data):
    df = pd.read_csv("data-transaksi2.csv")
    data["Transaction"] = 1  # Set Transaction to 1 for all entries
    df = pd.concat([df, data], ignore_index=True)
    df.to_csv("data-transaksi2.csv", index=False)

def load_item_names():
    if not os.path.isfile("data_barang.csv"):
        st.error("data_barang.csv file not found!")
        return []
    else:
        df = pd.read_csv("data_barang.csv")
        return df['nama_barang'].tolist()

def update_item_stock(item_name):
    df = pd.read_csv("data_barang.csv")
    if item_name in df['nama_barang'].values:
        # Mengurangi stok barang
        df.loc[df['nama_barang'] == item_name, 'stok'] -= 1
        # Menyimpan perubahan kembali ke file CSV
        df.to_csv("data_barang.csv", index=False)
    else:
        st.error(f"Item '{item_name}' not found in data_barang.csv")

def show_add_transaction_page():
    st.title("Tambah transaksi")

    with st.form(key='furniture_form'):
        date = st.date_input('date_time')
        item_names = load_item_names()
        if not item_names:
            st.error("No items available in data_barang.csv.")
            return
        item = st.selectbox('nama_barang', item_names)
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        new_data = {
            "date_time": [date],
            "Transaction": [1],  # Always set to 1
            "Item": [item],
        }
        new_data_df = pd.DataFrame(new_data)
        append_transaction_data(new_data_df)
        update_item_stock(item)
        st.success('Data has been added successfully!')
        st.write(new_data_df)

def show_data():
    st.title("Data Transaksi")
    df = load_furniture_data()
    
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
    df = df.sort_values(by='date_time', ascending=False)
    
    # Remove the 'Transaction' column before displaying
    df = df.drop(columns=['Transaction'])

    # Gunakan AgGrid untuk menampilkan tabel dengan pagination
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=5)
    gridOptions = gb.build()

    st.write("Report Data Transaction:")
    AgGrid(df, gridOptions=gridOptions, height=300, fit_columns_on_grid_load=True)
