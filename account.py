# from enum import auto
# import firebase_admin
import streamlit as st
import preferences as pf
from sqlalchemy import create_engine,text
import pandas as pd
# from firebase_admin import credentials
# from firebase_admin import auth

# cred = credentials.Certificate('mealmaster-4bb1c-7c25349d7a5c.json')
# firebase_admin.initialize_app(cred)


engine = create_engine(
    "sqlite:///meals_db",
    pool_size = 5,
    max_overflow=10,
    pool_recycle=3600,
    pool_pre_ping=True,
)
def app():

    st.title("Hello, Welcome to :red[Meal Master] 🍽️")

    
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'email' not in st.session_state:
        st.session_state.email = ''
    if 'password' not in st.session_state:
        st.session_state.password = ''

    def f():
        
        #user = auth.get_user_by_email(email)
        with engine.connect() as conn:
            count = conn.execute(text(f"""select count(*) from UserProfile where email = "{email}" and password = "{password}" """)).scalar()
            print(email,password)
            print(count)
            if count:

                st.write("Login Successful!")
                username = conn.execute(text(f"""select username from UserProfile where email = "{email}" """)).fetchone()
                print(username[0])
                st.session_state.username = username[0]
                st.session_state.email = email

                st.session_state.signedout = True
                st.session_state.signout = True
            else:
                st.warning("Login Failed!")
    
    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''



    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    if not st.session_state.signedout:
        choice = st.selectbox('Login/Signup', ['Login','Sign Up'])

        if choice == 'Login':
            email = st.text_input('Email Address')
            password = st.text_input('Password', type="password")

            st.button('Login',on_click=f)

        else:

            email = st.text_input('Email Address')
            password = st.text_input('Password',type="password")
            username = st.text_input('User Name')

            if st.button("Create My Account"):
                #user = auth.create_user(email=email,password=password,uid=username)
                conn = st.connection('meals_db', type='sql')
                count = conn.query(str(f"""select count(*) from UserProfile where email = "{email}" and password = "{password}" """))
                if count.iloc[0,0]:
                    pass 
                else:
                    with conn.session as s:
                        s.execute(text(f"""insert into UserProfile (username,email,password) values ("{username}","{email}","{password}")"""))
                        s.commit()
                        s.close()
                conn.reset()
                st.success("Account Created Successfully")
                st.balloons()

    if st.session_state.signout:
        st.text('Name : '+st.session_state.username)
        st.text('Email ID : '+st.session_state.email)
        st.button("Sign out", on_click=t)
