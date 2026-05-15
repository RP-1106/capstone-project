import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

def upload_data():
    """Upload Data page with data preview and editing capabilities"""

    # CSS
    st.markdown("""
    <style>
    * {
        font-family: Verdana, sans-serif !important;
    }
    /* Custom styling for Streamlit elements */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        width: 100px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0 0;
        background-color: #585c5c !important;
        gap: 1px;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0e7d8b !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.write("## 📤 Upload Your Daily Transactions")
    
    # Initialize session state to store the dataframe
    if 'finance_df' not in st.session_state:
        st.session_state.finance_df = None
    
    st.markdown("Give us your existing financial history data to get started with the financial insights and explore the application features. Alternatively, you can navigate to the Expense or Income page as well, to manually enter transactions from scratch or add new ones as you continue using the app.")
    uploaded_file = st.file_uploader("Upload CSV", type="csv", label_visibility="collapsed")
        
    # Process the uploaded file
    if uploaded_file is not None:
        if st.session_state.finance_df is None or uploaded_file.name != st.session_state.get('last_uploaded_file', ''):
            try:
                data = pd.read_csv(uploaded_file)
                data['Transaction_id'] = ['TXN' + str(i + 1) for i in range(len(data))]
                
                st.session_state.finance_df = data
                st.session_state.last_uploaded_file = uploaded_file.name
                
                st.success(f"Successfully loaded {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error: {e}")
                return
    
    if st.session_state.finance_df is not None:
        df = st.session_state.finance_df

        # Option to clear the entire dataset
        if st.button("❌ Clear Dataset", help="This will remove the entire dataset"):
            st.session_state.finance_df = None
            st.session_state.pop('last_uploaded_file', None)
            st.success("Dataset cleared successfully. You can now upload a new file.")
            st.rerun()
        
        # Show basic statistics
        st.subheader("Dataset Summary")
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            st.metric("Total Rows", df.shape[0])
        with col2:
            st.metric("Columns", df.shape[1])
        with col3:
            date_cols = [col for col in df.columns if 'date' in col.lower()]

            if date_cols:
                date_col = date_cols[0]
                try:
                    df[date_col] = pd.to_datetime(df[date_col], format='%d-%m-%Y').dt.date 
                    min_date = df[date_col].min().strftime('%b %Y') if not pd.isna(df[date_col].min()) else "N/A"
                    max_date = df[date_col].max().strftime('%b %Y') if not pd.isna(df[date_col].max()) else "N/A"
                    st.metric("Date Range", f"{min_date} to {max_date}")
                except Exception as e:
                    st.warning(f"Failed to convert '{date_col}' to date format. Error: {e}")
        
        # Display tabs for viewing and editing
        view_tab, edit_tab = st.tabs(["View", "Edit"])
        
        with view_tab:
            st.write("#### Data Preview")
            st.dataframe(df)
            
            # Option to download the current dataframe
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Current Data",
                data=csv,
                file_name=f"finance_data.csv",
                mime="text/csv"
            )
        
        with edit_tab:
            st.write("#### Edit Your Data")
            st.write("To record fresh transactions, please go to Income/Expense Section!")
            st.write("To edit any of the existing cell values, directly make changes on the screen.\
            Select one or more columns to remove them using the 'Delete Rows' button at the bottom.\
            Don't forget to save your changes!")
            
            # Create an editable grid
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
            gb.configure_selection('multiple', use_checkbox=True)
            gb.configure_default_column(editable=True, groupable=True)
            
            date_cols = [col for col in df.columns if 'date' in col.lower()]
            for date_col in date_cols:
                gb.configure_column(date_col, type=["dateColumnFilter", "customDateTimeFormat"], 
                                  custom_format_string='dd-MM-yy')
            
            amount_cols = [col for col in df.columns if any(term in col.lower() for term in ['amount', 'price', 'cost', 'value'])]
            for amount_col in amount_cols:
                gb.configure_column(amount_col, type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                                  precision=2)
            
            grid_options = gb.build()
            
            # Display the grid
            grid_return = AgGrid(df, 
                               gridOptions=grid_options,
                               update_mode=GridUpdateMode.MODEL_CHANGED,
                               fit_columns_on_grid_load=True,
                               height=400,
                               allow_unsafe_jscode=True)
            
            updated_df = grid_return['data']
            selected_rows = pd.DataFrame(grid_return['selected_rows'])

            if not selected_rows.empty and st.button('Delete Rows'):
                st.session_state.finance_df = updated_df[~updated_df.isin(selected_rows).all(axis=1)].reset_index(drop=True)
                st.success(f"Deleted {len(selected_rows)} rows")
                st.rerun()
            
            if st.button('Save Changes'):
                st.session_state.finance_df = updated_df
                st.success("Changes synced successfully!")
                
    else:
        st.info("Please upload a CSV file to get started.")
        
        if st.button("Use Sample Data"):
            sample_df = pd.read_csv("data/dummy1.csv")
            st.session_state.finance_df = sample_df
            st.session_state.last_uploaded_file = "sample_data.csv"
            st.rerun()