import streamlit as st
from login import main as login_main
from main import main as main_page

# Fungsi untuk memutuskan halaman mana yang harus ditampilkan
def navigate():
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    if st.session_state["page"] == "main":
        main_page()
    else:
        login_main()

if __name__ == '__main__':
    navigate()
