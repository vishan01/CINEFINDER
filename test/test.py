import streamlit as st

def main():
    st.set_page_config(page_title="CINEFINDER", page_icon="🖥️")
    st.title(":orange[CINEFINDER]: :blue[THE MOVIE GENIE]")
    option = st.selectbox(
    'How You Want To Find Your CINEMA',
    ('Genre', 'Language', 'Actor/Actress',"Release Year"))

    st.write('You selected:', option)


if __name__=="__main__":
    main()
