import streamlit as st
import pandas as pd
import os

def load_furniture_items():
    if os.path.isfile("data_barang.csv"):
        df = pd.read_csv("data_barang.csv")
        return df
    else:
        st.error("File 'data_barang.csv' tidak ditemukan.")
        return pd.DataFrame()

def append_item_data(data):
    if not os.path.isfile("data_barang.csv"):
        df = pd.DataFrame(columns=["id", "nama_barang", "stok"])
        df.to_csv("data_barang.csv", index=False)
    else:
        df = pd.read_csv("data_barang.csv")
    
    df = pd.concat([df, data], ignore_index=True)
    df.to_csv("data_barang.csv", index=False)

def get_next_id():
    if os.path.isfile("data_barang.csv"):
        df = pd.read_csv("data_barang.csv")
        if not df.empty:
            last_id = df['id'].astype(int).max()
            return last_id + 1
    return 1

def show_adding_item_furniture_page():
    st.title("Menambah Barang Furniture")

    if os.path.isfile("data_barang.csv"):
        df_existing_items = pd.read_csv("data_barang.csv")
        st.subheader("Daftar Barang")
        st.dataframe(df_existing_items)
    else:
        st.warning("Belum ada barang dalam 'data_barang.csv'.")

    if 'notification' not in st.session_state:
        st.session_state.notification = None

    if st.session_state.notification:
        st.success(st.session_state.notification)
        st.session_state.notification = None  # Reset after showing

    st.subheader("Tambah Barang Baru")

    with st.form(key='new_item_form'):
        new_item_name = st.text_input('Nama Barang Baru')
        new_item_stok = st.number_input('Stok', min_value=1, step=1)
        add_new_item_button = st.form_submit_button(label='Tambah Barang Baru')

    if add_new_item_button:
        if new_item_name.strip() and new_item_stok > 0:
            if os.path.isfile("data_barang.csv"):
                df_existing_items = pd.read_csv("data_barang.csv")
                existing_names = df_existing_items['nama_barang'].str.strip().tolist()
                
                if new_item_name.strip().lower() in [name.lower() for name in existing_names]:
                    st.warning('Barang dengan nama ini sudah ada dalam daftar.')
                else:
                    new_id = get_next_id()
                    new_item_data = {
                        "id": [new_id],
                        "nama_barang": [new_item_name],
                        "stok": [new_item_stok]
                    }
                    new_item_df = pd.DataFrame(new_item_data)
                    append_item_data(new_item_df)
                    st.session_state.notification = 'Barang baru telah ditambahkan!'
                    st.experimental_rerun()
            else:
                st.error("File 'data_barang.csv' tidak ditemukan.")
        else:
            st.warning('Masukkan nama barang dan stok yang valid.')

    st.subheader("Tambah Data Barang")

    with st.form(key='item_form'):
        items_df = load_furniture_items()
        if not items_df.empty:
            nama_barang = st.selectbox('Nama Barang', items_df['nama_barang'].tolist())
            stok = st.number_input('Stok', min_value=1, step=1)
            submit_button = st.form_submit_button(label='Submit')

            if submit_button:
                if nama_barang:
                    item_exists = items_df[items_df['nama_barang'].str.strip().str.lower() == nama_barang.strip().lower()]
                    
                    if not item_exists.empty:
                        item_id = item_exists.iloc[0]['id']
                        existing_stock = item_exists.iloc[0]['stok']
                        new_stock = existing_stock + stok
                        items_df.loc[items_df['id'] == item_id, 'stok'] = new_stock
                        items_df.to_csv("data_barang.csv", index=False)
                        st.session_state.notification = f'Stok untuk "{nama_barang}" berhasil ditambah menjadi {new_stock}!'
                    else:
                        new_id = get_next_id()
                        new_data = {
                            "id": [new_id],
                            "nama_barang": [nama_barang],
                            "stok": [stok]
                        }
                        new_data_df = pd.DataFrame(new_data)
                        append_item_data(new_data_df)
                        st.session_state.notification = 'Data baru telah ditambahkan!'
                    
                    st.dataframe(items_df)
                    st.experimental_rerun()
                else:
                    st.warning('Pilih nama barang yang valid.')
        else:
            st.warning('Belum ada barang untuk dipilih.')
