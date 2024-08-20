import streamlit as st
import streamlit_option_menu as option_menu
from sqlalchemy import text
import account, suggestions, about, customize

st.set_page_config(
    page_title="Meal Master",
    initial_sidebar_state= "expanded",
)
class MultiApp:


    def __init__(self) -> None:
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
    
    def run():
        
        with st.sidebar:
            app = option_menu.option_menu(
                menu_title='Meal Master',
                options=['Account','Preferences','Suggestion','About'],
                icons=['person-circle','gear','chat-fill','info-circle-fill'],
                menu_icon='house-heart',
                default_index=0,#Index which is highlighted
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )
        #Beware of spelling mismatch
        if app == "Account":
            account.app()
        if app == "Preferences":
            customize.app()
        if app == "Suggestion":
            suggestions.app()
        if app == "About":
            about.app()
    
    conn = st.connection("meals_db",type="sql")
    with conn.session as s:
        
        s.execute(text("create table if not exists UserProfile (username TEXT NOT NULL, email TEXT NOT NULL,password TEXT NOT NULL,preferences TEXT,allergies TEXT,history TEXT);"))
        s.commit()
        s.close()
    st.session_state.suggest = False
    run()


