# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 17:02:29 2020

@author: gen80
"""

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import json

recipe_path = r"recipes_5cols.csv"
recipe_df = pd.read_csv(recipe_path)

with open(r"ingredients.json") as f:
    d = json.load(f)

ingredients_set = set(d)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
        
        html.H1("What should I cook now?"),
        html.P("Recipes originated from user-uploaded content on Food.com"),
        html.Hr(),
        html.P("Any ingredient(s) you want to taste in the meal?"),
        
        dcc.Dropdown(
                id = 'liked_ingredients',
                options = [{'label': i[0].capitalize()+i[1:], 'value': i} for i in ingredients_set],
                value = [], #no default value
                multi=True),
        
        html.P("Is there any ingredient you hate? I can filter them out."),
 
        dcc.Dropdown(
                id = 'disliked_ingredients',
                options = [{'label': i[0].capitalize()+i[1:], 'value': i} for i in ingredients_set],
                value = [], #no default value
                multi=True,
                ),
        
        html.P(
        id='confirm', children = ""),
                
        html.P("You can sort recipes by random order or recency"),
        
        dcc.RadioItems(
                id = 'sort_order',
                options = [{"label":" Original order ", "value":"first"}, {"label":" Random order ", "value":"random"}, {"label":" Most recent","value":"recent"}],
                labelStyle={'display': 'block'}
                ),
        
        html.Hr(),
        html.P("Here are first few recipes matching your filtering criteria, click one to see cooking steps:"),        
        
        dcc.RadioItems(id = 'pick_a_recipe',
                       labelStyle={'display': 'block'},
                       value = ''),
                
        #html.P("Here is one recipe of your choice:"),
        html.Hr(),
        
        
        dcc.Markdown(id="recipe_container", children = ""),
        dcc.Markdown(id="recipe_ingredients_container", children = ""),
        
        dcc.Markdown(id="recipe_steps_container", children = "")
        
        ## button -- next one
        
        ])




@app.callback(
        [Output("pick_a_recipe","options"),
        Output("pick_a_recipe","value"),
        Output("confirm","children")],
        [Input("liked_ingredients","value"),
        Input("disliked_ingredients","value"),
        Input("sort_order","value")]
        )
def screen_by_liked_ingredients(liked_ingredients, disliked_ingredients, sort_order):
    filtered = recipe_df
    if liked_ingredients:
        for i,ing in enumerate(liked_ingredients):
            mask= filtered['ingredients'].str.contains(ing)
            filtered = filtered[mask]
    
    if disliked_ingredients:
        for i,ing in enumerate(disliked_ingredients):
            masked= filtered['ingredients'].str.contains(ing)
            filtered = filtered.mask(masked).dropna()
        
    
    if len(filtered) == 0:
        return [],"", "0 recipes matched your filtering criteria"
    cleaned_recipes = filtered
    if sort_order:
        if  'random' in sort_order: #random order
            cleaned_recipes = cleaned_recipes.sample(frac=1)
        elif 'recent' in sort_order: #sort by recency
            cleaned_recipes = cleaned_recipes.sort_values("submitted",ascending = False)

    recipes_no = len(filtered)
    

    if recipes_no >= 5:
        recipe_rows = cleaned_recipes[0:5]
        show_recipe = 5
    elif recipes_no >= 3:
        recipe_rows = cleaned_recipes[0:3]
        show_recipe = 3
    else:
        recipe_rows = cleaned_recipes
        show_recipe = recipes_no

    if liked_ingredients:
        options = [{'label':recipe_rows.iloc[i]['name'].capitalize(), 'value':recipe_rows.iloc[i]['name']} for i in range(show_recipe)]
        default_option = recipe_rows.iloc[0]['name']
        return options, default_option, f"{recipes_no} recipes matched your filtering criteria"
    else:
        return [],"", ""

    

@app.callback(
       [Output("recipe_container","children"),
       Output("recipe_ingredients_container","children"),
       Output("recipe_steps_container","children")],
       [Input("pick_a_recipe","value")]
       )
def update_recipe(recipe_name):
    if recipe_name != '':
        recipe_row = recipe_df[recipe_df['name']==recipe_name].iloc[0] #to a single row
    
        url = r"https://www.food.com/recipe/"+"-".join(str(recipe_row['name']).split())+"-" +str(recipe_row['id'])
        recipe_brief = "#### [" +str(recipe_row['name']).capitalize() + "]("+url+")"
        recipe_ingredients = "Ingredients in this recipe: " + ", ".join(eval(recipe_row['ingredients']))
        steps = []
        steps.append("> Steps of this recipe:")
        for step in eval(recipe_row['steps']): #turn str back into a list
            step_str = "* `"+step + "`"
            steps.append(step_str)
        
        return recipe_brief, recipe_ingredients, steps
    else:
        return "","",""

if __name__ == '__main__':
    app.run_server(debug=True) 

