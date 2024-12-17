import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import datetime

from get_data import generate_master_table, get_matrix
from graphs import plot_heatmap, plot_heatmap_perc, lines_chart

# ---- Password Protection ---- #
# Define username and password
USER_CREDENTIALS = {"admin": "password123", "user1": "securepass"}

# Create a login form
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("Invalid username or password")

# -------------------- Static Section --------------------

def main():
    # Set up the app title and static content
    st.title("Interactive User Analytics Dashboard")

    st.markdown("""
    ## Explanation and Summary
    This application provides an interactive way to analyze user activity across different countries and statuses. 
    You can use the dropdown inputs to customize the data and view the results in visual graphs. The sections include:
    1. An **Input Section** where you choose filters.
    2. A **Graphs Section** displaying insights.
    """)

    st.write("---")

    # -------------------- Input Section --------------------

    # Dropdown options
    cohort_size = ["Monthly", "Quarterly"]

    # Create a sentence with dropdowns
    st.subheader("Input Section")

    st.write("Cohort Size: ")
    cohort_size = st.selectbox("Cohort Size", options=cohort_size, index=0, label_visibility="collapsed")

    st.write("Cohorts Acquisition Period:")
    start_acq = st.date_input("Select Date", value=datetime.date(2024, 1, 1), key="start_acq")
    end_acq = st.date_input("Select Date", value=datetime.date(2024, 1, 1), key="end_acq")

    st.write("Retention Calculation End Date: ")
    #start_ret = st.date_input("Select Start Month and Year", value=datetime.date(2024, 1, 1), key="start_ret")
    end_ret = st.date_input("Select Date", value=datetime.date(2024, 1, 1), key="end_ret")

    st.write("---")

    st.markdown(f"""
    <span style="font-size:20px;">
    I want to see 
    <span style="font-weight:bold; font-size:22px;">
    {cohort_size}
    </span> retention for users acquired between
    <span style="font-weight:bold; font-size:22px;">
    {start_acq}
    </span>
    and
    <span style="font-weight:bold; font-size:22px;">
    {end_acq}
    </span> in the period between
    <span style="font-weight:bold; font-size:22px;">
    {start_acq}
    </span> and
    <span style="font-weight:bold; font-size:22px;">
    {end_ret}
    </span>
    </span>
    """, unsafe_allow_html=True)

    show_button = st.button("Show", type="primary")

    # col1, col2, col3 = st.columns([3, 2, 1])
    # Loading data
    df = generate_master_table()

    # Filtered Data based on Input
    if show_button:
        filtered_data = df[(df['FIRST_ORDER']>=pd.to_datetime(start_acq))&
        (df['FIRST_ORDER']<=pd.to_datetime(end_acq))&
        (df['ORDER_DATE']>=pd.to_datetime(start_acq))&
        (df['ORDER_DATE']<=pd.to_datetime(end_ret))]
        
        #st.write(f"### Showing **{status_choice.capitalize()}** users from **{country_choice}**")
    else:
        filtered_data = df.iloc[0:0]  # Show an empty DataFrame initially

    st.write("---")

    # -------------------- Visualization Section --------------------

    st.subheader("Visualization")

    if show_button and not filtered_data.empty:
        s = get_matrix(filtered_data, cohort_size)

        # Graph 1: Line Chart
        cohort_size = cohort_size.replace("ly", "")
        fig1 = plot_heatmap(s, cohort_size)
        st.plotly_chart(fig1, use_container_width=True)
        fig2 = plot_heatmap_perc(s, cohort_size)
        st.plotly_chart(fig2, use_container_width=True)
        fig3 = lines_chart(s, cohort_size)
        st.plotly_chart(fig3, use_container_width=True)

    elif show_button:
        st.error("No data found for the selected filters. Please adjust your inputs.")


# ---- App Flow ---- #
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    login()
else:
    main()