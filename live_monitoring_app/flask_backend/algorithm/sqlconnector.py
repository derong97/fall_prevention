

from sqlalchemy import create_engine

sql_engine = create_engine("mysql+pymysql://raspberry:password@10.21.147.2/post_monitoring_db")
sql_conn = sql_engine.connect()

new_log = sql_conn.execute("INSERT INTO  `post_monitoring_db`.`current_patient_logs` (bed_number,timestamp_start,timestamp_end,accompanied,hfr_count) \
                  VALUES (4,'2021-06-10 11:04:59','2021-06-10 11:07:44',0,1)")

print("Row Added  = ",new_log.rowcount)




