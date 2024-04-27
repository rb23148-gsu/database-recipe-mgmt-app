-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: recipe_managementdb
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `CategoryID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `UserID` int DEFAULT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`CategoryID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `category_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (9,'Breakfast',NULL,'2024-04-23 07:28:49'),(10,'Lunch',NULL,'2024-04-23 07:28:53'),(11,'Dinner',NULL,'2024-04-23 07:28:55');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredients` (
  `IngredientID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  PRIMARY KEY (`IngredientID`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredients`
--

LOCK TABLES `ingredients` WRITE;
/*!40000 ALTER TABLE `ingredients` DISABLE KEYS */;
INSERT INTO `ingredients` VALUES (83,'bacon'),(84,'onion'),(85,'red bell pepper'),(86,'garlic'),(87,'eggs'),(88,'milk'),(89,'frozen potatoes'),(90,'shredded cheddar'),(91,'salt'),(92,'black pepper'),(93,'green onions'),(94,'all purpose baking flour'),(95,'baking powder'),(96,'vegetable oil'),(97,'egg, beaten'),(98,'butter, melted'),(99,'packed brown sugar'),(100,'ground cinnamon'),(101,'butter'),(102,'cream cheese'),(103,'powdered sugar'),(104,'vanilla extract'),(105,'fish fillets'),(106,'unsalted butter'),(107,'heavy cream'),(108,'dijon mustard'),(109,'lemon juice'),(110,'shallots'),(111,'lemon'),(112,'fresh parsley'),(113,'hot dogs'),(114,'aaa'),(115,'egg'),(116,'ducks'),(117,'asdf'),(118,'black beans'),(119,'pinto beans'),(120,'garbanzo beans'),(121,'whale'),(122,'panko bread crumbs'),(123,'test'),(124,'smoked sausages'),(125,'buns'),(126,'spicy mustard');
/*!40000 ALTER TABLE `ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipe`
--

DROP TABLE IF EXISTS `recipe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipe` (
  `RecipeID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Description` text NOT NULL,
  `Instructions` text NOT NULL,
  `CategoryID` int DEFAULT NULL,
  `UserID` int DEFAULT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ImageURL` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`RecipeID`),
  KEY `CategoryID` (`CategoryID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `recipe_ibfk_1` FOREIGN KEY (`CategoryID`) REFERENCES `category` (`CategoryID`),
  CONSTRAINT `recipe_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipe`
--

LOCK TABLES `recipe` WRITE;
/*!40000 ALTER TABLE `recipe` DISABLE KEYS */;
INSERT INTO `recipe` VALUES (74,'Bacon Potato and Egg Casserole','This easy breakfast casserole is packed with bacon, potatoes, and cheese! It can be prepared ahead of time and is a real crowd pleaser!','Heat the oven to 350°F. Grease a 9×13 baking dish with nonstick cooking spray and set aside.\r\n\r\nIn a large skillet, cook bacon over medium heat, stirring occasionally. Cook until it is a nice crispy brown. Remove bacon with a slotted spoon and place on a paper towel lined plate. Roughly chop the bacon and set aside.\r\n\r\nAdd the onion and red pepper to the skillet and cook over medium heat until tender. Add the garlic and cook for 2 minutes. Set aside.\r\n\r\nIn a large bowl, beat the eggs and whisk in the milk. Stir in the cooked vegetables, potatoes, and 1 cup of the shredded cheese. Set ¾ cup of bacon aside and stir in the rest. Season with salt and pepper.\r\n\r\nPour the mixture into the prepared baking dish and top remaining cheese and green onions. Bake for 20 minutes so the eggs start to set up. Carefully add the remaining bacon to the top of the casserole. Bake for an additional 20 tot 30 minutes or until the eggs are firm and the top is slightly golden brown. Let stand for 10 minutes. Cut into squares and serve warm.\r\n\r\nNote: This casserole can be made in advance. Pour the mixture in the pan and refrigerate for up to 24 hours. Bake when ready to eat. You can also reheat the casserole.',9,1,'2024-04-23 08:48:13','/images/2024-04-23_08_44_59-Bacon_Potato_and_Egg_Casserole.png'),(75,'Cinnamon Roll Pancakes','Swirls of cinnamon and sugar fill these delicious Cinnamon Roll Pancakes. Top them with a cream cheese glaze for the ultimate breakfast treat!','Prepare Cinnamon Filling first:\r\nIn a medium bowl, mix butter, brown sugar and cinnamon. Scoop the filling into a small zip baggie and set aside. (Set this aside and let it rest for 10 to 15 minutes. You want it just slightly thick.)\r\n\r\nPrepare Pancake batter: In a medium bowl whisk together flour, baking powder and salt. Whisk in milk, oil and egg just until batter is moistened. (a few small lumps are fine)\r\n\r\nOR If using a boxed mix, prepare according to package directions.\r\n\r\nPrepare Cream Cheese glaze: In a medium glass or microwave-safe bowl, heat the butter and cream cheese until melted. Whisk together until smooth, then whisk in powdered sugar and vanilla. Set aside.\r\n\r\nHeat a large skillet or griddle over low heat. Spray with non-stick cooking spray. Pour about 1/2 cup of pancake batter onto the skillet.\r\n\r\nSnip the corner of your cinnamon filling baggie and squeeze a spiral of the filling onto the top of the pancake.\r\n\r\nWhen bubbles begin to appear on the surface, flip carefully with a spatula and cook until lightly browned on the underside, 1 to 2 minutes more. Transfer pancake to a baking sheet and keep warm in the oven while you make the rest of the pancakes.\r\n\r\nWhen ready to serve, spoon warmed cream cheese glaze on top of each pancake. Enjoy!',9,1,'2024-04-23 08:52:37','/images/2024-04-23_08_48_53-Cinnamon_Roll_Pancakes.png'),(76,'Baked Fish with Lemon Cream Sauce','A fantastic quick-fix dinner – baked fish in a lemon cream sauce, all made in ONE PAN!','Preheat oven to 200°C / 390°F (all oven types).\r\n\r\nPlace fish in a baking dish – ensure the fish isn’t crammed in too snugly. See video or photos in post. Sprinkle both sides of fish with salt and pepper.\r\n\r\nPlace butter, cream, garlic, mustard, lemon juice, salt and pepper in a microwave proof jug or bowl. Microwave in 2 x 30 sec bursts, stirring in between, until melted and smooth.\r\n\r\nSprinkle fish with shallots, then pour over sauce.\r\n\r\nBake for 10 – 12 minutes, or until fish is just cooked. Remove from oven and transfer fish to serving plates. Spoon over sauce, and garnish with parsley and lemon wedges if using.',11,2,'2024-04-23 08:56:58','/images/2024-04-23_08_54_07-Baked_Fish_with_Lemon_Cream_Sauce___RecipeTin_Eats.png'),(77,'Hot Dogs','Literally just a glizzy','Heat \'em and eat \'em. Or don\'t. I\'m not your dad.',10,1,'2024-04-23 10:20:30','/images/download.jpeg'),(83,'Beans','loads of beans','it\'s beans.',9,1,'2024-04-26 00:23:44','/images/beans.jpg'),(84,'Whale Nuggets','Just like memaw used to make.','1. Get a whale.\r\n2. Debone it.\r\n3. Make nuggets.',9,1,'2024-04-26 03:28:38','/images/66024759_l.jpg'),(86,'Smoked Sausages','Best enjoyed at your desk.','Top \'em to your heart\'s content and enjoy!',10,4,'2024-04-27 19:02:50','/images/smokedsausagedogs.jpg');
/*!40000 ALTER TABLE `recipe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipe_ingredients`
--

DROP TABLE IF EXISTS `recipe_ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipe_ingredients` (
  `RecipeIngredientID` int NOT NULL AUTO_INCREMENT,
  `RecipeID` int NOT NULL,
  `IngredientID` int NOT NULL,
  `Units` varchar(255) DEFAULT NULL,
  `Quantity` decimal(10,2) NOT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`RecipeIngredientID`),
  KEY `RecipeID` (`RecipeID`),
  KEY `IngredientID` (`IngredientID`),
  CONSTRAINT `recipe_ingredients_ibfk_1` FOREIGN KEY (`RecipeID`) REFERENCES `recipe` (`RecipeID`),
  CONSTRAINT `recipe_ingredients_ibfk_2` FOREIGN KEY (`IngredientID`) REFERENCES `ingredients` (`IngredientID`)
) ENGINE=InnoDB AUTO_INCREMENT=149 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipe_ingredients`
--

LOCK TABLES `recipe_ingredients` WRITE;
/*!40000 ALTER TABLE `recipe_ingredients` DISABLE KEYS */;
INSERT INTO `recipe_ingredients` VALUES (98,74,83,'lb',1.00,'2024-04-23 08:48:13'),(99,74,84,'diced',1.00,'2024-04-23 08:48:13'),(100,74,85,'diced',1.00,'2024-04-23 08:48:13'),(101,74,86,'cloves',3.00,'2024-04-23 08:48:13'),(102,74,87,'large',12.00,'2024-04-23 08:48:13'),(103,74,88,'cup',1.00,'2024-04-23 08:48:13'),(104,74,89,'cups diced',3.00,'2024-04-23 08:48:13'),(105,74,90,'cups',2.00,'2024-04-23 08:48:13'),(106,74,91,'tsp',1.50,'2024-04-23 08:48:13'),(107,74,92,'tsp',0.50,'2024-04-23 08:48:13'),(108,74,93,'chopped',2.00,'2024-04-23 08:48:13'),(109,75,94,'cups',1.25,'2024-04-23 08:52:37'),(110,75,95,'tsp',2.00,'2024-04-23 08:52:37'),(111,75,88,'cup',1.00,'2024-04-23 08:52:37'),(112,75,96,'tbsp',1.00,'2024-04-23 08:52:37'),(113,75,97,'large',1.00,'2024-04-23 08:52:37'),(114,75,98,'cups',0.33,'2024-04-23 08:52:37'),(115,75,99,'cup',0.75,'2024-04-23 08:52:37'),(116,75,100,'tbsp',1.00,'2024-04-23 08:52:37'),(117,75,101,'tbsp',4.00,'2024-04-23 08:52:37'),(118,75,102,'oz',2.00,'2024-04-23 08:52:37'),(119,75,103,'cups',1.25,'2024-04-23 08:52:37'),(120,75,104,'tsp',1.00,'2024-04-23 08:52:37'),(121,76,105,'5-6oz',4.00,'2024-04-23 08:56:58'),(122,76,106,'tbsp',4.00,'2024-04-23 08:56:58'),(123,76,107,'cup',0.25,'2024-04-23 08:56:58'),(124,76,86,'cloves',2.00,'2024-04-23 08:56:58'),(125,76,108,'tbsp',1.00,'2024-04-23 08:56:58'),(126,76,109,'tbsp',1.50,'2024-04-23 08:56:58'),(127,76,91,'tsp',1.00,'2024-04-23 08:56:59'),(128,76,92,'tsp',0.50,'2024-04-23 08:56:59'),(129,76,110,'tbsp',1.50,'2024-04-23 08:56:59'),(130,76,111,'slices',6.00,'2024-04-23 08:56:59'),(131,76,112,'bunch',1.00,'2024-04-23 08:56:59'),(132,77,113,'family size pack',1.00,'2024-04-23 10:20:30'),(140,83,118,'can',1.00,'2024-04-26 00:23:44'),(141,83,119,'cans',3.00,'2024-04-26 00:23:44'),(142,83,120,'cans',15.00,'2024-04-26 00:23:44'),(143,84,121,'whole',1.00,'2024-04-26 03:28:38'),(144,84,122,'boxes',3000.00,'2024-04-26 03:28:38'),(146,86,124,'pack',1.00,'2024-04-27 19:02:50'),(147,86,125,'pack',1.00,'2024-04-27 19:02:50'),(148,86,126,'tsp',1.00,'2024-04-27 19:02:50');
/*!40000 ALTER TABLE `recipe_ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(255) NOT NULL,
  `LastName` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `CreatedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Allergens` varchar(255) DEFAULT NULL,
  `Dislikes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'John','Doe','test@test.com','pass','2024-04-21 02:51:23','whale, fish','cilantro, cigarettes, lemon'),(2,'Jane','Doe','newuser@test.com','password','2024-04-21 02:54:16','grass','nothing'),(3,'Ran','McRandall','ran@test.com','TItXZdMGqHK26yV2UUY6Cs','2024-04-23 21:15:07',NULL,NULL),(4,'Bill','Clinton','bclinton@test.com','password','2024-04-27 18:24:33',NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-27 19:18:57
