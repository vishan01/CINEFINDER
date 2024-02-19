import streamlit as st
import load 
from sqlalchemy import create_engine,text
import pickle as pkl
from streamlit_searchbox import st_searchbox
from itertools import chain


user = load.user
host = load.link
password= load.password
db = load.db

engine = create_engine(f'postgresql://{user}:{password}@{host}/{db}')


if "recom" not in st.session_state:
    st.session_state["recom"]=False
if "search" not in st.session_state:
    st.session_state["search"]=False

class data:
    global content
    

    content={
            "id":[],
            "title":[],
             "image":[],
             "recommendation":[],
             "overview":[]   
             }
    def Genre(self,genre,lang):
        with engine.connect() as connection:
            query= text(f"SELECT id,title,poster_path,recommendations,overview,release_date FROM main_table WHERE original_language='{lang}' AND genres LIKE '%{genre}%'  AND poster_path IS NOT NULL  AND release_date IS NOT NULL ORDER BY popularity DESC, vote_average DESC LIMIT 100 ;")
            result = connection.execute(query)
            result=list(set(result))
            
            for row in result:
                content["id"].append(row[0])
                content['title'].append(row[1])
                content["image"].append("https://image.tmdb.org/t/p/w300_and_h450_bestv2/"+str(row[2]))
                content["recommendation"].append(row[3])
                content["overview"].append(row[4])
        return content
    def Actor(self,actor,lang):
        with engine.connect() as connection:
            query= text(f"SELECT id,title,poster_path,recommendations,overview FROM main_table WHERE credits LIKE '%{actor}-%' AND poster_path IS NOT NULL AND release_date IS NOT NULL ORDER BY release_date DESC, result,  popularity DESC,vote_average DESC ;")
            result = connection.execute(query)
            result=list(set(result))
            for row in result:
                content["id"].append(row[0])
                content['title'].append(row[1])
                content["image"].append("https://image.tmdb.org/t/p/w300_and_h450_bestv2/"+str(row[2]))
                content["recommendation"].append(row[3])
                content["overview"].append(row[4])
        return content
    def Release(self,Year,lang):
        with engine.connect() as connection:
            query= text(f"SELECT id,title,poster_path,recommendations,overview FROM main_table WHERE original_language='{lang}' AND release_date BETWEEN DATE '{Year.year}-01-01' AND DATE '{Year}'  AND poster_path IS NOT NULL AND release_date IS NOT NULL AND recommendations IS NOT NULL ORDER BY release_date DESC,vote_average DESC,result ASC;")
            result = connection.execute(query)
            result=list(set(result))
            for row in result:
                content["id"].append(row[0])
                content['title'].append(row[1])
                content["image"].append("https://image.tmdb.org/t/p/w300_and_h450_bestv2/"+str(row[2]))
                content["recommendation"].append(row[3])
                content["overview"].append(row[4])
        return content

    def Randomize(self,value,lang):
        
        with engine.connect() as connection:
            query = text(f"SELECT id,title,poster_path,recommendations,overview FROM main_table WHERE vote_average>={value} AND original_language='{lang}' AND release_date>= DATE '2018-01-01'  AND poster_path IS NOT NULL AND recommendations IS NOT NULL ORDER BY release_date DESC, result,  popularity DESC,vote_average DESC ;")
            result = connection.execute(query)
            result=list(set(result))
            for row in result:
                content["id"].append(row[0])
                content['title'].append(row[1])
                content["image"].append("https://image.tmdb.org/t/p/w300_and_h450_bestv2/"+str(row[2]))
                content["recommendation"].append(row[3])
                content["overview"].append(row[4])
        return content
    
    def recommend(self,m_list):
        m_list=tuple(m_list.split("-"))
        with engine.connect() as connection:
            query = text(f"SELECT id,title,poster_path,recommendations,overview FROM main_table WHERE id in {m_list}  AND poster_path IS NOT NULL ORDER BY result ASC, vote_average DESC;")
            result = connection.execute(query)
            result=list(set(result))
            for row in result:
                content["id"].append(row[0])
                content['title'].append(row[1])
                content["image"].append("https://image.tmdb.org/t/p/w300_and_h450_bestv2/"+str(row[2]))
                content["recommendation"].append(row[3])
                content["overview"].append(row[4])
        return content
    def movie_name(self,name):
        with engine.connect() as connection:
            query = text(f"SELECT id,title,poster_path,recommendations,overview FROM main_table WHERE title LIKE '%{name}%'  AND poster_path IS NOT NULL ORDER BY result ASC, vote_average DESC;")
            result = connection.execute(query)
            result=list(set(result))
            for row in result:
                content["id"].append(row[0])
                content['title'].append(row[1])
                content["image"].append("https://image.tmdb.org/t/p/w300_and_h450_bestv2/"+str(row[2]))
                content["recommendation"].append(row[3])
                content["overview"].append(row[4])
        return content
    
