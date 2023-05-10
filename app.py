import streamlit as st 
import pandas as pd
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
import os
from PIL import Image

#st.set_theme('dark')

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
        doctor = st.selectbox("Doctor", ["Dr. S. Sivakarthikeyan", "Dr. R.Thangaraj", "Dr. R.Pavithra"])

        c1,c2 = st.columns(2)

        with c1:
            # Date
            date = st.date_input("Date")
        with c2:
            # Time
            valid_times = []
            for hour in range(8, 17):
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
    st.table(df.drop(["Email","DateTime"],axis=1))
    st.button("Refresh")

with tab3:

    column1, column2, column3 = st.columns([1,3,1])

    with column2:
        st.write("Fill the particulars to cancel your appointment!")
        #st.set_page_config(layout = 'center')
        k = st.empty()
        # Name
        name_ = st.text_input("Enter your name")
        
        # Email
        email_ = st.text_input("Enter your email")

        # Doctor
        doctor_ = st.selectbox("Select Doctor", ["Dr. S. Sivakarthikeyan", "Dr. R.Thangaraj", "Dr. R.Pavithra"])

        col1,col2 = st.columns(2)

        with col1:
            # Date
            date_ = st.date_input("Select Date")
        with col2:
            # Time
            valid_times_ = []
            for hour in range(8, 17):
                for minute in ['00', '30']:
                    time_ = f"{hour:02d}:{minute}"
                    valid_times_.append(time_)

            # Display dropdown select box
            selected_time = st.selectbox("Select Time", valid_times)

            # Print selected time
            st.write("Selected time:", selected_time)
        if st.button("Remove"):
            if email_ != "" and date_ != "" and time_ != "":
                d1=df[email_ == df["Email"]]
                df = df.drop(df[email_ == df["Email"]].index)
                df.to_csv('data.csv', index = False)
                st.success("Appointment cancelled")
            else:
                k.error("Please enter valid Email, Date and Time!")


with tab4:

    image_1 = Image.open("doctor_1.jfif")
    image_2 = Image.open("doctor_2.jfif")
    image_3 = Image.open("doctor__3.jfif")
    
    #resize_1 = image_1.resize(200,200)


    with st.container():
        img_col_1, img_col_2 = st.columns([1,4])
        with img_col_1:
            st.image(image_1, caption = "Dr.S.Sivakarthikeyan")
        with img_col_2:
            st.header("CARDIOLOGY SPECIALIST")
            st.write("""
                    Education:

Bachelor of Medicine and Bachelor of Surgery (MBBS)
Master of Science in Cardiology
Doctor of Medicine (MD) in Cardiology
Specializations:

Cardiac Imaging
Heart Failure
Coronary Artery Disease
Arrhythmias
Interventional Cardiology
Experience:

10 years of experience in Cardiology
                """)

    with st.container():
        img_col_1, img_col_2 = st.columns([1,4])
        with img_col_1:
            st.image(image_2, caption = "Dr.R.Thangaraj")
        with img_col_2:
            st.header("NEUROLOGY SPECIALIST")
            st.write("""
                    Education:

Bachelor of Science, Biology: University of California, Los Angeles
Doctor of Medicine: University of Southern California, Keck School of Medicine
Neurology Residency: Stanford University Medical Center
Certifications and Memberships:

American Board of Psychiatry and Neurology Certification in Neurology
American Academy of Neurology Membership
California Medical Association Membership
                """)


    with st.container():
        img_col_1, img_col_2 = st.columns([1,4])
        with img_col_1:
            st.image(image_3, caption = "Dr.R.Pavithra")
        with img_col_2:
            st.header("DERMATOLOGY SPECIALIST")
            st.write("""
                    Qualifications: MD, FAAD\n
Specializations: Dermatology, Cosmetic Dermatology\n
Years of experience: 12 years
Board certifications: American Board of Dermatology
Education:

Bachelor's degree in Biology, University of California, Los Angeles (UCLA)
Doctor of Medicine (MD), Keck School of Medicine of USC
Residency: Dermatology, Keck School of Medicine of USC
Fellowship: Cosmetic Dermatology, UCLA School of Medicine
Professional memberships: American Academy of Dermatology, American Society for Dermatologic Surgery, Women's Dermatologic Society
                """)
