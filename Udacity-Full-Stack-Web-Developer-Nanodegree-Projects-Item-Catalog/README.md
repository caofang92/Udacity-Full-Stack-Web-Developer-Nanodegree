# Item Catalog Application

## About

￼RESTful web application using the Python Framework Flask along with implementing third-party OAuth authentication, provides a list of items within a variety of categories as well as provides a user registration and authentication system.￼ User can view all items, registered users will have the ability to post, edit and delete their own items. Only the ￼administrator can add, edit and delete a category.

You can visit http://54.201.40.18 for the website deployed

## Running the App

Clone or download this repository

Navigate to the cloned/downloaded folder

Launch the Vagrant VM (vagrant up)

Connect to the VM (vagrant ssh) and change to the project directory (cd /vagrant)

Run database_setup.py and lotsofitems.py

Run server.py (python server.py)

Browse to http://localhost:8000/ in your browser

## Business Rules (Application Logic)

### Functionality for all Users

View all categories and items

Sign up and sign in

### Additional Functionality for Authenticated Users

Create items

Edit items they created

Delete items they created

Sign out

### Additional Functionality for administrator (the first registered user)
Create categories

edit categories

delete categories (all items of this category will be deleted)

## API (JSON) Endpoints
The following API endpoints provide access to category and item data in JSON format. User account details are not needed.

return catalog content in JSON format
http://localhost:8000/catalog/JSON/

return an existing category’s content in JSON format 
http://localhost:8000/catalog/category_name/JSON/

return an existing item’s content in JSON format
http://localhost:8000/catalog/category_name/item_name/JSON/
