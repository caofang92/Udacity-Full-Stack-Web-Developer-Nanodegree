from flask import Flask, render_template, url_for, \
    request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, Category, Item, User

# New imports for this step
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

from functools import wraps

app = Flask(__name__)

CLIENT_ID = json.loads(
        open('client_secrets.json', 'r').read())['web']['client_id']

APPLICATION_NAME = "Item Catalog Application"

engine = create_engine('sqlite:///itemcatalogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

administrator_id = 1


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r')
                        .read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r')
                            .read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?' \
          'grant_type=fb_exchange_token&client_id=%s&client_secret=%s' \
          '&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange
        we have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then
        we split it on colons to pull out the actual token value and replace
        the remaining quotes with nothing so that it can be used directly
        in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s' \
          '&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)

    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?' \
          'access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['userid'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;' \
              '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?' \
          'access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
                json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?'
           'access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
                json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['userid'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;' \
              '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    credentials = login_session.get('credentials')

    if credentials is None:
        response = make_response(
                json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        response = make_response(
                json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['userid']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    allcategories = session.query(Category).all()

    # retrieve 10 most recent item
    items = session.query(Item).order_by(Item.id.desc()).limit(10).all()

    #  category of each recent item
    categories = []
    for item in items:
        category = session.query(Category).filter_by(id=item.category_id).one()
        categories.append(category)

    if 'username' not in login_session \
            or login_session['userid'] != administrator_id:
        return render_template('publiccatalog.html',
                               allcategories=allcategories,
                               items=items, categories=categories)
    else:
        return render_template('catalog.html', allcategories=allcategories,
                               items=items, categories=categories)


@app.route('/catalog/new/', methods=['GET', 'POST'])
@login_required
def newCategory():
    # only the administrator can add a new category
    if login_session['userid'] != administrator_id:
        return "<script>function myFunction()" \
               "{ alert('You are not authorized to add a category.');}" \
               "</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if (len(request.form['name']) == 0):
            flash("Name can't be empty!")
            return render_template('newcategory.html')
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        flash("New Category created!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newcategory.html')


@app.route('/catalog/<string:category_name>/edit/', methods=['GET', 'POST'])
@login_required
def editCategory(category_name):
    # only the administrator can edit a category
    if login_session['userid'] != administrator_id:
        return "<script>function myFunction()" \
               "{ alert('You are not authorized to edit this category.');}" \
               "</script><body onload='myFunction()''>"

    try:
        editedCategory = session.query(Category).filter_by(
                name=category_name).one()
    except NoResultFound:
        return "<script>function myFunction() " \
               "{alert('the category does not exist.');}" \
               "</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            session.add(editedCategory)
            session.commit()
            flash("Category Successfully Edited!")
            return redirect(url_for('showCatalog'))
        else:
            flash("Name can't be empty!")
            return render_template('editcategory.html',
                                   category=editedCategory)
    else:
        return render_template('editcategory.html', category=editedCategory)


@app.route('/catalog/<string:category_name>/delete/', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_name):
    # only the administrator can delete a category
    if login_session['userid'] != administrator_id:
        return "<script>function myFunction()" \
               "{ alert('You are not authorized to delete this category.');}" \
               "</script><body onload='myFunction()''>"

    try:
        deletedCategory = session.query(Category).filter_by(
                name=category_name).one()
    except NoResultFound:
        return "<script>function myFunction() " \
               "{alert('the category does not exist.');}" \
               "</script><body onload='myFunction()''>"

    if request.method == 'POST':
        # delete the category
        session.delete(deletedCategory)
        session.commit()

        # delete all items of the category
        deleteditems = session.query(Item).filter_by(
                category_id=deletedCategory.id).all()
        for item in deleteditems:
            session.delete(item)
            session.commit()
        flash("Category Successfully Deleted!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deletecategory.html', category=deletedCategory)


@app.route('/catalog/<string:category_name>/items')
def showCategory(category_name):
    try:
        selectedcategory = session.query(Category).filter_by(
                name=category_name).one()
    except NoResultFound:
        return "<script>function myFunction() " \
               "{alert('the category does not exist.');}" \
               "</script><body onload='myFunction()''>"

    items = session.query(Item).filter_by(category_id=selectedcategory.id)

    if 'username' not in login_session \
            or login_session['userid'] != administrator_id:
        return render_template('publiccategory.html',
                               category=selectedcategory, items=items)
    else:
        return render_template('category.html',
                               category=selectedcategory, items=items)


@app.route('/catalog/<string:category_name>/new/', methods=['GET', 'POST'])
@login_required
def newItem(category_name):
    try:
        category = session.query(Category).filter_by(name=category_name).one()
    except NoResultFound:
        return "<script>function myFunction() " \
               "{alert('the category does not exist.');}" \
               "</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if len(request.form['name']) == 0:
            flash("Name can't be empty!")
            return render_template('newitem.html', category=category)

        if len(request.form['description']) == 0:
            flash("Description can't be empty!")
            return render_template('newitem.html', category=category)

        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       category_id=category.id,
                       user_id=login_session['userid'])
        session.add(newItem)
        session.commit()
        flash("new item created!")
        return redirect(url_for('showCategory', category_name=category.name))
    else:
        return render_template('newitem.html', category=category)


@app.route('/catalog/<string:category_name>/<string:item_name>/edit/',
           methods=['GET', 'POST'])
@login_required
def editItem(category_name, item_name):
    try:
        category = session.query(Category).filter_by(name=category_name).one()
        editedItem = session.query(Item).filter_by(
                name=item_name, category_id=category.id).one()
    except NoResultFound:
        return "<script>function myFunction() " \
               "{alert('the item of that category does not exist.');}" \
               "</script><body onload='myFunction()''>"

    if login_session['userid'] != editedItem.user_id:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to edit this item.');}" \
               "</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']

        session.add(editedItem)
        session.commit()
        flash("item successfully edited!")
        return redirect(url_for('showItem', category_name=category.name,
                                item_name=request.form['name']))
    else:
        return render_template('edititem.html', item=editedItem,
                               category=category)


@app.route('/catalog/<string:category_name>/<string:item_name>/delete/',
           methods=['GET', 'POST'])
@login_required
def deleteItem(category_name, item_name):
    try:
        category = session.query(Category).filter_by(name=category_name).one()
        deletedItem = session.query(Item).filter_by(
                name=item_name, category_id=category.id).one()
    except NoResultFound:
        return "<script>function myFunction() " \
               "{alert('the item of that category does not exist.');}" \
               "</script><body onload='myFunction()''>"

    if login_session['userid'] != deletedItem.user_id:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to delete that item.');}" \
               "</script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("item successfully deleted!")
        return redirect(url_for('showCategory', category_name=category.name))
    else:
        return render_template('deleteitem.html', category=category,
                               item=deletedItem)


@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItem(category_name, item_name):
    try:
        category = session.query(Category).filter_by(
                name=category_name).one()
        selecteditem = session.query(Item).filter_by(
                name=item_name, category_id=category.id).one()
    except NoResultFound:
        return "<script>function myFunction() " \
               "{alert('the item of that category does not exist.');}" \
               "</script><body onload='myFunction()''>"

    creator = getUserInfo(selecteditem.user_id)
    if 'username' not in login_session \
            or login_session['userid'] != selecteditem.user_id:
        return render_template('publicitem.html', item=selecteditem,
                               category=category, creator=creator)
    else:
        return render_template('item.html', item=selecteditem,
                               category=category, creator=creator)


@app.route('/catalog/JSON/')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[i.serialize for i in categories])


@app.route('/catalog/<string:category_name>/JSON/')
def categoryitemsJSON(category_name):
    try:
        selectedcategory = session.query(Category).filter_by(
                name=category_name).one()
        items = session.query(Item).filter_by(
                category_id=selectedcategory.id).all()
    except NoResultFound:
        return "<script>function myFunction() " \
               "{alert('the category does not exist.');}" \
               "</script><body onload='myFunction()''>"

    return jsonify(Items=[i.serialize for i in items])


@app.route('/catalog/<string:category_name>/<string:item_name>/JSON/')
def ItemJSON(category_name, item_name):
    try:
        selectedcategory = session.query(Category).filter_by(
                name=category_name).one()
        selecteditem = session.query(Item).filter_by(
                category_id=selectedcategory.id, name=item_name).one()
    except NoResultFound:
        return "<script>function myFunction() " \
               "{alert('the category or the item does not exist.');}" \
               "</script><body onload='myFunction()''>"

    return jsonify(selecteditem=[selecteditem.serialize])


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
