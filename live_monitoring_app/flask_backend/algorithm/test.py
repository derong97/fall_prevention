from sqlalchemy import create_engine


sql_engine = create_engine("mysql+pymysql://raspberry:password@10.21.147.2/post_monitoring_db")
sql_conn = sql_engine.connect()

query = ("INSERT INTO  `post_monitoring_db`.`current_patient_logs`"
        "(bed_number,timestamp_start,timestamp_end,accompanied,hfr_count)"
        "VALUES ('{}','{}','{}','{}','{}');".format(777,'2021-06-19 16:54:46','2021-06-19 16:54:51', 1, 0))

new_log = sql_conn.execute(query)

print(new_log)