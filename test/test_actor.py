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
sql_query = text("""
SELECT 
    actor_name
FROM 
    main_table,
    unnest(array(SELECT DISTINCT unnest(string_to_array(credits, '-')))) AS actor_name
WHERE
    original_language='en' AND
    credits IS NOT NULL AND credits != '';
""")

# Execute the query with parameters
result = connection.execute(sql_query)

for row in result:
    print(row)
# Close the connection
connection.close()