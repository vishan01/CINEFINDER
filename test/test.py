import streamlit as st
import load 
from sqlalchemy import create_engine,text

user = load.user
host = load.link
password= load.password
db = load.db

engine = create_engine(f'postgresql://{user}:{password}@{host}/{db}')

class data:
    global content

    content={
            "id":[],
            "title":[],
             "image":[],
             "recommendation":[]   
             }
    def Genre(self,genre):
        with engine.connect() as connection:
            query= text(f"SELECT id,title,poster_path,recommendations FROM main_table WHERE credits LIKE '%{genre}%' ORDER BY vote_average DESC,result ASC;")
            result = connection.execute(query)
            
            for row in result:
                content["id"].append(row[0])
                content["title"].append(row[1])
                content["image"].append("https://image.tmdb.org/t/p/w300_and_h450_bestv2/"+str(row[2]))
                content["recommendation"].append(row[3])
        return content

        



def main():
    caller = data()
    st.set_page_config(page_title="CINEFINDER", page_icon="🖥️")
    st.title(":orange[CINEFINDER]: :blue[THE MOVIE GENIE]")
    option = st.selectbox(
    'How You Want To Find Your CINEMA',
    ('Genre', 'Language', 'Actor/Actress',"Release Year"))

    st.write('You selected:', option)
    if option == 'Genre':
        value = st.selectbox(
            "Select Your Genre",
            ("Action","Horror","Comedy")
        )
        if value:
            content=caller.Genre(value)
            cols = st.columns(len(content["id"]))
            count =0
            for i in cols:
                with i:
                    st.image(content["image"][count])
                    st.header(content["title"][count])
                    count = count+1


if __name__=="__main__":
    main()
