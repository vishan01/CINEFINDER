import streamlit as st
import load 
from st_keyup import st_keyup
from sqlalchemy import create_engine,text
import pickle as pkl
import re

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
    def Genre(self,genre,lang):
        with engine.connect() as connection:
            query= text(f"SELECT id,title,poster_path,recommendations FROM main_table WHERE original_language='{lang}' AND genres LIKE '%{genre}%' ORDER BY vote_average DESC,release_date DESC,result ASC;")
            result = connection.execute(query)
            
            for row in result:
                content["id"].append(row[0])
                content["title"].append(row[1])
                content["image"].append("https://image.tmdb.org/t/p/w300_and_h450_bestv2/"+str(row[2]))
                content["recommendation"].append(row[3])
        return content
    def Actor(self,actor,lang):
        with engine.connect() as connection:
            query= text(f"SELECT id,title,poster_path,recommendations FROM main_table WHERE credits LIKE '%{actor}%' ORDER BY result ASC,vote_average DESC,release_date DESC;")
            result = connection.execute(query)
            
            for row in result:
                content["id"].append(row[0])
                content["title"].append(row[1])
                content["image"].append("https://image.tmdb.org/t/p/w300_and_h450_bestv2/"+str(row[2]))
                content["recommendation"].append(row[3])
        return content
    def Release(self,Year,lang):
        with engine.connect() as connection:
            query= text(f"SELECT id,title,poster_path,recommendations FROM main_table WHERE original_language='{lang}' AND release_date BETWEEN DATE '{Year.year}-01-01' AND DATE '{Year}'  ORDER BY release_date DESC,vote_average DESC,result ASC;")
            result = connection.execute(query)
            
            for row in result:
                content["id"].append(row[0])
                content["title"].append(row[1])
                content["image"].append("https://image.tmdb.org/t/p/w300_and_h450_bestv2/"+str(row[2]))
                content["recommendation"].append(row[3])
        return content

        



def main():
    caller = data()
    actor=pkl.load(open("../data/actors.pkl","rb"))
    genre=pkl.load(open("../data/genres.pkl","rb"))
    language = pkl.load(open("../data/lang.pkl","rb"))

    st.set_page_config(page_title="CINEFINDER", page_icon="🖥️")
    st.title(":orange[CINEFINDER]: :blue[THE MOVIE GENIE]")
    lang = st.selectbox(
    'Select Your Language',
    language,
   placeholder="Select Your Language")
    option = st.selectbox(
    'How You Want To Find Your CINEMA',
    ('Genre', 'Actor/Actress',"Release Year"),index=None,
   placeholder="Select Your Way")
    try:
        st.write('You selected:', option)
        if option == 'Genre':
            value = st.selectbox(
                "Select Your Genre",
                genre,index=None,placeholder="Select Your Way"
            )
            if value:
                content=caller.Genre(value,language[lang])
                count =0
                with st.container():
                    col1,col2,col3 = st.columns(3)
                    while(count<20):
                        with col1:
                            st.image(content["image"][count])
                            st.text(content["title"][count])
                            count = count+1
                        with col2:
                            st.image(content["image"][count])
                            st.text(content["title"][count])
                            count = count+1
                        with col3:
                            st.image(content["image"][count])
                            st.text(content["title"][count])
                            count = count+1


        if option == 'Actor/Actress':
            
            value = st.text_input("Enter The Name",key=0)
            value =value.title()
            st.write("Actor Name:", value)
            if value:
                content=caller.Actor(value,language[lang])
                count =0
                with st.container():
                    col1,col2,col3 = st.columns(3)
                    while(count<20):
                        with col1:
                            st.image(content["image"][count])
                            st.text(content["title"][count])
                            count = count+1
                        with col2:
                            st.image(content["image"][count])
                            st.text(content["title"][count])
                            count = count+1
                        with col3:
                            st.image(content["image"][count])
                            st.text(content["title"][count])
                            count = count+1

                        
        if option == 'Release Year':
            value = st.date_input("Enter The Year Of Release",value=None)
            if value:
                
                content=caller.Release(value,language[lang])
                count =0
                with st.container():
                    col1,col2,col3 = st.columns(3)
                    while(count<20):
                        with col1:
                            st.image(content["image"][count])
                            st.text(content["title"][count])
                            count = count+1
                        with col2:
                            st.image(content["image"][count])
                            st.text(content["title"][count])
                            count = count+1
                        with col3:
                            st.image(content["image"][count])
                            st.text(content["title"][count])
                            count = count+1
    except:
        if(count==0):
            st.title("No Movies")
        else:
            st.title("The END")


if __name__=="__main__":
    main()

