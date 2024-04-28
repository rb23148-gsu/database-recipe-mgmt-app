from flask import Flask, request, redirect, render_template, url_for, session, jsonify, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func
from datetime import datetime
import os
import dotenv
from werkzeug.utils import secure_filename


# TODO: Add blueprints/possibly change file structure to categorize scripts by type/function depending on project size
# Set limit on the number of ingredients a user can put in a recipe (idk, 30?).
# Consider instructions to be inserted in a number of steps like ingredients to give it structure and automatically number them. 
#   (might skip for now until more functionality is added towards project completion.)
# Consider standardizing metric/imperial units instead of just letting users input whatever they want.
# Implement category functionality to generate categories by ingredient, e.g., chicken, beef, etc.
# Do more testing on the Create Recipe route to make sure it's going to work with existing ingredients, etc.
# Upon recipe creation, the user should be forwarded to their new recipe page.
# Look into allowing user image uploads for their recipes.
# Implement edit recipe function.
# Implement new category function to allow users to create their own lists, possibly even making them public or private.
# Show some default categories on the page along with previews of a few recipes they contain.
# Consider thorough input validation if this project continues beyond this class, both with JS and backend.
# Figure out how to use the non-deprecated AutomapBase.prepare.reflect because apparently "Reflection is enabled when AutomapBase.prepare.autoload_with is passed."
# Review project requirements to make sure I'm still on track.
# Tracking moved from here to Github issues for the project.


# Load sensitive data in .env file (db username and password in a separate file to be excluded from the repo)
dotenv.load_dotenv()
mysql_user = os.environ.get('USERNAME')
mysql_password = os.environ.get('MYSQL_PASSWORD')

# Create app instance
app = Flask(__name__)

# Set secret key for login session (cryptographically signed, not encrypted.)
app.secret_key = os.urandom(24)

# Specify mySQL connection
mysql_connection = f'mysql+pymysql://{mysql_user}:{mysql_password}@localhost/recipe_managementdb'

# Add db to app
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_connection

# Set image upload folder to a local folder since this is a small app.
UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define allowed image extensions.
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'ico'}

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

    # Query all recipes to show to the user on the front page.
    recipes = db.session.query(Recipe).all()

    # Check if user is already logged in
    if 'user_id' in session:

        # Track user id in the session data.
        user_id = session['user_id']

        # Send them to the homepage.
        return render_template('index.html', recipes=recipes)
    # Render the homepage as well as any errors
    else:

        # Check for error messages to display.
        error = session.pop('error', None)

        # Go to the homepage and send any errors to be displayed.
        return render_template('index.html', recipes=recipes, error=error)
    

# Get Allergens and Dislikes if not None.
def get_user_attributes():

    # Retrieve user ID from the session
    user_id = session.get('user_id')

    if user_id:
        
        # Fetch user attributes based on user ID
        user_attributes = db.session.query(Users).filter_by(UserID=user_id).first()

        # Get allergens and dislikes if not None. Split them into strings for later use to be compared to recipe ingredients.
        if user_attributes:
            allergens = user_attributes.Allergens.split(",") if user_attributes.Allergens is not None else []
            dislikes = user_attributes.Dislikes.split(",") if user_attributes.Dislikes is not None else []
            return allergens, dislikes
    
    # Return empty lists because returning None causes errors to throw.
    return [], []

