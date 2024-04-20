from flask import Flask, request, redirect, render_template, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from datetime import datetime
import os
import dotenv


# TODO: Add blueprints/possibly change file structure to categorize scripts by type/function depending on project size
# Set limit on the number of ingredients a user can put in a recipe (idk, 30?).
# Consider instructions to be inserted in a number of steps like ingredients to give it structure and automatically number them. 
#   (might skip for now until more functionality is added towards project completion.)
# Consider standardizing metric/imperial units instead of just letting users input whatever they want.
# If an ingredient name already exists, look at updating the recipeID column for that ingredient so we can see all recipes that use a particular ingredient if we wanted to.
# Do more testing on the Create Recipe route to make sure it's going to work with existing ingredients, etc.
# Upon recipe creation, the user should be forwarded to their new recipe page.
# Look into allowing user image uploads for their recipes.
# Implement edit recipe function.
# Implement new category function to allow users to create their own lists, possibly even making them public or private.
# Show some default categories on the page along with previews of a few recipes they contain.
# Consider thorough input validation if this project continues beyond this class, both with JS and backend.
# Figure out how to use the non-deprecated AutomapBase.prepare.reflect because apparently "Reflection is enabled when AutomapBase.prepare.autoload_with is passed."
# Review project requirements to make sure I'm still on track.


# Load sensitive data in .env file (db username and password in a separate file to be excluded from the repo)
dotenv.load_dotenv()
mysql_user = os.environ.get('USERNAME')
mysql_password = os.environ.get('MYSQL_PASSWORD')

# Create app instance
app = Flask(__name__)

# Set secret key for login session
app.secret_key = os.urandom(24)

# Specify mySQL connection
mysql_connection = f'mysql+pymysql://{mysql_user}:{mysql_password}@localhost/recipe_managementdb'

# Add db to app
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_connection

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define base class and automap reflected tables from db into SQLAlchemy objects.
with app.app_context():
    Base = automap_base()
    # engine = create_engine(mysql_connection)
    Base.prepare(db.engine, reflect=True)
    # Base.prepare(autoload_with=db.engine)
    Users = Base.classes.users
    Recipe = Base.classes.recipe
    Ingredient = Base.classes.ingredients
    RecipeIngredient = Base.classes.recipe_ingredients
    Category = Base.classes.category


# DEFINE ROUTES
# Default route to URL root
@app.route('/', methods=['GET', 'POST'])
def index():

    # Check if user is already logged in
    if 'user_id' in session:

        # Track user id in the session data.
        user_id = session['user_id']

        # Send them to the homepage.
        return render_template('index.html')
    else:
        # Render the homepage as well as any errors.

        # Check for error messages to display.
        error = session.pop('error', None)

        # Go to the homepage and send any errors to be displayed.
        return render_template('index.html', error=error)


# Test route to print all table names in the db
@app.route('/print_tables')
def print_tables():

    # Get table names and return a string.
    tables = Base.classes.keys()
    return ', '.join(tables)


# Test route to print db schema/structure
@app.route('/print_db_info')
def print_db_info():

    # Define a list to collect db info.
    info = []

    # Iterate over automapped db tables
    for name, table in Base.classes.items():
        info.append(f'Table: {name}')

        # Print columns
        columns = [f'   Column: {column.key} ({column.type})' for column in table.__table__.columns]
        info.extend(columns)

        # Print relationships
        relationships = [f'    Relationship: {rel.key} ({rel.mapper.class_.__name__})' for rel in table.__mapper__.relationships]
        info.extend(relationships)

        # Empty string as a separator.
        info.append('')

    # Return as HTML with br element between entries
    return '<br>'.join(info)

# Test route to print the entire db's records.
@app.route('/print_all_records')
def print_all_records():

    # Initialize a dictionary
    all_records = {}

    # Iterate over tables and convert entries into a dictionary within the app's context
    with app.app_context():
        for table_name, table_class in Base.classes.items():

            # Gets records from the current table.
            records = db.session.query(table_class).all()

            # Convert each record to a dictionary with some sweet list comprehension.
            record_dicts = [record.__dict__ for record in records]

            # Exclude internal SQLAlchemy attributes
            cleaned_records = [{key: value for key, value in record_dict.items() if not key.startswith('_')} for record_dict in record_dicts]

            # Stores cleaned records in a dictionary wth the table name as a key.
            all_records[table_name] = cleaned_records
    return jsonify(all_records)

