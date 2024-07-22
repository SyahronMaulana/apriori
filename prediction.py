import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

def load_data_prediction():
    try:
        df = pd.read_csv("data-transaksi2.csv")
    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
        return None
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        return None

    try:
        df['date_time'] = pd.to_datetime(df['date_time'], format='%Y-%m-%d', errors='coerce')
        df.dropna(subset=['date_time'], inplace=True)
        df['year_month_day'] = df['date_time'].dt.to_period('D')
        df['year_month'] = df['date_time'].dt.to_period('M')

        # Mapping month numbers to month names
        month_mapping = {i: month for i, month in enumerate(['January', 'February', 'March', 'April', 'May', 'June'], 1)}
        df['year_month'] = df['year_month'].apply(lambda x: month_mapping.get(x.month, 'Unknown'))
    except Exception as e:
        st.error(f"An error occurred while processing the data: {e}")
        return None

    return df

def show_prediction_page():
    st.title("Halaman Prediction")
    df = load_data_prediction()
    if df is None:
        return

    with st.form(key='prediction_form'):
        periode_pendukung = st.number_input('Periode Bulan Pendukung', min_value=1, max_value=6, step=1)
        periode_prediksi = st.number_input('Periode Prediksi Bulan', min_value=1, step=1, value=1)
        submit_button = st.form_submit_button(label='Submit')
    
    if submit_button:
        st.write(f"Periode Bulan Pendukung: {periode_pendukung}")
        st.write(f"Periode Prediksi Bulan: {periode_prediksi}")  
        
        # Convert inputs to integers
        periode_pendukung = int(periode_pendukung)
        periode_prediksi = int(periode_prediksi)
        
        try:
            # Filter the last 'periode_pendukung' months
            latest_period = df['year_month'].unique()[-periode_pendukung:]
            pendukung_data = df[df['year_month'].isin(latest_period)]
        except Exception as e:
            st.error(f"An error occurred while filtering the data: {e}")
            return
        
        # Check if the pendukung_data is empty
        if pendukung_data.empty:
            st.write("No data available for the selected period.")
        else:
            try:
                # Remove duplicate transactions for the same item in the same period
                pendukung_data = pendukung_data.drop_duplicates(subset=['year_month', 'Item', 'Transaction'])

                # Group data by item and calculate demand for each item
                demand_per_product = pendukung_data.groupby('Item')['Transaction'].count()
                prediction_data = []

                for item, demand in demand_per_product.items():
                    if demand > 0:
                        # Calculate the single moving average for the item
                        item_data = pendukung_data[pendukung_data['Item'] == item]
                        moving_average = int(item_data['Transaction'].count() / periode_pendukung)
                        
                        # Generate predictions for the item
                        predictions = [moving_average] * periode_prediksi
                        total_prediction = sum(predictions)
                        prediction_data.append({
                            'Item': item,
                            'Total Predicted Demand': total_prediction
                        })

                if prediction_data:
                    prediction_df = pd.DataFrame(prediction_data)
                    # Sort the prediction data by Total Predicted Demand in descending order
                    prediction_df = prediction_df.sort_values(by='Total Predicted Demand', ascending=False)
                    
                    # Create AgGrid table with pagination
                    gb = GridOptionsBuilder.from_dataframe(prediction_df)
                    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=5)
                    gridOptions = gb.build()

                    st.write("Predictions for the demand of the next months:")
                    AgGrid(prediction_df, gridOptions=gridOptions, height=300, fit_columns_on_grid_load=True)
                else:
                    st.write("No items have demand in the selected period.")
            except Exception as e:
                st.error(f"An error occurred while generating predictions: {e}")
