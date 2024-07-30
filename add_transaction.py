import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder

def load_furniture_data():
    if not os.path.isfile("data-transaksi2.csv"):
        df = pd.DataFrame(columns=["date_time", "Transaction", "Item", "qty"])
        df.to_csv("data-transaksi2.csv", index=False)
    else:
        df = pd.read_csv("data-transaksi2.csv")
    return df

def append_transaction_data(data):
    try:
        df = pd.read_csv("data-transaksi2.csv")
        df = pd.concat([df, data], ignore_index=True)
        df.to_csv("data-transaksi2.csv", index=False)
    except PermissionError:
        st.error("Permission denied while accessing data-transaksi2.csv. Please check file permissions.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def get_next_transaction_id():
    df = load_furniture_data()
    if df.empty:
        return 1
    else:
        return df['Transaction'].max() + 1

def load_item_names():
    if not os.path.isfile("data_barang.csv"):
        st.error("data_barang.csv file not found!")
        return []
    else:
        df = pd.read_csv("data_barang.csv")
        return df['nama_barang'].tolist()

def update_item_stock(item_names, quantities):
    try:
        df = pd.read_csv("data_barang.csv")
        for item_name, qty in zip(item_names, quantities):
            if item_name in df['nama_barang'].values:
                # Mengurangi stok barang
                df.loc[df['nama_barang'] == item_name, 'stok'] -= qty
            else:
                st.error(f"Item '{item_name}' not found in data_barang.csv")
        # Menyimpan perubahan kembali ke file CSV
        df.to_csv("data_barang.csv", index=False)
    except PermissionError:
        st.error("Permission denied while accessing data_barang.csv. Please check file permissions.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def show_add_transaction_page():
    st.title("Tambah transaksi")

    date = st.date_input('date_time')
    item_names = load_item_names()
    
    if not item_names:
        st.error("No items available in data_barang.csv.")
        return
    
    # Memungkinkan pemilihan beberapa item
    items = st.multiselect('Pilih barang', item_names)

    # Form input kuantitas muncul jika ada item yang dipilih
    if items:
        quantities = []
        for item in items:
            qty = st.number_input(f'Jumlah untuk {item}', min_value=1, value=1, step=1, key=item)
            quantities.append(qty)

        transaction_id = get_next_transaction_id()
        submit_button = st.button(label='Submit')

        if submit_button:
            if not items:
                st.error("Please select at least one item.")
                return

            # Buat DataFrame dengan beberapa item
            new_data = {
                "date_time": [date] * len(items),
                "Transaction": [transaction_id] * len(items),
                "Item": items,
                "qty": quantities
            }
            new_data_df = pd.DataFrame(new_data)
            append_transaction_data(new_data_df)
            update_item_stock(items, quantities)
            st.success('Data has been added successfully!')
            st.write(new_data_df)

def show_data():
    st.title("Data Transaksi")
    df = load_furniture_data()
    
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
    df = df.sort_values(by='Transaction', ascending=False)
    
    # Gunakan AgGrid untuk menampilkan tabel dengan pagination
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=5)
    gridOptions = gb.build()

    st.write("Report Data Transaction:")
    AgGrid(df, gridOptions=gridOptions, height=300, fit_columns_on_grid_load=True)
