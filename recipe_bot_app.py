import streamlit as st

import pandas as pd
import re
import random
from datetime import datetime

## have to set random seed, otherwise the text_input elements will be a mess on if-else conditions

#seed_no = random.randint(0,9) ## cannot be a random number everytime the page reloads
# better fix it for a certain time duration e.g. a day/ a particular hour
seed_no = datetime.now().hour

random.seed(seed_no)

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
    if try_or_not in ["yes","y","sure","alright","ok","okay","why not"] or "yes" in try_or_not:
        sent1 = "These are the steps of making this cuisine:"
        recipe_row = sorted_recipes.iloc[0]
    else:
        recipe_row = sorted_recipes.iloc[1]
        sent1 = "This is another recipe: " +f"`{recipe_row['name'].capitalize()}`" + "  \n  \n" + "Ingredients in this recipe: " + ", ".join(eval(recipe_row['ingredients'])) + "  \n  \n" + "Steps of this recipe:"
    yield sent1
        
    
    for step in eval(recipe_row['steps']): #turn str back into a list
        step_str = "> "+step 
        yield step_str
    
## predefined template for QA 

### text_input element ids are uniquely defined by their label(a string). liked_ingredients(variable assigned to user-input value of text_input) will disappear if page refresh to another text_input element with a different label.
    
Q1_candidates = ["Any ingredient(s) you want to taste in the meal?",
                    "Any food you have in mind to start search?",
                    "Tell me one food you like.",
                    "What ingredients do you like?"]
Q1 = random.choice(Q1_candidates)

Q2_candidates = ["Is there any ingredient(s) you hate? I can filter them out.",
                    "What ingredient(s) would you like to avoid?",
                    "Is there something you don't eat?",
                    "There's plenty of choices! You can narrow down further by removing recipes containing certain ingredients. What would you like to filter?"]
Q2 = random.choice(Q2_candidates)


## get varied replies
def get_R1(matching_recipes_df, liked_ingredients):
    R1_candidates = [f"Okay! {len(matching_recipes_df)} recipes match your choice.", 
                f"I can find {len(matching_recipes_df)}  in the database that contain {' and '.join(liked_ingredients)}.",
                f"Alright! There are  {len(matching_recipes_df)} available for your selection. "]

    R1 = random.choice(R1_candidates)
    return R1 


def get_R2(cleaned_recipes,disliked_ingredients):
    R2_candidates = [f"I see. After filtering out those ingredients, {len(cleaned_recipes)} recipes remain.",
                f"Sure I can remove recipes containing {' and '.join(disliked_ingredients)}! You have narrowed down the number of recipes to {len(cleaned_recipes)}. ",
                f"I don't like {','.join(disliked_ingredients)} too! Now we have  {len(cleaned_recipes)} options left."]
    R2 = random.choice(R2_candidates)
    return R2



## start streamlit interface
recipe_path = "recipes_4cols.csv"
recipe_db = load_data(recipe_path)

st.header("Ask chatbot: What should I cook now?")
st.text("Recipes originated from user-uploaded content on Food.com")

liked_ingredients = st.text_input(Q1,"")
#st.write(liked_ingredients)

if liked_ingredients:
    
    liked_ingredients = re.split('[ ,;//]',liked_ingredients.lower().strip(" !?."))
    matching_recipes_df = recipe_bot_query(liked_ingredients)
    
    R1 = get_R1(matching_recipes_df,liked_ingredients)
    st.write(R1)

    disliked_ingredients = st.text_input(Q2,"")
    #st.write(disliked_ingredients)

    if disliked_ingredients:
        disliked_ingredients = [t for t in re.split('[ ,;//]',disliked_ingredients.lower().strip(" !?.")) if t != ""]
        
        cleaned_recipes = recipe_remove(matching_recipes_df,disliked_ingredients)

        
        st.write(get_R2(cleaned_recipes,disliked_ingredients))

        sort_order = st.text_input("Do you want the first one, a random recipe or the most recent recipe?","")
        if sort_order:

            sorted_recipes = rank_recipe(cleaned_recipes, sort_order.lower())
    
            st.write(f"Here is the recipe: " + "`"+sorted_recipes['name'].iloc[0].capitalize()+"`")
            st.write("Ingredients in this recipe: " +", ".join(eval(sorted_recipes['ingredients'].iloc[0])))

            try_or_not =  st.text_input("Do you want to try it?","").lower()
            if try_or_not:
                for return_str in next_one(try_or_not):
                    st.markdown(return_str)

