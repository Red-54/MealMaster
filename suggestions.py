from plotly.graph_objs import XAxis
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
import streamlit as st
from sqlalchemy import text,create_engine
import tempfile
import plotly.graph_objects as go
import json
st.session_state.preferences = ''
st.session_state.allergies = ''
engine = create_engine(
    "sqlite:///meals_db",
    pool_size = 5,
    max_overflow=10,
    pool_recycle=3600,
    pool_pre_ping=True,
)

genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt])
    return response.text

def get_ingredients(img):
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir,img.name)
    with open(path,"wb") as f:
        f.write(img.getvalue())
    ind = genai.upload_file(path=path)
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([ind,"Just give list of food ingredients in given file."])
    return response.text

def get_nutrients(response):
    model = genai.GenerativeModel('gemini-pro')
    prompt = str("""Give the nutritional value of the above recipe in the format {"Calories": value, "Protein": value, "Fat": value, "Cholesterol": value, "Carbohydrates": value, "Fiber": value, "Sodium" : value} just give the key values pairs nothing else and Most important you must only give the output in json """)
    nutrients = model.generate_content([prompt,response])
    return nutrients.text



def app():
    st.header("Suggestions")
    if st.session_state.username == '':
        st.warning("You must Login First!")
        pass
    else:
        username = st.session_state.username
        with engine.connect() as conn:
            p = conn.execute(text(f'''select count(*) from UserProfile where username = "{username}" and preferences is null;''')).scalar()
            if p:
                st.session_state.preferences = ''
            else:
                pref = conn.execute(text(f'''select preferences from UserProfile where username = "{username}" ''')).fetchone()
                st.session_state.preferences = pref[0].split(', ')
            print(st.session_state.preferences)

        upload_img = st.file_uploader("You can upload image of Ingredients(optional)",type=['png','jpg'])

        if upload_img is not None:
            indgredients = get_ingredients(upload_img,)
        else:
            indgredients = ''
        if st.button("Recommend"):
            prefer = f'''
            You should only respond in markdown
            You are greatest Meal Suggestioner
            based on the preferences : {st.session_state.preferences} and allergies : {st.session_state.allergies} and you should try to include the given indgredients which are : {indgredients} it is okay to use other ingredients required for the recipes if not given then use any required also it is not compulsory to use all the ingredients just the needed ones
            You suggest only one Recipe
            for example if the preference is American and allergies are Peanut
            The response should be in markdown of Recipe of hamburger or any other American cuisine but any recipe should not contain any allergies mention as Peanut is mentioned the recipe for hamburger should not contain Peanut as Ingredient'''
            print(prefer)
            response = get_gemini_response(prefer)
            nutrient = get_nutrients(response)
            nutrient = json.loads(nutrient)
            nutrient_names = list(nutrient.keys())
            nutrient_values = list(nutrient.values())

            fig = go.Figure(data=[go.Bar(x=nutrient_names,y=nutrient_values)])

            st.markdown(response)
            st.plotly_chart(fig,use_container_width=True)

        
