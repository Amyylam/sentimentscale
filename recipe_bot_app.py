import streamlit as st

import pandas as pd

@st.cache
def load_data(recipe_path):
     return pd.read_csv(recipe_path)

def recipe_bot_query(liked_ingredients):
    
    #initialize a new df
    filtered = recipe_db
    for i,ing in enumerate(liked_ingredients):
        mask= filtered['ingredients'].str.contains(ing)
        filtered = filtered[mask]
    
    return filtered

def recipe_remove(matching_recipes_df,disliked_ingredients):
    filtered = matching_recipes_df
    for i,ing in enumerate(disliked_ingredients):
        masked= filtered['ingredients'].str.contains(ing)
        filtered = filtered.mask(masked).dropna()
    
    return filtered

def rank_recipe(cleaned_recipes,sort_order):
    
    if  'random' in sort_order: #random order
        cleaned_recipes = cleaned_recipes.sample(frac=1)
    elif 'recent' in sort_order: #sort by recency
        cleaned_recipes = cleaned_recipes.sort_values("submitted",ascending = False)
    
    return cleaned_recipes

def next_one(try_or_not):
    if try_or_not == "yes":
        sent1 = "These are the steps of making this recipe:"
        recipe_row = sorted_recipes.iloc[0]
    else:
        recipe_row = sorted_recipes.iloc[1]
        sent1 = "This is the next recipe:" +f" {recipe_row['name'].capitalize()}"
    yield sent1
        
    
    for step in eval(recipe_row['steps']): #turn str back into a list
        step_str = "> "+step 
        yield step_str
    
     

## start streamlit interface
recipe_path = "recipes_4cols.csv"
recipe_db = load_data(recipe_path)

st.header("Ask chatbot: What should I cook now?")


liked_ingredients = st.text_input("Any ingredient you want to taste in the meal?","")

if liked_ingredients:
    liked_ingredients = liked_ingredients.lower().strip(" ").split(",")
    matching_recipes_df = recipe_bot_query(liked_ingredients)
    st.write(f"Okay! {len(matching_recipes_df)} recipes match your choice.")

    disliked_ingredients = st.text_input("Is there any ingredient you hate? I can filter them out.","")
    if disliked_ingredients:
        disliked_ingredients = disliked_ingredients.lower().strip(" !?.").split(",")
        cleaned_recipes = recipe_remove(matching_recipes_df,disliked_ingredients)
        st.write(f"I see. After filtering out those ingredients, {len(cleaned_recipes)} recipes remain.")

        sort_order = st.text_input("Do you want the first one, a random recipe or the most recent recipe?","")
        if sort_order:
            sort_order = sort_order.lower()
            sorted_recipes = rank_recipe(cleaned_recipes, sort_order)
    
            st.write("Here is the first recipe: " + sorted_recipes['name'].iloc[0].capitalize())

            try_or_not =  st.text_input("Do you want to try it?","").lower()
            if try_or_not:
                for return_str in next_one(try_or_not):
                    st.markdown(return_str)
