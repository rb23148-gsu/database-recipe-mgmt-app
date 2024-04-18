# database-recipe-mgmt-app
 Database Systems Recipe Management App

<<<<<<< Updated upstream
How to set up DB locally.
=======
 This project primarily utilizes HTML and CSS, possibly Bootstrap for the frontend, and Flask for the backend with the SQLAlchemy toolkit and a MySQL database.

How to set up the MySQL DB locally.
>>>>>>> Stashed changes

1. Open up MySQL Workbench.
2. Create a new connection, test it, make sure your password works, and give the connection a relevant name.
3. Take note of your user and password, most likely 'root' and whatever password you decided on. You'll need it later.
4. You should be at a blank screen with a tab called something like 'Query1'.
5. Paste the data from the .sql file in the project root folder into the blank 'Query1' file inside MySQL Workbench. Make sure no text is selected and click the lightning bolt to run the commands to initialize the database.
    (Note as of 4/17: Data is not yet added beyond a single user. More will be added as the project develops.)
6. In the project root directory, create a file called .env, and add the line 'MYSQL_PASSWORD=yourPassword' without quotes. On the next line, add 'USERNAME=yourUsername' without quotes. Replace yourPassword and yourUsername with your information to log in to your database. Save it.
7. In the project root directory, create a file called '.gitignore', no quotes. On the first line, put '.env' without quotes, then save and exit. This prevents your password from being hardcoded into the program, and also from being uploaded to Github.


How to set up the app locally:

1. Install Python: https://www.python.org/downloads/
2. Clone the repo locally from Github using Github Desktop or CLI.
3. Go to the github project directory and open cmd.
4. If on Windows, run '.venv\Scripts\activate' without quotes to start the virtual environment. You should see some visual change in your terminal/command line to reflect that you're operating in a virtual environment.
    4.1. If on macOS/Linux, run '.venv/bin/activate' (?? Idk if this will work since my primary machine is Windows. lmk)
5. Run 'pip install -r requirements.txt' without quotes to install dependencies locally (until I write a script to do a bunch of this automatically.)
6. You should be able to now run 'python app.py' from the root directory of the project, which should start an app at http://localhost:5000, accessible via your browser of choice.
7. ???
8. PROFIT!!!

