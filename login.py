import streamlit as st
import pandas as pd

# Load the admin.csv file
def load_users(file_path):
    return pd.read_csv(file_path)

# Check if the username and password are valid
def authenticate(username, password, users):
    if username in users['username'].values:
        if users[users['username'] == username]['password'].values[0] == password:
            return True
    return False

# Main app function
def main():
    st.title("Login Form")

    # Load users
    users = load_users('admin.csv')

    # Create login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password, users):
            st.session_state['logged_in'] = True
            st.session_state['page'] = "main"
            st.success("Login successful. Click the button below to go to the Prediction page.")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

if __name__ == '__main__':
    main()
