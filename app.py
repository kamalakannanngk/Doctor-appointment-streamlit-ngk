import streamlit as st 
import pandas as pd
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
import os

# Doctor appointment system
st.set_page_config(page_title="Doctor Appointment System", page_icon=":hospital:", layout="wide")
df = pd.read_csv("data.csv")

# Add a new column "DateTime" to the dataframe
df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"])

style = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://www.worldatlas.com/r/w1200/upload/80/05/d5/pill-map-ss.jpg");
        background-size: cover;
    }
    [data-testid="stHeader"]{
        background-color: rgba(0, 0, 0, 0);
    }
    [data-testid="stTable"], .streamlit-expanderHeader, .streamlit-expanderContent{
        background-color: #ffffff;
    }
"""

# Title
title = """
    <h1 style="text-align: center;"> Doctor Appointment System </h1>
"""

st.markdown(title, unsafe_allow_html=True)

tab1,tab2,tab3,tab4 = st.tabs(["Appointment","Appointment details","Cancellation","Doctor details"])
with tab1:
    c3,c4,c5 = st.columns([1,3,1])

    with c4:
        st.write("Enter your details to book an appointment")
        b = st.empty()
        c = st.empty()
        # Name
        name = st.text_input("Name", key = "name3")
        
        # Email
        email = st.text_input("Email")

        #Validate Email
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            if email != "":
                st.warning("Invalid email address")

        # Doctor
        doctor = st.selectbox("Doctor", ["Dr. P.Arumugam", "Dr. R.Thangaraj", "Dr. P.Sivakumar"])

        c1,c2 = st.columns(2)

        with c1:
            # Date
            date = st.date_input("Date")
        with c2:
            # Time
            valid_times = []
            for hour in range(24):
                for minute in ['00', '30']:
                    time = f"{hour:02d}:{minute}"
                    valid_times.append(time)

            # Display dropdown select box
            selected_time = st.selectbox("Time", valid_times)

            # Print selected time
            st.write("Selected time:", selected_time)
            # Time
            #time = st.time_input("Time")

        # Convert selected date and time to a datetime object
        selected_datetime = pd.to_datetime(str(date) + " " + selected_time)

        # Reason
        reason = st.text_area("Reason", height=100)

        # Submit
        submit = st.button("Submit")
        if submit:
            if not (name and email and doctor and date and selected_time and reason):
                c.warning("Fill all the details!")
            else:
                # Check if the email is already registered
                if email in df["Email"].values:
                    c.warning("Email already registered!")
                elif ((df["Doctor"] == doctor) & (df["DateTime"] == selected_datetime)).any():
                    c.warning("Appointment already booked!")
                else:
                    # Add new appointment to data file
                    data = pd.DataFrame({
                        "Name": [name],
                        "Email": [email],
                        "Doctor": [doctor],
                        "Date": [date],
                        "Time": [selected_time],
                        "Reason": [reason],
                        "DateTime": [selected_datetime]
                    })
                    df_original = pd.read_csv("data.csv")
                    df = pd.concat([df_original, data], ignore_index=True)
                    df.to_csv('data.csv', index=False)
                    c.success("Appointment Successful")

with tab2:
    st.table(df)
