import streamlit as st
import preferences as pf
def app():
    st.header("You can Add and Delete your Preferences and Allergies here")
    perfer = st.multiselect(
        "What are your Dietary Preferences?",pf.cuisine+pf.diet+pf.dairy+pf.grains+pf.protein+pf.flavours
    )
    allegries = st.multiselect(
        "Do you have any Allegries?",pf.allegries
    )
    
    st.button("Save")

