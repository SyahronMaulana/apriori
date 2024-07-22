import streamlit as st
from prediction import show_prediction_page
from apriori import show_apriori_page
from add_transaction import show_add_transaction_page, show_data
from adding_item_furniture import show_adding_item_furniture_page  # Mengimpor fungsi dari adding_item_furniture.py

# Fungsi untuk memeriksa status login
def check_login():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.session_state['page'] = 'login'
        st.experimental_set_query_params(page="login")
        st.experimental_rerun()

# Fungsi utama
def main():
    # Periksa status login
    check_login()

    

    # Judul aplikasi
    st.title("Inventory Management System")

    # Menu sidebar
    pilihan = st.sidebar.radio(
        "Menu",
        ("Home", "Data Barang", "Data Transaksi", "Apriori", "Prediksi")
    )

    # Tombol logout di sidebar
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['page'] = "login"
        st.experimental_rerun()

    # Konten berdasarkan pilihan sidebar atau session state
    page = st.session_state.get("page", "home")
    
    if pilihan == "Home":
        if page == 'login':
            st.error("You must log in first!")
        else:
            st.title("Halaman Utama")
            st.write("Selamat datang di halaman utama.")
    elif pilihan == "Prediksi":
        show_prediction_page()
    elif pilihan == 'Apriori':
        show_apriori_page()
    elif pilihan == 'Data Transaksi':
        show_add_transaction_page()
        show_data()
    elif pilihan == 'Data Barang':
        show_adding_item_furniture_page()

    # Update session state berdasarkan pilihan
    st.session_state["section"] = pilihan.lower()

if __name__ == '__main__':
    main()
