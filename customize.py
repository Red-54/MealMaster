import streamlit as st
import preferences as pf
from sqlalchemy import text,create_engine


engine = create_engine(
    "sqlite:///meals_db",
    pool_size = 5,
    max_overflow=10,
    pool_recycle=3600,
    pool_pre_ping=True,
)


def app():
    st.header("You can Add and Delete your Preferences and Allergies here")
    username = st.session_state.username
    if username != '':
        with engine.connect() as conn:
            p = conn.execute(text(f'''select count(*) from UserProfile where username = "{username}" and preferences is null;''')).scalar()
            if p:
                st.session_state.preferences = ''
            else:
                pref = conn.execute(text(f'''select preferences from UserProfile where username = "{username}" ''')).fetchone()
                st.session_state.preferences = pref[0].split(', ')
            print(st.session_state.preferences)
            
            a = conn.execute(text(f''' select count(*) from UserProfile where username = "{username}" and allergies is null;''')).scalar()
            if a:
                st.session_state.allergies = None
            else:
                allergy = conn.execute(text(f'''select allergies from UserProfile where username = "{username}" ''')).fetchone()
                st.session_state.allergies = allergy[0].split(", ")
            
            print(st.session_state.allergies)
            try:
               perfer = st.multiselect(
                    "What are your Dietary Preferences?",pf.cuisine+pf.diet+pf.fruits+pf.dairy+pf.grains+pf.protein+pf.flavours,default=st.session_state.preferences
                )
            except:
                perfer = st.multiselect(
                    "What are your Dietary Preferences?",pf.cuisine+pf.diet+pf.fruits+pf.dairy+pf.grains+pf.protein+pf.flavours)

            try:
               allegries = st.multiselect(
                    "Do you have any Allergies?",pf.allegries,default=st.session_state.allergies
                )
            except:
                allegries = st.multiselect(
                    "Do you have any Allergies?",pf.allegries)


        if st.button("Save"):
            ps = ", ".join(perfer)
            als = ", ".join(allegries)
            conn = st.connection("meals_db",type="sql")
            with conn.session as s:

                s.execute(text(f''' update UserProfile set preferences = "{ps}" where username = "{username}";'''))
                s.execute(text(f''' update UserProfile set allergies = "{als}" where username = "{username}";'''))
                s.commit()
            st.rerun()
    else:
        st.warning("You need to login")
