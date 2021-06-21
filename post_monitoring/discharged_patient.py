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
    engine = create_engine("mysql+pymysql://rpi:password123^@localhost/post_monitoring_db")
    conn = engine.connect()

    print(conn)

    def execute_query(connection, query):
        with connection.connect() as connection:
            result = connection.execute(query)
            print("Query successful")
    
    header = st.beta_container()
    #log_table, buffer_1, functions_1 = st.beta_columns([1,1/20,1])
    dataset, buffer_2, functions = st.beta_columns([1,1/20,1])

    #remove logs 1 year ago
    today_date = datetime.date.today() #get current date
    one_year_ago =  today_date - datetime.timedelta(weeks=52) #get one year ago
    remove_data = "DELETE FROM discharged_patient_logs WHERE date_last < '{0}'".format(one_year_ago)
    execute_query(conn, remove_data)
    
    discharged_ward_data = "SELECT * FROM discharged_patient_logs"
    discharged_logs = pd.read_sql(discharged_ward_data, conn)
    discharged_logs.columns = ["Bed Number", "Timestamp Start","Timestamp End","Accompanied","HFR Count","First Toilet Visit","Last Toilet Visit"]
    discharged_display = discharged_logs.copy()
    discharged_display.insert(1,"Date",pd.to_datetime(discharged_logs["Timestamp Start"]).dt.date)
    discharged_display.insert(2,"Time Start",pd.to_datetime(discharged_logs["Timestamp Start"]).dt.time)
    discharged_display.insert(3,"Time End",pd.to_datetime(discharged_logs["Timestamp Start"]).dt.time)
    discharged_display["First Toilet Visit"]= pd.to_datetime(discharged_logs["First Toilet Visit"]).dt.date
    discharged_display["Last Toilet Visit"]= pd.to_datetime(discharged_logs["Last Toilet Visit"]).dt.date
    discharged_display = discharged_display.drop(columns=["Timestamp Start","Timestamp End"])
    discharged_display.columns = ["Bed Number", "Date", "Time Start","Time End","Accompanied","HFR Count","First Toilet Visit","Last Toilet Visit"]

    with header: 
        st.title("Discharged Patient Log")

    with dataset:
        st.header("")
        placeholder_logs = st.empty()
        placeholder_logs.dataframe(discharged_display, height = 800)
            
   
    with functions:
        with st.form(key="filter_patient"):
            st.header("Filter Search")
            bed_filter = st.checkbox("Specific Bed Number")
            bed_search = st.selectbox(label = "Bed Number", options = range(1,39))
            if st.form_submit_button(label='Filter'):
                if bed_filter:
                    patient_old_logs = discharged_display[discharged_display["Bed Number"]== int(bed_search)]
                    placeholder_logs.dataframe(patient_old_logs)
                else:
                    placeholder_logs.dataframe(discharged_display,height = 800)
                
        with st.form(key="export_bedno_2"):
            st.header("Export Bed Number") 
            bed_export = st.selectbox(label = "", options = range(1,39))
            date_input = st.date_input(label= "Date of First Toilet Visit")
            if st.form_submit_button(label='Export'):
                now = datetime.datetime.now()
                timestamp_export = now.strftime("%d %m %Y %H%M")
                export_logs = discharged_display[(discharged_display["Bed Number"] == bed_export) & (discharged_display["First Toilet Visit"] == date_input)]
                export_logs.to_csv('bed {0} toilet log {1}.csv'.format(int(bed_export),timestamp_export),index=False)

   
    conn.close()
