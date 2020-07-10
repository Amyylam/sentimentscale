from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import pandas as pd
import re
import json
import os

class CorpusWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        print(self.path)
        query = parse.urlsplit(self.path).query
        query_dict = parse.parse_qs(query)
        print("This is the query dict:", query_dict)
        #print(query_dict.keys())
        if "style.css" in self.path:
            self.send_header('Content-type','text/css; charset=utf-8')
            self.end_headers()
            f = open("style.css", encoding="utf-8")
            html = f.read()
            f.close()
            self.wfile.write(html.encode("utf-8"))
        elif "script.js" in self.path:
            self.send_header('Content-type','text/javascript; charset=utf-8')
            self.end_headers()
            f = open("script.js", encoding="utf-8")
            html = f.read()
            f.close()
            self.wfile.write(html.encode("utf-8"))
        elif "liked" in query_dict and 'disliked' in query_dict:
            liked_ingredients = query_dict['liked']
            disliked_ingredients = query_dict['disliked']
            recipe_path = r"recipes_4cols.csv"
            unsorted_recipes = load_filter(recipe_path,liked_ingredients,disliked_ingredients)
            random_recipes = unsorted_recipes.sample(frac=1)
            top_recipes = random_recipes['name'][0:10].values
            top_recipes_string = ", ".join([v for v in top_recipes])
            
            #top_recipe = unsorted_recipes['name'].iloc[0].capitalize()

            self.send_header('Content-type','text/html; charset=utf-8')
            self.end_headers()
            #f = open("index.html", encoding="utf-8")
            #html = f.read()
            #f.close()
            #button_html = "<button type='button' name='submit' onclick='add_recipes();' style='width:75px; height:30px;font-size:14'>Nice!</button> "
            hover_html = "<p onmousemove = 'add_recipes();'>"
            hover_end_html = "</p>"
            html = hover_html + top_recipes_string + hover_end_html


            print(html)

            self.wfile.write(html.encode("utf-8"))
        elif "recipe" in query_dict:
            self.send_header('Content-type','text/html; charset=utf-8')
            self.end_headers()


            recipe_path = r"recipes_4cols.csv"
            recipes_df = load_data(recipe_path)
            recipe_name = parse.unquote(query_dict['recipe'][0]) #need to parse a string
            recipe_row = recipes_df.query("name == @recipe_name").iloc[0]
            #print(recipe_row)
            added_html = "<p><strong>"+recipe_row['name'].capitalize()+"</strong></p>"
            added_html += "<p> Ingredients:"+", ".join([i for i in eval(recipe_row['ingredients'])])+"</p>"
            for step in eval(recipe_row['steps']):
                added_html += "<p> * "+step+"</p>"
            added_html += "</br>"
            #print(added_html)
            self.wfile.write(added_html.encode("utf-8"))

        elif self.path == "/":
            self.send_header('Content-type','text/html; charset=utf-8')
            self.end_headers()
            f = open("index.html", encoding="utf-8")
            html = f.read()
            f.close()
            self.wfile.write(html.encode("utf-8"))
        return
##############

def load_data(recipe_path):
    return pd.read_csv(recipe_path,nrows=10000).dropna()

def recipe_bot_query(recipe_db,liked_ingredients):
    
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

def load_filter(recipe_path,liked_ingredients,disliked_ingredients):
    recipe_db = load_data(recipe_path)
    filtered = recipe_bot_query(recipe_db,liked_ingredients)
    removed = recipe_remove(filtered,disliked_ingredients)
    return removed


if __name__ == "__main__":
    http_port = int(os.environ.get("PORT",9996))
    server = HTTPServer(('0.0.0.0', http_port),  CorpusWebServer)
    #server = HTTPServer(('localhost', http_port),  CorpusWebServer)
    server.serve_forever()