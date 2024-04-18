from flask import Flask, request, redirect, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from datetime import datetime
import os
import dotenv


# TODO: Add blueprints/possibly change file structure to categorize scripts by type/function depending on project size
# Add user registration page to add new users.
# Add date/time values for some fields.
# Make some fields such as email unique so they can't be duplicated, e.g., email.
# Double check project requirements to make sure I'm on track.

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
        # Clear session to log out the user
        session.clear()
        return redirect(url_for('index'))
    else:
        # Handle other methods with an error, because we only want to log out with a POST.
        return 'Method Not Allowed', 405

if __name__ == "__main__":
    app.run(debug=True)

