# Meal Master - AI-Powered Recipe Recommendations 👨‍🍳🤖

**Meal Master** is a simple meal suggestion application built with Streamlit, leveraging the power of Google's Gemini Pro LLM and a SQLite database. 

## Features ✨

* **Personalized Recommendations:** 
    - Suggests recipes based on user dietary preferences (e.g., American 🇺🇸, Italian 🇮🇹) and allergies (e.g., Dairy 🥛, Shellfish 🦐).
    - Considers past liked recipes ❤️ to enhance suggestions.
* **Ingredient-Based Suggestions:** 
    - Users can upload images 📸 of ingredients, and the app uses Gemini to extract ingredient information.
    - Recommends recipes that incorporate the detected ingredients 🍅🥕🧅.
* **Recipe Details:** Provides a full recipe, including ingredients and instructions, in an easy-to-read markdown format.
* **Nutritional Information:** Displays a bar chart 📊 visualizing the estimated nutritional value of the recommended recipe (calories, protein, fat, etc.). 
* **Like and Save:**  Users can "like" 👍 recipes, which are then saved to their history for future reference.

## Technologies Used 💻

* **Frontend:** Streamlit 
* **Language Model:** Google Gemini Pro 
* **Database:** SQLite
* **Database ORM:** SQLAlchemy 
* **Visualization:** Plotly

## Setup and Installation 🚀

1. **Clone the Repository:** `git clone git@github.com:Red-54/MealMaster.git`
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Google Cloud API Key:**
    - Obtain a Google Cloud API Key 🔑 and enable the Gemini API.
    - Create a `secrets.toml` file in your Streamlit app directory.
    - Add the API Key to the `secrets.toml` file:

    ```toml
    [secrets]
    GOOGLE_API_KEY = "your_api_key_here" 
    ```

4. **Run the App:** `streamlit run app.py` 

## Usage 🧑‍💻

1. **Login/Sign-up:** Create an account or log in.
2. **Preferences:**  Go to the "Preferences" section to set your dietary preferences and allergies.
3. **Suggestions:**
    -  Optionally, upload an image of ingredients.
    - Click the "Recommend" button to receive a personalized recipe suggestion.
    - View the recipe details, nutritional information, and "like" ❤️ it to save it to your history.

## Limitations ⚠️

* **No Fine-tuning:** The app currently relies on Gemini's pre-trained capabilities without any fine-tuning. This may lead to occasional inaccuracies in ingredient detection or recipe suggestions.
* **Simplified Recommendations:**  The recommendation system is rule-based and primarily focuses on ingredient matching and dietary restrictions. Collaborative filtering or more advanced AI algorithms are not yet implemented.
* **SQLite Database:**  SQLite is suitable for a small-scale application, but it may not be ideal for handling a large user base or complex data analysis in the future. 

## Future Enhancements ➡️

* **Improved Authentication 🔐:**  Enforce strong password policies and provide options for password recovery.
* **Database Migration:** Consider migrating to a more scalable database (e.g., PostgreSQL) if the application grows significantly.
* **User History  📖:** Allow users to see previously liked recipes or remove them.

## Contributing 🤝

Contributions are welcome! Please open an issue or submit a pull request if you have ideas for improvements. 
