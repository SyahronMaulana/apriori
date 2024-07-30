import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import association_rules, apriori
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

def load_data_apriori():
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

        month_mapping = {i: month for i, month in enumerate(['January', 'February', 'March', 'April', 'May', 'June'], 1)}
        df['year_month'] = df['year_month'].apply(lambda x: month_mapping.get(x.month, 'Unknown'))
    except Exception as e:
        st.error(f"An error occurred while processing the data: {e}")
        return None

    return df

def show_apriori_page():
    st.title("Apriori Analysis")
    df = load_data_apriori()
    if df is None:
        return

    with st.form(key='apriori_form'):
        periode_pendukung = st.number_input('Periode Bulan Analisis', min_value=1, max_value=6, step=1)
        min_support = st.number_input('Minimum Support', min_value=0.0, max_value=1.0, step=0.01, value=0.1)
        min_confidence = st.number_input('Minimum Confidence', min_value=0.0, max_value=1.0, step=0.01, value=0.5)
        submit_button = st.form_submit_button(label='Submit')
    
    if submit_button:
        st.write(f"Periode Bulan Analisis: {periode_pendukung}")
        
        try:
            # Filter the last 'periode_pendukung' months
            latest_period = df['year_month'].unique()[-periode_pendukung:]
            analysis_data = df[df['year_month'].isin(latest_period)]
        except Exception as e:
            st.error(f"An error occurred while filtering the data: {e}")
            return
        
        # Check if the analysis_data is empty
        if analysis_data.empty:
            st.write("No data available for the selected period.")
        else:
            try:
                # Prepare data for apriori analysis
                basket = (analysis_data
                          .groupby(['Transaction', 'Item'])['Item']
                          .count().unstack().reset_index().fillna(0)
                          .set_index('Transaction'))

                # Convert quantities to 1/0
                basket = basket.applymap(lambda x: 1 if x > 0 else 0)
                
                # Apply apriori
                frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
                rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
                
                if not rules.empty:
                    rules = rules[['antecedents', 'consequents', 'support', 'confidence']]
                    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
                    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
                    
                    st.write("Association Rules:")
                    
                    # Create AgGrid table with pagination
                    gb = GridOptionsBuilder.from_dataframe(rules)
                    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=5)
                    gridOptions = gb.build()

                    AgGrid(rules, gridOptions=gridOptions, height=300, fit_columns_on_grid_load=True)
                else:
                    st.write("No association rules found for the selected period with the given support and confidence thresholds.")
               
            except Exception as e:
                st.error(f"An error occurred while generating association rules: {e}")