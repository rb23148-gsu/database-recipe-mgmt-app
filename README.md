# database-recipe-mgmt-app
 #Database Systems Recipe Management App

 This project primarily utilizes HTML and CSS, possibly Bootstrap for the frontend, and Flask for the backend with the SQLAlchemy toolkit and a MySQL database.
 

#First, how to set up the MySQL DB locally:

1. Open up MySQL Workbench 8.

2. Create a new connection, test it, make sure your password works, and give the connection a relevant name.

3. Take note of your user and password, most likely 'root' and whatever password you decided on. You'll need it later.

4. You should be at a blank file screen with a tab called something like 'Query1'.

5. Paste the data from the .sql file in the project root folder into the blank 'Query1' file inside MySQL Workbench. Make sure no text is selected and click the lightning bolt to run all the commands to initialize the database.
    (Note as of 4/17: Data is not yet added beyond a single user. More will be added as the project develops.)

6. To set up the files for steps 7 and 8 automatically on Windows, just double click or open in command prompt 'create_env_and_gitignore.bat' to create the files and prepopulate the fields. All you have to do is enter your username and password for your local database in 'yourUsername' and 'yourPassword' without quotes inside the .env file.

If you can't or don't want to use the .bat file:

7. In the project root directory, (if you didn't use the .bat file) create a file called '.env', no quotes, and add the line 'USERNAME=yourUsername' without quotes. On the next line, add 'MYSQL_PASSWORD=yourPassword' without quotes. Replace yourUsername and yourPassword with your information to log in to your database. Save it.

8. In the project root directory, (if you didn't use the .bat file) create a file called '.gitignore', no quotes. On the first line, put '.env' without quotes, then save and exit. This prevents your password from being hardcoded into the program, and also from being uploaded to Github, which isn't necessarily a huge issue for this project, but it's good practice.


#Next, how to set up the app locally:

1. Install Python and check the 'add to the system path variables' option during setup: https://www.python.org/downloads/

2. Clone this project repo locally from Github using Github Desktop or CLI.

3. If using Github desktop, make sure this project is selected, right click on the repository tab, and select 'Open in Command Prompt'.

4. Run the command 'py -3 -m venv .venv' or otherwise get .venv installed for Python to install Python Virtual Environment.

5. If on Windows, run '.venv\Scripts\activate' without quotes to start the virtual environment. A virtual environment lets you have different dependencies on a per-project basis instead of trying to use whatever you have installed on your system. It makes the project more portable since you'll usually have a list of dependencies to install, such as in requirements.txt, which you'll see in a couple of steps. When you activate your virtual environment successfully, you should see some visual change in your terminal/command line to reflect that you're operating in a virtual environment. For me, it's green text on my command line that says '(.venv)' at the start of the line. 

5.1. If on macOS/Linux, run '.venv/bin/activate' (?? Idk if this will work since my primary machine is Windows. lmk)

6. Run 'pip install -r requirements.txt' without quotes to install dependencies locally from the requirements file. 

7. You should be able to now run 'python app.py' from the root directory of the project, which should start an app at http://localhost:5000, accessible via your browser of choice.

8. ???

9. PROFIT!!!

