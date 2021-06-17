import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objects as go
import mysql.connector

from sqlalchemy import create_engine

def app():
    engine = create_engine("mysql+pymysql://raspberry:password123^@localhost/post_monitoring_db")
    conn = engine.connect()
    #conn = mysql.connector.connect(
    #    host = "localhost",
    #    port="3306",
    #    user  = "raspberry",
    #    password = "password123^",
    #    database = "post_monitoring_db"
    #)

    print(conn)

    def execute_query(connection, query):
        with connection.connect() as connection:
            result = connection.execute(query)
            print("Query successful")


    # page layout
    header = st.beta_container()
    hfr_count = st.beta_container()   
    frequency, buffer_2, average_visits = st.beta_columns([1,1/20,1])

    current_patient_data = "SELECT * FROM current_patient_logs"
    df_logs = pd.read_sql(current_patient_data, conn) #read from database
    df_logs.columns = ["Bed Number", "Timestamp Start","Timestamp End","Accompanied","HFR Count"]
    df_display = df_logs.copy()
    df_display.insert(1,"Date",pd.to_datetime(df_logs["Timestamp Start"]).dt.date)
    df_display.insert(2,"Time Start",pd.to_datetime(df_logs["Timestamp Start"]).dt.time)
    df_display.insert(3,"Time End",pd.to_datetime(df_logs["Timestamp Start"]).dt.time)
    df_display = df_display.drop(columns=["Timestamp Start","Timestamp End"])
    df_display.columns = ["Bed Number", "Date", "Time Start","Time End","Accompanied","HFR Count"]

    # calculating frequency of toilet use of entire ward
    df_frequency = df_display.copy()
    df_frequency = df_frequency.iloc[:, 0:3]
    today_date = datetime.date.today() #get current date
    week_before =  today_date - datetime.timedelta(weeks=1) #get week before
    df_frequency = df_frequency[df_frequency["Date"] >= week_before] #keep only those dates in the past 7 days
    df_frequency['Hour of the Day'] = df_frequency['Time Start'].astype("string")
    df_frequency['Hour of the Day'] = df_frequency['Hour of the Day'].str[:3]+"00"
    df_frequency['Frequency'] = 1
    df_frequency = df_frequency[["Date",'Hour of the Day',"Frequency"]]
    df_hour_freq = df_frequency.groupby(["Date",'Hour of the Day'],as_index=False).count() #group by time interval , count
    df_hour_freq = df_hour_freq.groupby('Hour of the Day',as_index=False)["Frequency"].mean()  #mean number of times each patient uses the toilet each day
    df_hour_freq.reset_index(inplace = True)

    # calculating number of toilet visits per day 
    df_average_visits = df_display.copy()
    df_average_visits = df_average_visits.iloc[:, 0:3]
    df_average_visits = df_average_visits.drop(columns = ["Time Start"])
    df_average_visits['Frequency'] = 1
    df_average_visits = df_average_visits.groupby(["Date","Bed Number"],as_index=False).count() #count the number of times each patient uses the toilet for each day
    df_average_visits = df_average_visits.drop(columns = ["Date"])
    df_average_visits = df_average_visits.groupby("Bed Number",as_index=False)["Frequency"].mean()  #mean number of times each patient uses the toilet each day
    df_average_visits.sort_values("Frequency", inplace=True ,ascending=False,ignore_index=True)

    # calculating patients by the HFR counts
    df_hfr_count = df_display[df_display["Accompanied"] == 0]
    df_hfr_count = df_hfr_count.groupby("Bed Number").mean()
    df_hfr_count = df_hfr_count[["HFR Count"]]
    df_hfr_count.reset_index(inplace = True)
    df_hfr_count.columns = ["Bed Number", 'HFR Count Ratio']
    df_hfr_count.sort_values('HFR Count Ratio', inplace=True ,ascending=False,ignore_index=True)

    with header: 
        st.title("Ward 37's Post-Toilet Visit Monitoring Visualisation")


    with hfr_count: 
        st.header("Patients By Their High Fall Risk (HFR) Count Ratio for Every Unaccompanied Toilet Visit")
        placeholder_hfr = st.empty()
        description_hfr = placeholder_hfr.button("Description of HFR Count Ratio")  
        if description_hfr:
            placeholder_hfr.write("For every unaccompanied toilet visit, if a 'Come Now' alarm is triggered, it would result in a HFR Count of 1, else it would result in a HFR Count of 0. A HFR ratio is then calculated by taking the average HFR counts from all the unaccompanied toilet visits for the patients. For example, if the patient has recorded 3 unaccompanied toilet visits, and activates the 'Come Now' alarm 2 times, then the HFR Count ratio is 2/3 = 0.66")
            if st.button("Close Description"):
                placeholder_hfr.empty()
        hist_hfr_count = fig = px.bar(df_hfr_count, x='Bed Number', y='HFR Count Ratio')
        hist_hfr_count.add_trace(go.Scatter(x=df_hfr_count['Bed Number'],y=[.5]*38,showlegend = False))
        st.plotly_chart(hist_hfr_count,use_container_width=True)

    with frequency: 
        st.header("Average Frequency of Toilet Use (Over a Week) for Every Hour in the Entire Ward")
        placeholder_freq = st.empty()
        description_freq = placeholder_freq.button("Description of Average Toilet Use Frequency")
        if description_freq:
            placeholder_freq.write("For every hour, the average frequency is calculated by taking the total number of toilet visits during that hour divided by the past 1 week based on the currently registered patients in the ward . For example, at 0900, if there were 21 toilet visits recorded over the past 1 week, the average frequency calculated as 21/7 = 3.")
            if st.button("Close Description"):
                placeholder_freq.empty()
        hist_hour_freq = fig = px.bar(df_hour_freq, x='Hour of the Day', y='Frequency',labels={'Hour of the Day':'Time of the Day (24h)'})
        hist_hour_freq.update_traces(marker_color='MediumPurple')
        st.plotly_chart(hist_hour_freq, use_container_width=True)

    with average_visits: 
        st.header("Average Number of Toilet Visits Per Day For Each Patient")
        placeholder_visit = st.empty()
        description_visit = placeholder_visit.button("Description of Average Toilet Visit")
        if description_visit:
            placeholder_visit.write("For each patient, the average number of toilet visits is calculated by taking the number of toilet visits that the patient takes divided by the number of dates where the patient has recorded to have used the toilet. For example, if the patient is recorded to have visited the toilet 5 times on day 1 and 8 times on day 2, the average number of toilet visits calculated will be (8+5)/2 = 6.5")
            if st.button("Close Description"):
                placeholder_visit.empty()
        hist_average_visits = fig = px.bar(df_average_visits, x='Bed Number', y='Frequency')
        hist_average_visits.add_trace(go.Scatter(x=df_average_visits['Bed Number'],y=[3]*38,showlegend = False))
        st.plotly_chart(hist_average_visits,use_container_width=True)

    conn.close()
