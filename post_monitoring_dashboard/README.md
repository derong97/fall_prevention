# fall-prevention-visualisation
Data Analytics and Visualisation on StreamLit.


# Setup MySQL
1. Install MySQL:
https://dev.mysql.com/downloads/mysql/5.7.html
2. Create the database and tables
Run 'post_monitoring_db script.sql'
Refer to posture_detection_logs_v3.csv for psuedo data created
3. Create an account with the following permissions (change 'username' and 'password' to desired input) by running the following commands:
`CREATE USER 'username’@‘%’ IDENTIFIED BY 'password';`
`GRANT ALL PRIVILEGES ON post_monitoring_db.* TO 'username’@‘%’ WITH GRANT OPTION;`
`FLUSH PRIVILEGES`


# Setup Streamlit
1. Clean Install Streamlit 
use this link: https://docs.streamlit.io/en/stable/troubleshooting/clean-install.html
2. Connect Interface to Database
Create a .env file. Copy and paste the required environment variables from env_template, and insert the details of the private SQL database into that file.
3. Run this command to ensure that all other requirements are installed: 
`pip3 install -r requirements.txt`
4. Run the app:
`streamlit run main_app.py`


#Visualisation 
A Dashboard containing 3 different insights will be shown (visualisation.py)
![Visualisation](/post_monitoring_dashboard/images/visualisation.jpg)
1. To edit the thresholds (red line) for:
 - Patient’s High Fall Risk (HFR) Count Ratio: change value for hfr_threshold 
 - Patient Daily Average Number of Toilet Visits: change value for average_threshold 
2. An alternative user interface for the visualisation (visualisation_v2.py) has been created should you wish to have the descriptions for the analytics permanently displayed as shown below. 
![Visualisation](/post_monitoring_dashboard/images/visualisation_v2.png)
Run the alternative user interface using `streamlit run main_app_v2.py`


#Current Patient Log (current_patient.py)
User interface that displays the logs of currently admitted patients. Includes reset, export and edit features.
![Current Patient Log](/post_monitoring_dashboard/images/current.jpg)

#Discharged Patient Log (discharged_patient.py)
User interface that displays the logs of discharged patients. Includes export feature.
![Discharged Patient Log](/post_monitoring_dashboard/images/discharged.jpg)
