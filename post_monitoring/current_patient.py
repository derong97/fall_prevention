import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objects as go
import time
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


    
    header = st.beta_container()

    hfr_count = st.beta_container()   
    frequency, buffer_2, average_visits = st.beta_columns([1,1/20,1])
    log_table_func, buffer_1, edit = st.beta_columns([1,1/20,1])

    current_patient_data = "SELECT * FROM current_patient_logs"
    df_logs = pd.read_sql(current_patient_data, conn) # read from database
    df_logs.columns = ["Bed Number", "Timestamp Start","Timestamp End","Accompanied","HFR Count"]
    df_display = df_logs.copy()
    df_display.insert(1,"Date",pd.to_datetime(df_logs["Timestamp Start"]).dt.date)
    df_display.insert(2,"Time Start",pd.to_datetime(df_logs["Timestamp Start"]).dt.time)
    df_display.insert(3,"Time End",pd.to_datetime(df_logs["Timestamp Start"]).dt.time)
    df_display = df_display.drop(columns=["Timestamp Start","Timestamp End"])
    df_display.columns = ["Bed Number", "Date", "Time Start","Time End","Accompanied","HFR Count"]
    
    
    with header: 
        st.title("Current Patient Log")
        

    with log_table_func:
        st.dataframe(df_display)

        with st.form(key="reset_bedno"):
            st.header("Reset Bed Number") 
            bed_reset = st.selectbox('Bed Number to Reset',range(1,39))
            if st.form_submit_button(label='Reset'): #sql query executed when button is clicked
                edit_logs = df_logs.copy()
                edit_logs["Timestamp Start"]= edit_logs["Timestamp Start"].dt.date
                date_first = edit_logs.loc[edit_logs['Bed Number'] == int(bed_reset), "Timestamp Start"].min() #date of first toilet visit
                date_last = edit_logs.loc[edit_logs['Bed Number'] == int(bed_reset), "Timestamp Start"].max() #date of last toilet visit
                send_old = df_logs[df_logs["Bed Number"] == int(bed_reset)] #select logs of patient to reset
                send_old["Date First"] = pd.to_datetime(date_first).date()
                send_old["Date Last"] = pd.to_datetime(date_last).date()
                send_old.columns = ['bed_number', 'timestamp_start','timestamp_end','hfr_count','accompanied','date_first','date_last']
                send_old.to_sql('discharged_patient_logs',conn,if_exists='append',index = False) #send to 
                refresh_command = "DELETE FROM current_patient_logs WHERE bed_number={0}".format(int(bed_reset))
                execute_query(conn, refresh_command)
            
        with st.form(key="export_bedno"):
            st.header("Export Bed Number") 
            bed_export = st.selectbox('Bed Number to Export',range(1,39))
            if st.form_submit_button(label='Export'): #sql query executed when button is clicked
                now = datetime.datetime.now()
                timestamp_export = now.strftime("%d %m %Y %H%M")
                export_logs = df_display[df_display["Bed Number"] == bed_export]
                export_logs.to_csv('bed {0} toilet log {1}.csv'.format(int(bed_export),timestamp_export),index=False)
        
    with edit:   
        with st.form(key='edit_log'):
            st.header("Edit Patient Log")
            st.write("Current Patient Data to Edit")
            bed_edit = st.selectbox('Bed Number',range(1,39))
            date_input = st.date_input(label= "Date")
            date_input = date_input.strftime('%d/%m/%Y')
            time_input = st.text_input(label= "Start Time in HH:MM:SS format")
            st.write("Updated Patient Data")
            accompanied_new_input = st.checkbox('Accompanied')
            hfr_count_new_input = st.selectbox("HFR Count",("Alarm was Triggered","Alarm was not Triggered","Not Applicable"))
            if accompanied_new_input: #convert user input into db input
                accompanied_new = 1
            else:
                accompanied_new = 0
            if (hfr_count_new_input == "Alarm was Triggered"):
                hfr_count_new = 1
            elif (hfr_count_new_input == "Alarm was not Triggered"):
                hfr_count_new = 0
            elif (hfr_count_new_input == "Not Applicable"):
                hfr_count_new = 'NULL'
            if st.form_submit_button(label='Edit'): #sql query executed when button is clicked
                date_input = pd.to_datetime(date_input)
                time_input = datetime.datetime.strptime(time_input,"%H:%M:%S").time()
                datetime_input = datetime.datetime.combine(date_input, time_input)
                edit_command = "UPDATE current_patient_logs SET accompanied = {0}, hfr_count = {1} WHERE bed_number = {2} AND timestamp_start = '{3}' ".format(int(accompanied_new), int(hfr_count_new), int(bed_edit), datetime_input)
                execute_query(conn, edit_command)
                


    conn.close()
