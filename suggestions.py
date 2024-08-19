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
engine = create_engine(
    "sqlite:///meals_db",
    pool_size = 5,
    max_overflow=10,
    pool_recycle=3600,
    pool_pre_ping=True,
)

genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))
st.session_state.preferences = ''
st.session_state.allergies = ''
st.session_state.response = ''
st.session_state.nutrient_names = []
st.session_state.nutrient_values = []
if "show" not in st.session_state:
    st.session_state.show = False


def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt])
        return response.text
    except ValueError:
        get_gemini_response(prompt)

def get_ingredients(img):
    try:
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir,img.name)
        with open(path,"wb") as f:
            f.write(img.getvalue())
        ind = genai.upload_file(path=path)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        response = model.generate_content([ind,"Just give list of food ingredients in given file."])
        return response.text
    except:
        get_ingredients(img)

def get_nutrients(response):
    model = genai.GenerativeModel('gemini-pro')
    prompt = str("""Give the nutritional value of the above recipe in the format {"Calories": value, "Protein": value, "Fat": value, "Cholesterol": value, "Carbohydrates": value, "Fiber": value, "Sodium" : value} just give the key values pairs nothing else and Most important you must only give the output in json do not return empty dictionary json the json must contain some positive integer""")
    try:
        nutrients = model.generate_content([prompt,response])
        return nutrients.text
    except:
        get_nutrients(response)

def get_key_values(nutrient):
    try:
        nutri = json.loads(nutrient)
        nutrient_names = list(nutri.keys())
        nutrient_values = list(nutri.values())
        return nutrient_names, nutrient_values
    except:
        get_key_values(nutrient)


def get_recipe_title(response):
    model = genai.GenerativeModel('gemini-pro')
    prompt = "You just have to give title of the recipe nothing else just the title of the recipe"
    try:
        title = model.generate_content([prompt,response])
        return title.text
    except:
        get_recipe_title(response)


def app():
    username = st.session_state.username
    st.header("Suggestions")
    if st.session_state.username == '':
        st.warning("You must Login First!")
        pass
    else:
        response = ''
        fig = go.Figure(data=[go.Bar(x=[],y=[])])

        with engine.connect() as conn:
            p = conn.execute(text(f'''select count(*) from UserProfile where username = "{username}" and preferences is null;''')).scalar()
            if p:
                st.session_state.preferences = ''
            else:
                pref = conn.execute(text(f'''select preferences from UserProfile where username = "{username}" ''')).fetchone()
                st.session_state.preferences = pref[0].split(', ')
            print(st.session_state.preferences)

            a = conn.execute(text(f'''select count(*) from UserProfile where username = "{username}"  and allergies is null;''')).scalar()
            if a:
                st.session_state.allergies = ''
            else:
                allerg = conn.execute(text(f'''select allergies from UserProfile where username = "{username}" ''')).fetchone()
                st.session_state.allergies = allerg[0].split(', ')
            print(st.session_state.allergies)

            h = conn.execute(text(f''' select count(*) from UserProfile where username = "{username}" and history is null'''))

            if h:
                st.session_state.history = ''
            else:
                history = conn.execute(text(f''' select history from UserProfile where username = "{username}" ''')).fetchone()
                st.session_state.history = history[0].split(', ')

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
            also you can recommend based on past liked recipes : {st.session_state.history}
            for example if the preference is American and allergies are Peanut
            The response should be in markdown of Recipe of hamburger or any other American cuisine but any recipe should not contain any allergies mention as Peanut is mentioned the recipe for hamburger should not contain Peanut as Ingredient'''
            print(prefer)
            response = get_gemini_response(prefer)
            st.session_state.response = response
            st.session_state.show = True
            nutrient = get_nutrients(response)
            st.session_state.nutrient_names, st.session_state.nutrient_values = get_key_values(nutrient)         
    fig = go.Figure(data=[go.Bar(x=st.session_state.nutrient_names,y=st.session_state.nutrient_values)])

    if st.session_state.show:
        st.markdown(st.session_state.response)
        if st.session_state.nutrient_names and st.session_state.nutrient_values:
            st.plotly_chart(fig,use_container_width=True)
        else:
            pass
        if st.button(":heart:"):   
            updated_history = str(get_recipe_title(st.session_state.response)) + ", " + st.session_state.history
            with engine.connect() as conn:
                conn.execute(text(f'''UPDATE UserProfile SET history = "{updated_history}" WHERE username = "{username}";'''))
                conn.commit()
    else:
        pass
