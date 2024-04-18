@echo off

rem Check if .env file exists
if not exist .env (
    rem Create .env file
    echo USERNAME=yourUsername > .env
    echo MYSQL_PASSWORD=yourPassword >> .env
    echo .env created.
) else (
    echo .env file already exists. Skipping creation.
)

rem Check if .gitignore file exists
if not exist .gitignore (
    rem Create .gitignore file
    echo .env > .gitignore
    echo .gitignore created.
) else (
    echo .gitignore file already exists. Skipping creation.
)

echo Setup complete.

echo Put your MySQL db username/password in 'yourUsername' and 'yourPassword'
