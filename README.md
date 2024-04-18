# database-recipe-mgmt-app
 Database Systems Recipe Management App

 This project primarily utilizes HTML and CSS, possibly Bootstrap for the frontend, and Flask for the backend with the SQLAlchemy toolkit and a MySQL database.

How to set up DB locally.

1. Open up MySQL Workbench.
2. Create a new connection, test it, make sure your password works, and give the connection a relevant name.
3. You should be at a blank screen with a tab called something like Query1.
4. Paste the data from the .sql file in the project root into the blank Query1 file, make sure nothing is selected, and click the lightning bolt to run the commands to initialize the database.
    (Note as of 4/17: Data is not yet added beyond a single user. More will be added as the project develops.)

How to set up the app locally:

1. Install Python: https://www.python.org/downloads/
2. Clone the repo locally from Github using Github Desktop or CLI.
3. Go to the github project directory and open cmd.
4. If on Windows, run '.venv\Scripts\activate' without quotes to start the virtual environment.
4.1 If on macOS/Linux, run '.venv/bin/activate' (?? Idk if this will work since my primary machine is Windows. lmk)
5. Run 'pip install -r requirements.txt' without quotes to install dependencies locally (until I write a script to do this automatically.)
6. You should be able to now run 'python app.py' from the root directory, which should start an app at http://localhost:5000, accessible via your browser of choice.
7. ???
8. PROFIT!!!

