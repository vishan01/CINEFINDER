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
content={
            "id":[],
            "title":[],
             "image":[],
             "recommendation":[]   
             }

query= text(f"SELECT id,title,poster_path,recommendations FROM main_table WHERE credits LIKE '%Jason Statham%' ORDER BY result ASC,vote_average DESC,release_date DESC;")
result = connection.execute(query)
            
for row in result:
    content["id"].append(row[0])
    content["title"].append(row[1])
    content["image"].append("https://image.tmdb.org/t/p/w300_and_h450_bestv2/"+str(row[2]))
    content["recommendation"].append(row[3])
# Define a SQL query
list_value=tuple(content["recommendation"][1].split("-"))
sql_query = text(f"select id,title,poster_path,recommendations FROM main_table WHERE id in {list_value};")

# Execute the query with parameters
result = connection.execute(sql_query)

for row in result:
    print(row)
# Close the connection
connection.close()