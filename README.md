# 507Final-Project

# Overview
Using Yelp Fusion API,  organizing the data related to restaurants into trees. By asking the users their preference about the type of the food, price, ratings, open time, the program will provide restaurants that meet the preference. 

# API used
https://api.yelp.com/v3/businesses/search
https://api.yelp.com/v3/businesses/{id}/reviews

# 3 files are uploaded for the final project:

1. final_getJson.py - used to get restaurants data from Yelp fusion API, and safe;
2. restaurants.json - the restaurants data in json form;
3. final_recommendation.py - the code to excecute the recommendations;

# Data Structure
The restaurant.json file contains 902 restaurants in Chicago, each posess the information about the business_id, name of the restaurant, category, rating, review_count, and review_content, etc.
