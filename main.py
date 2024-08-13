import streamlit as st
import streamlit_option_menu as option_menu

import account, suggestions, about

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
                options=['Account','Suggestion','About'],
                icons=['person-circle','chat-fill','info-circle-fill'],
                menu_icon='chat-fill',
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
        if app == "Suggestion":
            suggestions.app()
        if app == "About":
            about.app()
    
    run()


