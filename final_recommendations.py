import json
from tree import SearchTree
with open("restaurants.json",'r') as load_f:
    data_list = json.load(load_f)
data_tree = SearchTree(data_list)

input_category = True
category = ""
while input_category:
    category = input("##Categories available##\n"+", ".join(data_tree.categories_type_list)+" :\n"+"Please select a category:")
    if category not in  data_tree.categories_type_list:
        print("Please enter the correct value")
    else:
        input_category = False

input_price = True
price = ""
while input_price:
    price = input("Please Select price with $ or $$ or $$$ or $$$: ")
    if price not in  data_tree.price_type_list:
        print("Please enter the correct value")
    else:
        input_price = False

input_rating = True
rating = -1
while input_rating:
    rating_str = input("Please Select rating with 2.5 or 3.0 or 3.5 or 4.0 or 4.5 or 5.0: ")
    rating = float(rating_str)
    if rating not in  data_tree.rating_type_list:
        print("Please enter the correct value")
    else:
        input_rating = False

input_close = True
close = False
while input_close:
    close_str = input("Do you want to search for the restaurants that are currently open?(yes/no): ")
    if close_str == 'yes':
        close = False
        input_close = False
    elif close_str == 'no':
        close = True
        input_close = False
    else:
        print("Please only enter yes or no")

search_list = data_tree.search_data(filter_list=[category,price,rating,close])

print("")
print(str(len(search_list)) + " " + "restaurant(s) meet your preference :")
for item in search_list:
    print("")
    print("-----------------------------------------------")
    #print("id:"+item['id'])
    print("name:"+item['name'])
    print("category:"+item['category'])
    print("price:"+item['price'])
    print("rating:"+str(item['rating']))
    print("phone:"+item['phone'])
    if 'location' in item and 'display_address' in item['location']:
        print("location:"+str(item['location']['display_address']))
    print("-----------------------------------------------")


is_exit = False
while is_exit == False:
    name = input("You can enter a restaurant's name to review the customers' comment or enter 'exit' to quit searching:\n")
    if name == 'exit':
        is_exit = True
    else:
        temp = None
        for item in search_list:
            if item['name'] == name:
                temp = item
                break
        if temp == None:
            print("Please enter the correct name: ")
        else:
             if 'reviews' in temp:
                for item in temp['reviews']:
                    print("")
                    print("-----------------------------------------------")
                    print("comment: ", item['review_content'])
                    print("individual rating: ", item['individual_rating'])
                    print("-----------------------------------------------")
                    print("")
            
