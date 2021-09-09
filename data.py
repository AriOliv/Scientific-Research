import psycopg2
import getpass
import pandas as pd
from datetime import date, datetime

conn = psycopg2.connect(
    database = "postgres",
    user = "postgres",
    password = "postgres",  
    host = "localhost",
    port = "5432"
)

cursor = conn.cursor()
sql_file = open('data/calls_202103111126.sql','r')
cursor.execute(sql_file.read())

try:
    df = pd.read_sql("""
    select * 
    from ic.calls;  
    """, conn)
    
    df1 = pd.read_sql("""
    select beginning,  count(beginning)
    from ic.calls
    group by beginning;  
    """, conn)
except Exception as err:
    print(err)
    print("I can't drop our test database!")

df['DATA'] = pd.to_datetime(df["beginning"])
df.set_index('DATA', inplace = True)
col = [list(df.columns)[index] for index in [3,4,5,6,11]]

