import streamlit as st
import preferences as pf
def app():

    st.title("Hello, Welcome to :red[Meal Master] 🍽️")

    choice = st.selectbox('Login/Signup', ['Login','Sign Up'])

    if choice == 'Login':
        email = st.text_input('Email Address')
        password = st.text_input('Password', type="password")

        st.button('Login')

    else:

        email = st.text_input('Email Address')
        password = st.text_input('Password',type="password")
        username = st.text_input('User Name')
        preferences = st.multiselect(
            "What are your Dietary Preferences?",pf.cuisine+pf.diet+pf.dairy+pf.grains+pf.protein+pf.flavours
        )
        allegries = st.multiselect(
            "Do you have any allegries?",
            pf.allegries
        )