@st.cache_data
def name_suggestor(name):
    name = name.lower()
    with engine.connect() as connection:
        query = text(f"SELECT title FROM main_table WHERE LOWER(title) LIKE '%{name}%'  AND poster_path IS NOT NULL ORDER BY result ASC, vote_average DESC;")
        result = connection.execute(query)
        result=list(set(result))
        result = list(chain.from_iterable(result))
    return result
    
def display(content):
    count =0
    with st.container():
        col1,col2,col3 = st.columns(3)
        try:
            while(count<20):
                with col1:
                    with st.form(key=f"{content['title'][count]}"):
                        st.image(content["image"][count])
                        st.text(content['title'][count])
                        submit=st.form_submit_button("Recommend")
                        if submit:
                            st.session_state["recom"]=content["recommendation"][count]
                        with st.expander("Description"):
                            st.write(content["overview"][count])
                        count = count+1 
                                
                        
                with col2:
                    with st.form(key=f"{content['title'][count]}"):
                        st.image(content["image"][count])
                        st.text(content['title'][count])                        
                        submit=st.form_submit_button("Recommend")
                        if submit:
                            st.session_state["recom"]=content["recommendation"][count]
                        with st.expander("Description"):
                            st.write(content["overview"][count])
                        count = count+1 
                                
                        
                with col3:
                    with st.form(key=f"{content['title'][count]}"):
                        st.image(content["image"][count])
                        st.text(content['title'][count])
                        submit=st.form_submit_button("Recommend")
                        if submit:
                            st.session_state["recom"]=content["recommendation"][count]
                        with st.expander("Description"):
                            st.write(content["overview"][count])
                        count = count+1 
                                
        except:
            st.title("Click on Back to Home to Search differently")
            st.session_state["recom"]=False
 



def main():
    caller = data()
    genre=pkl.load(open("../data/genres.pkl","rb"))
    language = pkl.load(open("../data/lang.pkl","rb"))
    count=0
    st.set_page_config(page_title="CINEFINDER", page_icon="🖥️",layout="wide")
    st.title(":orange[CINEFINDER]: :blue[THE MOVIE GENIE]")
    lang = st.selectbox(
    'Select Your Language',
    language,
   placeholder="Select Your Language")
    option = st.selectbox(
    'How You Want To Find Your CINEMA',
    ("Randomize",'Genre', 'Actor/Actress',"Release Year"),index=None,
   placeholder="Select Your Way")
    with st.sidebar:
        st.session_state["search"]=st_searchbox(name_suggestor,key="Searchbox",label="Search by Movie Name",clear_on_submit=True)
        if st.button("Back to Home State"):
            st.session_state["recom"]=False
            st.session_state["search"]=False

    try:
        
        if st.session_state["recom"]:
                content=caller.recommend(st.session_state["recom"])
                display(content)      
                
        else:
            st.write('You selected:', option)
            if st.session_state["search"]:                    
                    content=caller.movie_name(st.session_state["search"])
                    display(content)
            elif option == 'Randomize':
                value=7
                if value:                    
                    content=caller.Randomize(value,language[lang])
                    display(content)             
            elif option == 'Genre':
                value = st.selectbox(
                    "Select Your Genre",
                    genre,index=None,placeholder="Select Your Way"
                )
                if value:
                    content=caller.Genre(value,language[lang])
                    display(content)                        
            elif option == 'Actor/Actress':
                value = st.text_input("Enter The Name",key=0)
                if value!=value.upper():
                    value =value.title()
                st.write("Actor Name:", value)
                if value:
                    content=caller.Actor(value,language[lang])
                    display(content)            
            elif option == 'Release Year':
                value = st.date_input("Enter The Year Of Release",value=None)
                if value:
                    content=caller.Release(value,language[lang])
                    display(content)

    except(AttributeError):
        if(count==0):
            st.title("No Movies")
        else:
            st.title("The End😅")
        
        
        
    


if __name__=="__main__":
    main()

