import streamlit as st
import pandas as pd
import os
import hashlib

def load_user_data():
    try:
        if not os.path.isfile("admin.csv"):
            df = pd.DataFrame(columns=["username", "password"])
            df.to_csv("admin.csv", index=False)
        else:
            df = pd.read_csv("admin.csv")
    except pd.errors.ParserError as e:
        st.error(f"Error reading the CSV file: {e}")
        # Create an empty DataFrame if there is an error
        df = pd.DataFrame(columns=["username", "password"])
    return df

def save_user_data(df):
    df.to_csv("admin.csv", index=False)

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    df = load_user_data()
    if username in df['username'].values:
        st.error(f"User '{username}' already exists.")
    else:
        hashed_password = hash_password(password)
        new_user = pd.DataFrame({"username": [username], "password": [hashed_password]})
        df = pd.concat([df, new_user], ignore_index=True)
        save_user_data(df)
        st.success(f"User '{username}' added successfully!")

def delete_user(username):
    df = load_user_data()
    if username in df['username'].values:
        df = df[df['username'] != username]
        save_user_data(df)
        st.success(f"User '{username}' deleted successfully!")
    else:
        st.error(f"User '{username}' not found.")

def show_manage_users_page():
    st.title("Kelola Pengguna")

    st.subheader("Tambah Pengguna")
    with st.form(key='add_user_form'):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        add_user_button = st.form_submit_button("Add User")

        if add_user_button:
            if new_username and new_password:
                add_user(new_username, new_password)
            else:
                st.error("Username and password are required.")

    st.subheader("Hapus Pengguna")
    with st.form(key='delete_user_form'):
        username_to_delete = st.text_input("Username to Delete")
        delete_user_button = st.form_submit_button("Delete User")

        if delete_user_button:
            if username_to_delete:
                delete_user(username_to_delete)
            else:
                st.error("Username is required.")

    st.subheader("Daftar Pengguna")
    df = load_user_data()
    # Hapus kolom password sebelum menampilkan
    if 'password' in df.columns:
        df = df.drop(columns=['password'])
    st.write(df)