# Compare allergens and dislikes to recipe ingredients in order to generate warnings on the page.
def check_user_preferences(recipe):

    # Retrieve user attributes for allergens and dislikes
    allergens, dislikes = get_user_attributes()

    # Define allergen and dislike warning list.
    allergen_warning = []
    dislike_warning = []

    # Check allergens and dislikes if they are present in the user's profile.
    if allergens and dislikes:

        # Get ingredients from the recipe and iterate over them, splitting them, and comparing them with the user's preferences.
        ingredients = db.session.query(RecipeIngredient.Quantity, RecipeIngredient.Units, Ingredient).join(RecipeIngredient).filter_by(RecipeID=recipe.RecipeID).all()
        for quantity, units, ingredient in ingredients:
            ingredient_name = ingredient.Name.split()  
            for keyword in ingredient_name:
                keyword = keyword.strip().lower()

                # If present, log a warning message to be sent to appear on the page.
                for allergen in allergens:
                    if allergen.strip().lower() == keyword:
                        matching_allergen = allergen
                        allergen_warning.append("This recipe contains ingredients you are allergic to: " + matching_allergen)
                        break

                for dislike in dislikes:
                    if dislike.strip().lower() == keyword:
                        matching_dislike = dislike
                        dislike_warning.append("This recipe contains ingredients you dislike: " + matching_dislike)
                        break
                    
    return allergen_warning, dislike_warning


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
        session['error_origin'] = 'login'
        return redirect(url_for('index'))
    
    elif 'error' in session:

        # Display any errors if available.
        error = session.pop('error', None)
        return render_template('login.html', error=error)

    # Default error message to none.
    error = None
    session.pop('error', None)
    session.pop('error_origin', None)
    
    if request.method == 'POST':

        #Get the email and password from the form.
        email = request.form.get('email')
        password = request.form.get('password')

        # If the email or password are empty, return an error.
        if not email.strip() or not password.strip():
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
                session.pop('error_origin', None)
                return redirect(url_for('index'))
            else:
                # Invalid credentials, render login page with error message
                error = 'Invalid email or password'
    
        #Store the error message in the session
        session['error'] = error
        session['error_origin'] = 'login'

    #Render login page for GET requests
    return render_template('login.html', error=error, error_origin='login')


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

    #Clear any existing errors.
    session.pop('error', None)
    session.pop('error_origin', None)
    error=None

    # Retrieve data from the register user form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    verify_password = request.form.get('verify_password')

    # Input validation:
    # Check if the email is already registered
    existing_user = db.session.query(Users).filter_by(Email=email).first()

    # If the email address already exists, return with an error and autofill info to prepopulate some fields.
    if existing_user:
        error = 'Email is already registered'
        return render_template('login.html', error=error, first_name=first_name, last_name=last_name, email=email, error_origin='register')

    # Check if the passwords match
    # This should probably be done in Javascript first to reduce use of
    # server resources, but I'm feeling lazy.
    if password != verify_password:
        error = 'Passwords do not match'
        return render_template('login.html', error=error, first_name=first_name, last_name=last_name, email=email, error_origin='register')

    
    # If all input validation is successful:
    # Create a new user
    new_user = Users(FirstName=first_name, LastName=last_name, Email=email, Password=password)
    db.session.add(new_user)
    db.session.commit()

    # Log in the new user
    session['user_id'] = new_user.UserID
    session['login_success'] = True
    session['user_first_name'] = new_user.FirstName

    # Clear any errors. (should probably use flash() instead)
    session.pop('error', None)

    # Redirect to the homepage
    return redirect(url_for('index'))


# Only allow certain file extensions for uploads when adding images to recipes.
def allowed_file(filename):

    # Check the filename's extension
    if '.' in filename:

        # Split the filename at the last dot using a right split, once from the right.
        # Access the second element, [1], which would be the file extension and convert to 
        # lowercase for comparison.
        extension = filename.rsplit('.', 1)[1].lower()

        # Check if the extension is in the set of allowed extensions
        if extension in ALLOWED_EXTENSIONS:
            return True
        
    return False


# Define a route to serve static image files
@app.route('/images/<filename>')
def images(filename):
    return send_from_directory('images', filename)


# Route to create recipes.
@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():

    #Clear any existing errors.
    session.pop('error', None)
    error=None

    # If the user is not logged in and tries to visit this page, send them to the login form.
    if 'user_id' not in session:

        error='You must be logged in to create a recipe!'
        session['error'] = error
        # Redirect to login page if user is not logged in
        return redirect(url_for('login'))

    if request.method == 'POST':

        # Retrieve form data for the recipe to be created.
        name = request.form['name']
        description = request.form['description']
        instructions = request.form['instructions']
        category_id = request.form['category_id']
        user_id = session['user_id']

        # Retrieve form data for ingredients, quantities, and units, zipping them all together in chunks
        ingredients = request.form.getlist('ingredient')
        quantities = request.form.getlist('quantity')
        units = request.form.getlist('unit')

        # Check if data fields are blank
        if not name.strip():
            error = 'Recipe must have a name.'

        elif not description.strip():
            error = 'Recipe must have a description.'
        
        elif not instructions.strip():
            error = 'Recipe must have instructions.'

        elif not category_id.strip():
            error = 'Recipe must be assigned a category.'
        
        elif not ingredients:
            error = 'Recipe must have at least one ingredient.'

        # Remove commas from entered quantities because they're throwing errors on recipe creation.
        cleaned_quantities = [quantity.replace(',', '') for quantity in quantities]

        # If there's any error, display it and render the form again using flash
        # Flash() displays a message to the user without needing to persist across requests.
        if error:

            # Flash error to user.
            flash(error, 'error')

            # Get categories for the new page render.
            categories = db.session.query(Category).all()
            return render_template('create_recipe.html', categories=categories)

        # Initialize image_url as None
        image_url = None

        # Check if an image file was uploaded
        if 'image' in request.files:

            file = request.files['image']

            # Check if the file is not empty and also allowed.
            if file.filename != '' and allowed_file(file.filename):

                # Sanitize filename before storing or using it.
                filename = secure_filename(file.filename)

                # Set filepath to our designated folder.
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Construct the image URL
                image_url = f"/images/{filename}"

                #Save the filepath
                file.save(filepath)

                flash('Image uploaded successfully')
            else:

                # Set filepath to None if image upload failed
                flash('Invalid file format for image upload', 'error')
                filepath = None  

        # Set filepath to None if no image was uploaded
        else:
            filepath = None  

        # If validation checks out:
        # Create a new recipe object
        new_recipe = Recipe(Name=name, Description=description, Instructions=instructions, 
                            CategoryID=category_id, UserID=user_id, CreatedAt=datetime.now(), ImageURL=image_url)


        # Add recipe to database
        db.session.add(new_recipe)
        db.session.commit()

        # Create Ingredient and RecipeIngredient objects
        # It's structured this way because of the relationship between Ingredients and Recipe_Ingredients, and
        # also because these three fields are one unit on the Create Recipe page.
        # Create tuples from each set of these fields.
        for ingredient_name, quantity, unit in zip(ingredients, cleaned_quantities, units):

            # Check if the ingredient already exists
            existing_ingredient = db.session.query(Ingredient).filter_by(Name=ingredient_name).first()

             # If the ingredient does not exist, create a new ingredient entry
            if not existing_ingredient:
                new_ingredient = Ingredient(Name=ingredient_name)
                db.session.add(new_ingredient)
                db.session.commit()
                existing_ingredient = new_ingredient

            # Create a new recipe_ingredient entry
            new_recipe_ingredient = RecipeIngredient(RecipeID=new_recipe.RecipeID, IngredientID=existing_ingredient.IngredientID,
                                                    Units=unit, Quantity=quantity, CreatedAt=datetime.now())
            db.session.add(new_recipe_ingredient)
            db.session.commit()

        # Redirect to view recipe page
        return redirect(url_for('view_recipe', recipe_id=new_recipe.RecipeID))

    else:
        # Render the create recipe form with categories for dropdown.
        categories = db.session.query(Category).all()  
        return render_template('create_recipe.html', categories=categories)


