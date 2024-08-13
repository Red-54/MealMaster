from enum import auto
import firebase_admin
import streamlit as st
import preferences as pf

from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate('mealmaster-4bb1c-7c25349d7a5c.json')
firebase_admin.initialize_app(cred)



def app():

    st.title("Hello, Welcome to :red[Meal Master] 🍽️")

    choice = st.selectbox('Login/Signup', ['Login','Sign Up'])

    def f():
        try:
            user = auth.get_user_by_email(email)
            st.write("Login Successful!")
        except:
            st.warning("Login Failed!")

    if choice == 'Login':
        email = st.text_input('Email Address')
        password = st.text_input('Password', type="password")

        st.button('Login',on_click=f)

    else:

        email = st.text_input('Email Address')
        password = st.text_input('Password',type="password")
        username = st.text_input('User Name')

        """
         preferences = st.multiselect(
            "What are your Dietary Preferences?",pf.cuisine+pf.diet+pf.dairy+pf.grains+pf.protein+pf.flavours
        )
        #allegries = st.multiselect(
            "Do you have any allegries?",
            pf.allegries
        )

        """
        perfer = st.multiselect(
            "What are your Dietary Preferences?",pf.cuisine+pf.diet+pf.dairy+pf.grains+pf.protein+pf.flavours
        )
        allegries = st.multiselect(
            "Do you have any Allegries?",pf.allegries
        )
        if st.button("Create My Account"):
            user = auth.create_user(email=email,password=password,uid=username)

            st.success("Account Created Successfully")
            st.balloons()