# Define a login route.
@app.route('/login', methods=['GET', 'POST'])
def login():

    # If the user is already logged in, forward them to the homepage with an error message
    if 'user_id' in session:
        error = 'You are already logged in!'
        session['error'] = error
        return redirect(url_for('index'))
    
    # Default error message
    error = None
    
    if request.method == 'POST':

        #Get the email and password from the form.
        email = request.form.get('email')
        password = request.form.get('password')

        # If the email or password are empty, return an error.
        if not email or not password:
            error = 'Email and password are required'

        else:
            # Query the database for the user and return a response
            user = db.session.query(Users).filter_by(Email=email, Password=password).first()

            # If successful login, redirect to the home page or some other page
            if user:
                session['user_id'] = user.UserID
                session['login_success'] = True
                session['user_first_name'] = user.FirstName
                # Clear any errors
                session.pop('error', None)
                return redirect(url_for('index'))
            else:
                # Invalid credentials, render login page with error message
                error = 'Invalid email or password'

        # return render_template('login.html', error=error)
    
        #Store the error message in the session
        session['error'] = error

    #Render login page for GET requests
    return render_template('login.html', error=error)


@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':     
        # Clear session to log out the user and send to the homepage.
        session.clear()
        return redirect(url_for('index'))
    else:
        # Handle other methods with an error, because we only want to log out with a POST.
        return 'Method Not Allowed', 405


@app.route('/register_user', methods=['POST'])
def register_user():

    # Retrieve data from the register user form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    verify_password = request.form.get('verify_password')

    # Check if the email is already registered
    existing_user = db.session.query(Users).filter_by(Email=email).first()

    # If the email address already exists, return with an error and autofill info to prepopulate some fields.
    if existing_user:
        error = 'Email is already registered'
        return render_template('login.html', error=error, first_name=first_name, last_name=last_name, email=email)

    # Check if the passwords match
    # This should probably be done in Javascript first to reduce use of
    # server resources, but I'm feeling lazy.
    if password != verify_password:
        error = 'Passwords do not match'
        return render_template('login.html', error=error, first_name=first_name, last_name=last_name, email=email)

    
    # Create a new user
    new_user = Users(FirstName=first_name, LastName=last_name, Email=email, Password=password)
    db.session.add(new_user)
    db.session.commit()

    # Log in the new user
    session['user_id'] = new_user.UserID
    session['login_success'] = True
    session['user_first_name'] = new_user.FirstName

    # Clear any errors
    session.pop('error', None)

    # Redirect to the homepage
    return redirect(url_for('index'))


@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():

    # If the user is not logged in and tries to visit this page, send them to the login form.
    if 'user_id' not in session:

        # Redirect to login page if user is not logged in
        return redirect(url_for('login'))

    if request.method == 'POST':

        # Retrieve form data for the recipe to be created.
        name = request.form['name']
        description = request.form['description']
        instructions = request.form['instructions']
        category_id = request.form['category_id']
        user_id = session['user_id']

        # Create a new recipe object
        new_recipe = Recipe(Name=name, Description=description, Instructions=instructions, 
                            CategoryID=category_id, UserID=user_id, CreatedAt=datetime.now())

        # Add recipe to database
        db.session.add(new_recipe)
        db.session.commit()

        # Retrieve form data for ingredients, quantities, and units, zipping them all together in chunks
        ingredients = request.form.getlist('ingredient')
        quantities = request.form.getlist('quantity')
        units = request.form.getlist('unit')

        # Create Ingredient and RecipeIngredient objects
        # It's structured this way because of the relationship between Ingredients and Recipe_Ingredients, and
        # also because these three fields are one unit on the Create Recipe page.
        # Create tuples from each set of these fields.
        for ingredient_name, quantity, unit in zip(ingredients, quantities, units):

            # Check if the ingredient already exists
            existing_ingredient = db.session.query(Ingredient).filter_by(Name=ingredient_name).first()

            # If the ingredient does exist, get its id.
            if existing_ingredient:
                ingredient_id = existing_ingredient.IngredientID
            else:
                # Create a new ingredient entry if it doesn't exist
                new_ingredient = Ingredient(Name=ingredient_name, RecipeID=new_recipe.RecipeID)
                db.session.add(new_ingredient)
                db.session.commit()

                # Store the ingredient id for use in the recipe_ingredient table
                ingredient_id = new_ingredient.IngredientID

            # Create a new recipe_ingredient entry
            new_recipe_ingredient = RecipeIngredient(RecipeID=new_recipe.RecipeID, IngredientID=ingredient_id,
                                                    Units=unit, Quantity=quantity, CreatedAt=datetime.now())
            db.session.add(new_recipe_ingredient)
            db.session.commit()

        # Redirect to recipe detail page ideally. (Homepage for now.)
        return redirect(url_for('index', recipe_id=new_recipe.RecipeID))

    else:
        # Render the create recipe form
        categories = db.session.query(Category).all()  # Get all categories for dropdown
        return render_template('create_recipe.html', categories=categories)


if __name__ == "__main__":
    app.run(debug=True)

