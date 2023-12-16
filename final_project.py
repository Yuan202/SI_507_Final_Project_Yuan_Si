#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import requests

def get_cache_key(url, params):
    return url + "_".join([f"{k}-{v}" for k, v in params.items()])

def get_data_from_api(url, params, api_key):
    cache_key = get_cache_key(url, params)
    if cache_key in cache:
        return cache[cache_key]
    else:
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers, params=params)
        cache[cache_key] = response.json()
        save_cache(cache)
        return cache[cache_key]

# Load and save cache functions remain the same as previously provided


# In[4]:


def get_restaurants(location, api_key, term='restaurants'):
    url = 'https://api.yelp.com/v3/businesses/search'
    params = {'location': location, 'term': term}
    return get_data_from_api(url, params, api_key)



# In[5]:


class RestaurantNode:
    def __init__(self, name, details):
        self.name = name
        self.details = details  # Dictionary containing details like rating, cuisine, etc.
        self.children = []  # Child nodes can be subcategories

    def add_child(self, child_node):
        self.children.append(child_node)


# In[6]:


def recommend_restaurants(root_node, preferences):
    # This is a placeholder function.
    # The actual implementation will depend on how you want to match preferences.
    recommended = []
    for child in root_node.children:
        if child.details['cuisine'] == preferences['cuisine']:
            recommended.append(child)
    return recommended


# In[19]:


import sqlite3
import os

def create_connection(db_name):
   
    home_dir = os.path.expanduser('~')
    db_path = os.path.join(home_dir, db_name)
    conn = sqlite3.connect(db_path)
    return conn

def setup_database(conn):
    create_restaurant_table = """
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        cuisine TEXT,
        rating REAL,
        location TEXT
    );
    """
    conn.execute(create_restaurant_table)
    conn.commit()

# Example usage
conn = create_connection('restaurants.db')
setup_database(conn)



# In[20]:


from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        # Process the search query and fetch results
        # For now, we are redirecting to the home page
        return redirect(url_for('home'))
    return render_template('search.html')  # Create a search.html template

if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:


def add_reviews_table(conn):
    create_reviews_table = """
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY,
        restaurant_id INTEGER,
        user_name TEXT,
        rating INTEGER,
        comment TEXT,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
    );
    """
    conn.execute(create_reviews_table)
    conn.commit()

# Call this function after setting up the database
add_reviews_table(conn)


# In[ ]:


@app.route('/restaurant/<int:restaurant_id>', methods=['GET', 'POST'])
def restaurant(restaurant_id):
    if request.method == 'POST':
        user_name = request.form['user_name']
        rating = request.form['rating']
        comment = request.form['comment']
        # Save the review to the database
        # Redirect to the same page to display the review
        return redirect(url_for('restaurant', restaurant_id=restaurant_id))
    # Fetch restaurant details and reviews from the database
    return render_template('restaurant.html', restaurant=restaurant_data, reviews=reviews_data)


# In[1]:




