from datetime import datetime, timedelta
import shutil
import psycopg2

#connection to database
conn = psycopg2.connect("dbname=framesdb user=dbuser host=localhost password=password")
cur = conn.cursor()

#query to get paths to delete local files
days = 0
query = f"SELECT * from camera_api_data WHERE timestamp < NOW() - INTERVAL '{days} days'"
cur.execute(query)
results = cur.fetchall()
paths_list = []
for i in results:
    paths_list.append(str(i[5]))

for folder in paths_list:
    try:
        shutil.rmtree(folder)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

#deletes entries in DB
query2 = f"DELETE FROM camera_api_data WHERE timestamp < NOW() -INTERVAL '{days} days'"
cur.execute(query2)


conn.commit()