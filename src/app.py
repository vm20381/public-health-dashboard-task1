import streamlit as st

def main():
    st.set_page_config(page_title="Public Health Dashboard", layout="wide")
    
    st.title("Public Health Dashboard")
    st.write("Welcome to the COVID-19 Data Insights Dashboard.")
    
    st.sidebar.header("Navigation")
    st.sidebar.info("This dashboard is currently under construction.")

if __name__ == "__main__":
    main()
