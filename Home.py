import streamlit as st 
import datetime
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
from streamlit_pandas_profiling import st_profile_report
from tabulate import tabulate

names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pparker","rmiller"]

file_path = Path(__file__).parent/"hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names,usernames,hashed_passwords, "application_system", "abcdef", cookie_expiry_days=30)

name,authentication_status, username = authenticator.login("Login","main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")
    
if authentication_status:
    st.title="Student Monitoring System"
    st.sidebar.success("Succesfully Login!")
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Student Registration", "Prospectus", "Course Assignment and Enrollment", "Grade Report"],
            icons=["house", "person-lines-fill", "book", "list-columns-reverse", "bar-chart"],
            menu_icon = "cast",
            default_index=0,
        )

    st.markdown("# Student Monitoring System")
    st.write(f'Welcome *{name}*')
    st.write('Some content')

    if selected == "Home":
        st.line_chart(np.random.randn(30, 3))
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        st.bar_chart(chart_data)

        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode("utf-8")

        csv = convert_df(chart_data)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="large_df.csv",
            mime="text/csv",
        )
        
    if selected == "Student Registration":
        df = pd.DataFrame(
            [
            {"command": "st.selectbox", "rating": 4, "is_widget": True},
            {"command": "st.balloons", "rating": 5, "is_widget": False},
            {"command": "st.time_input", "rating": 3, "is_widget": True},
        ]
        )
        edited_df = st.data_editor(df)

        favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
        st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
    
    if selected == "Prospectus":
        tab_data = { 
    'Course No.' : ['GEC101','GEC104','MAT051','STT101','STT125','STT125.1','PED001','NST001'],
    'Course Title' : ['Understanding Self','Mathematics in the Modern World','Calculus I','Descriptive and Inferential Statistics','Statistical Computing I (Lec)','Statistical Computing I (Lab)','Exercise Prescription and Management','CWTS 1/ROTC 1'],
    'Units' : [3,3,5,4,2,1,2,3]
                 }
    
    data_Pros = pd.DataFrame(tab_data, header= "keys", tablefmt = 'grid')
    st.write(f"Welcome {selected}")

    if selected == "Course Assignment and Enrollment":
        st.write(f"Welcome {selected}")
    if selected == "Grade Report":
        st.write(f"Welcome {selected}")

    authenticator.logout("Logout","sidebar")
