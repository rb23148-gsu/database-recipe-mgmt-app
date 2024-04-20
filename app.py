from flask import Flask, request, redirect, render_template, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from datetime import datetime
import os
import dotenv


# TODO: Add blueprints/possibly change file structure to categorize scripts by type/function depending on project size
# Add a "Create Recipe" route to allow the user to create a new recipe.
# Double check relationships between tables to make sure this can happen correctly.

# Load sensitive data in .env file (db password in a separate file to be excluded from the repo)
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

# Define base class and automap reflected tables from db for SQLAlchemy models
with app.app_context():
    Base = automap_base()
    # engine = create_engine(mysql_connection)
    Base.prepare(db.engine, reflect=True)
    # Base.prepare(autoload_with=db.engine)
    Users = Base.classes.users


# DEFINE ROUTES
# Default route to URL root
@app.route('/', methods=['GET', 'POST'])
def index():

    # Check if user is already logged in
    if 'user_id' in session:
        user_id = session['user_id']

        # Query data related to the logged-in user
        # Example: user_data = db.session.query(UserData).filter_by(user_id=user_id).all()
        
        # return render_template('index.html', user_id=session['user_id'])
        return render_template('index.html')
    else:
        # Render the homepage with login form

        # Check for error messages to display.
        error = session.pop('error', None)

        return render_template('index.html', error=error)


# Test route to print all tables in the db
@app.route('/print_tables')
def print_tables():
    tables = Base.classes.keys()
    return ', '.join(tables)


# Test route to print db info
@app.route('/print_db_info')
def print_db_info():
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

        info.append('')

    # Return as HTML with br element between entries
    return '<br>'.join(info)

# Test route to print the entire db.
@app.route('/print_all_records')
def print_all_records():

    # Initialize a dictionary
    all_records = {}

    # Iterate over tables and convert entries into a dictionary with the app's resources
    with app.app_context():
        for table_name, table_class in Base.classes.items():

            # Gets records from the current table.
            records = db.session.query(table_class).all()

            # Convert each record to a dictionary
            record_dicts = [record.__dict__ for record in records]

            # Exclude internal SQLAlchemy attributes
            cleaned_records = [{key: value for key, value in record_dict.items() if not key.startswith('_')} for record_dict in record_dicts]

            # Stores cleaned records in a dictionary wth the table name as a key.
            all_records[table_name] = cleaned_records
    return jsonify(all_records)

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
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            # If the emails are empty or whitespace only, return an error.
            error = 'Email and password are required'

        else:
            # Query the database for the user and return a response
            user = db.session.query(Users).filter_by(Email=email, Password=password).first()

            if user:
                # Successful login, redirect to the home page or some other page
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

    # If it already exists, return with an error and autofill info to prepopulate some fields.
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

if __name__ == "__main__":
    app.run(debug=True)

