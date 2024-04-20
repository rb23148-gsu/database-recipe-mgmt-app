CREATE DATABASE Recipe_managementdb;
USE Recipe_managementdb;

CREATE TABLE Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Category (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    UserID INT,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Recipe (
    RecipeID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    Instructions TEXT NOT NULL,
    Type VARCHAR(255),
    CategoryID INT,
    UserID INT,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Ingredients (
    IngredientID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Quantity DECIMAL(10,2) NOT NULL,
    Unit VARCHAR(50),
    RecipeID INT,
    FOREIGN KEY (RecipeID) REFERENCES Recipe(RecipeID)
);

CREATE TABLE Recipe_Ingredients (
    RecipeID INT NOT NULL AUTO_INCREMENT,
    IngredientID INT NOT NULL,
    Units VARCHAR(255),
    Quantity DECIMAL(10,2) NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (RecipeID, IngredientID),
    FOREIGN KEY (RecipeID) REFERENCES Recipe(RecipeID),
    FOREIGN KEY (IngredientID) REFERENCES Ingredients(IngredientID)
);

INSERT INTO Users (FirstName, LastName, Email, Password)
VALUES ('John', 'Doe', 'test@test.com', 'password');

-- Quantity is already tied to Recipe_Ingredients table, so this is probably redundant.
ALTER TABLE ingredients DROP COLUMN Quantity;

-- 'Type' is too generic, or I just forgot what we were going to use it for. Seems like a duplicate of Category. Either way, it's gone for now.
ALTER TABLE recipe DROP COLUMN Type;

-- Removed Units from Ingredients Table since it already exists in Recipe_Ingredients.
ALTER TABLE ingredients DROP COLUMN Unit;

INSERT INTO Category (Name)
VALUES ('Breakfast');

INSERT INTO Category (Name)
VALUES ('Lunch');

INSERT INTO Category (Name)
VALUES ('Dinner');

DELETE FROM recipe;
DELETE FROM ingredients;
DELETE FROM recipe_ingredients;

SELECT * from recipe;