# View a recipe by its id.
@app.route('/view_recipe/<int:recipe_id>')
def view_recipe(recipe_id):

    # Query the database for the recipe by its id, creating a recipe object.
    recipe = db.session.query(Recipe).filter_by(RecipeID=recipe_id).first()

    # Check user preferences for this recipe to see what warnings to generate, and with what ingredients
    allergen_warnings, dislike_warnings = check_user_preferences(recipe)

    # If the recipe does exist, get the recipe information
    if recipe:

        # Query the Users table with the recipe's userID to get the author.
        user = db.session.query(Users).filter_by(UserID=recipe.UserID).first()

        # Grab first name and last initial so we can display it on the page.
        user_first_name = user.FirstName
        user_last_name = user.LastName
        user_last_initial = user_last_name[0] + '.'

        # Get a list of sorted valid recipe IDs for navigation purposes using list comprehension.
        valid_recipe_ids = sorted([result.RecipeID for result in db.session.query(Recipe).all()])

        # Take note of how many recipes we have.
        num_recipes = len(valid_recipe_ids)

        # Find this recipe's current position in the list of recipes.
        current_recipe_index = valid_recipe_ids.index(recipe_id)

        # Assign values to send to the Prev and Next Recipe buttons so that the user can endlessly
        # scroll by having the recipes wrap around either way with a modulo operator.
        prev_recipe_id = valid_recipe_ids[(current_recipe_index - 1) % num_recipes]
        next_recipe_id = valid_recipe_ids[(current_recipe_index + 1) % num_recipes]

    # otherwise, return a 404 error.
    else:

        # Show an error if the page is not a valid recipe id.
        error='Recipe not found'
        # flash(error, 'error')
        return render_template('error.html', error=error), 404
    
    # Get the list of ingredients, quantity, and units for the recipe  by joining the Recipe_Ingredient table to the Ingredients table based on the given recipeID.
    ingredients = db.session.query(RecipeIngredient.Quantity, RecipeIngredient.Units, Ingredient).join(RecipeIngredient).filter_by(RecipeID=recipe_id).all()
    
    # Return the view_recipe.html view with recipe, ingredient, user data, and prev/next Recipe ids for an endless recipe loop.
    return render_template('view_recipe.html', recipe=recipe, ingredients=ingredients, 
                           user_first_name=user_first_name, user_last_initial=user_last_initial, 
                           prev_recipe_id=prev_recipe_id, next_recipe_id=next_recipe_id, allergen_warnings=allergen_warnings, dislike_warnings=dislike_warnings)



