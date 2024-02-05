import load 
from sqlalchemy import create_engine,text
import pandas as pd

user = load.user
host = load.link
password= load.password
db = load.db


engine = create_engine(f'postgresql://{user}:{password}@{host}/{db}')

# Create a connection
connection = engine.connect()

# Define a SQL query
sql_query = text("SELECT * FROM main_table where credits like '%%Jason Statham%' LIMIT 5;")

# Execute the query with parameters
result = connection.execute(sql_query)

for row in result:
    print(row)
# Close the connection
connection.close()