# Route to edit recipe by its id.
@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):

    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get the recipe from the database
    recipe = db.session.query(Recipe).filter_by(RecipeID=recipe_id).first()

    # Check if the recipe exists
    if not recipe:
        flash("That recipe was not found!", 'error')
        return redirect(url_for('home'))

    # Check if the logged in user is the owner of the recipe
    if recipe.UserID != session['user_id']:
        flash("You are not authorized to edit this recipe.", 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        description = request.form['description']
        instructions = request.form['instructions']
        category_id = request.form['category_id']
        
        # Update recipe details
        recipe.Name = name
        recipe.Description = description
        recipe.Instructions = instructions
        recipe.CategoryID = category_id

        # Retrieve form data for ingredients, quantities, and units.
        ingredients = request.form.getlist('ingredient')
        quantities = request.form.getlist('quantity')
        units = request.form.getlist('unit')

        # Remove commas from entered quantities because they're throwing errors on recipe creation.
        cleaned_quantities = [quantity.replace(',', '') for quantity in quantities]

        # Create Ingredient and RecipeIngredient objects
        # It's structured this way because of the relationship between Ingredients and Recipe_Ingredients, and
        # also because these three fields are one unit on the Create Recipe page.
        # Create tuples from each set of these fields.
        for ingredient_name, quantity, unit in zip(ingredients, cleaned_quantities, units):

            # Check if the ingredient already exists
            existing_ingredient = db.session.query(Ingredient).filter_by(Name=ingredient_name).first()

             # If the ingredient does not exist, create a new ingredient entry
            if not existing_ingredient:
                new_ingredient = Ingredient(Name=ingredient_name)
                db.session.add(new_ingredient)
                db.session.commit()
                # existing_ingredient = new_ingredient

            # Create a new recipe_ingredient entry
            new_recipe_ingredient = RecipeIngredient(RecipeID=recipe.RecipeID, IngredientID=existing_ingredient.IngredientID,
                                                    Units=unit, Quantity=quantity, CreatedAt=datetime.now())
            db.session.add(new_recipe_ingredient)
            db.session.commit()


        # Commit changes
        db.session.commit()

        flash('Recipe updated successfully.', 'success')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))

    # If it's a GET request, render the edit_recipe template
    categories = db.session.query(Category).all() 
    ingredients = db.session.query(RecipeIngredient.Quantity, RecipeIngredient.Units, Ingredient).join(RecipeIngredient).filter_by(RecipeID=recipe_id).all()
    return render_template('edit_recipe.html', recipe=recipe, categories=categories, ingredients=ingredients)


# Route to delete a recipe by its id.
@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):

    # Check if the user is logged in
    if 'user_id' not in session:

        # If not, go to login screen
        return redirect(url_for('login'))

    # Get the recipe from the database by recipe id
    recipe = db.session.query(Recipe).filter_by(RecipeID=recipe_id).first()

    # Check if the recipe exists
    if not recipe:
        flash("Recipe not found!", 'error')
        return redirect(url_for('index'))

    # Check if the logged in user is the owner of the recipe
    if recipe.UserID != session['user_id']:
        flash("You are not authorized to delete this recipe.", 'error')
        return redirect(url_for('index'))

    # Delete the recipe and associated recipe_ingredients entries
    db.session.query(RecipeIngredient).filter_by(RecipeID=recipe_id).delete()
    db.session.delete(recipe)
    db.session.commit()

    flash('Recipe deleted successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings():

    # Check if the user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to access user settings.', 'error')
        return redirect(url_for('login'))

    # Retrieve user data based on their current logged in user id
    user_id = session['user_id']
    user = db.session.query(Users).filter_by(UserID=user_id).first()
    user_recipes = db.session.query(Recipe).filter_by(UserID=user_id).all()

    # Use SQLAlchemy's func.count to count the number of recipes for the given user ID
    recipe_count = db.session.query(func.count(Recipe.RecipeID)).filter_by(UserID=user_id).scalar()

    if request.method == 'POST':

        # Check if the form is for changing the password
        if 'old_password' in request.form:
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            # Verify the old password
            if user.Password != old_password:
                flash('Incorrect old password. Please try again.', 'error')
                return redirect(url_for('user_settings'))

            # Check if the new password matches the confirm password
            if new_password != confirm_password:
                flash('New password and confirm password do not match.', 'error')
                return redirect(url_for('user_settings'))

            # Update the user's password
            user.Password = new_password
            db.session.commit()
            flash('Password updated successfully.', 'success')
            return redirect(url_for('user_settings'))

        # Check if the form is for updating allergens and dislikes
        elif 'allergens' in request.form and 'dislikes' in request.form:
            allergens = request.form['allergens']
            dislikes = request.form['dislikes']

            # Update the user's allergens and dislikes
            user.Allergens = allergens
            user.Dislikes = dislikes
            db.session.commit()
            flash('Allergens and dislikes updated successfully.', 'success')
            return redirect(url_for('user_settings'))

    # Render the user settings page with user data
    return render_template('user_settings.html', user=user, recipe_count=recipe_count, user_recipes=user_recipes)


if __name__ == "__main__":
    app.run(debug=True)

