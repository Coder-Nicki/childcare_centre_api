# CHILDCARE CENTRE API DOCUMENTATION

## Developed by Nicole Hulett

[GitHub - Childcare Centre API](https://github.com/Coder-Nicki/childcare_centre_api)

[Trello - Project Management](https://trello.com/b/tMMIqMil/childcare-centre-review-api)

### Instructions for installation:

1. Click on link GitHub link above
2. Clone the project to your local computer
3. Create a virtual environment 
4. Install the requirements text ```pip install requirements.txt``
5. Create the database (in psql)
    1. ```CREATE DATABASE childcare_api_db```
    2. 
6. Type ```Flask run``` in your command line
7. Open up Insomnia or Postman to test out routes


### R1 	Identification of the problem you are trying to solve by building this particular app.

Childcare is an industry that is currently seeing rapid growth in Australia. Most parents are now required to seek care for their child or children in the first 5 years of their lives as they return to work. For many parents this is a daunting prospect. All parents want the very best for their children. They want a childcare that will keep their child safe and provide a stimulating environment where they can grow and develop. However, finding the right childcare is often difficult. Most childcares these days do have a website or are listed on a directory of childcares with their current NQS (National Quality Standard) rating. But this doesn’t give parents the positive or negative feel for a centre. Parents most trust word-of-mouth from other parents that have or have had their child or children at the centre and experienced the daily operations of care. This application aims to replicate this idea by providing users with the ability to create a childcare centre listing, if one is not already available within the app, and then to provide a review of the childcare centre and give it a parent rating out of 10. Any user is then able to search the different childcare centres using multiple filters and read the reviews, good or bad, about each centre. This is all able to be done before calling up a centre and going for a tour. It will certainly reduce the number of centres that parents may have to visit to find the perfect fit for their child. This is so important in today’s busy world. 

### R2 	Why is it a problem that needs solving?

This problem needs solving as there is no current, simple way to search and compare childcare centres that provide parent reviews. Any current web sites or applications only provide the actual details and description of the centre. This is no longer enough for parents these days. Parents want to know what others think, parents want to be able to make an informed decision. Parents also do not want to waste their precious time going on countless tours of numerous childcare centres that would obviously not be a good fit for their child. 
This application would make the search for and decision about a childcare centre much simpler. It is important that this problem is solved soon, as childcare is an ever-growing industry. It is currently growing at a super rapid rate and appears to still not be keeping up with demand as more parents then ever, due to the rise in the cost of living and other reasons, require childcare for their young children. 
### R3 	Why have you chosen this database system. What are the drawbacks compared to others?

I have chosen to use a PostgreSQL database system as it is an object relational database management system that suits my project. My project is made up of related entities and a PostgreSQL system allows my data to be structured and defined in an appropriate, tabular way. PostgreSQL stores information in tables. Each table is required to have at least one column that has a specific data type and the rows of the table make up the records. A row is a single value entry that adheres to the predefined schema. A schema is like a blueprint or set of rules for what can or cannot enter the table. (Lemonaki, 2022). This is appropriate for my childcare_centre API project that has a number of different entities that would be translated into tables to store the incoming or outgoing information. PostgreSQL also allows for more than one table and for these tables to be related to one another. PostgreSQL uses the main data types as required by my application such as; string, boolean, integer and date/time. This DBMS also provides the needed constraints for my projects like, UNIQUE and NOT NULL. Primary Keys and Foreign Keys can also be used which are essential to develop the relationships between the different entities in my project and ensure data integrity and security. In addition, PostgreSQL supports the use of the Python programming language. PostgreSQL databases can be queried with simple or complex commands to perform any of the CRUD (Create, Read, Update, Delete) operations needed for my project. Some disadvantages of PostgreSQL are; it is slower in it’s processing capabilities compared to MySQL or NoSQL database managements systems. Also, not all open-source applications will support a PostgreSQL database. (Sharda, 2021).
Overall, PostgreSQL is a great fit as a DBMS for this API project to store and query the data in an organised and defined way. 

### R4 	Identify and discuss the key functionalities and benefits of an ORM

An ORM (Object Relational Mapping) is a way to connect an Object Orientated Program (OOP) with a relational database. An ORM helps to simplify the process of interacting with a database for the different CRUD operations like creating, reading, updating and deleting. Normally these interactions are done through SQL (structured query language) commands. (Abba, 2022)

An ORM uses much simpler methods to query the database. In this API project the Python programming language is used, therefore SQLAlchemy is a great choice for the ORM system. SQLAlchemy has great features and uses function-based query construction that allows SQL queries to be built similar to Python functions and expressions. SQLAlchemy can utilise the full range of functions to query a PostgreSQL database and can also use raw SQL statements if needed. In addition, SQLAlchemy uses composite behaviour and primary and foreign keys are represented in their own unique columns with the compatibility to ‘ON DELETE CASCADE and other tools and expressions for relationships within a database. (Features and Philosophy, n.d.)

#### Key functionality of an ORM:
-	Allows queries to be made to the database to manipulate the data using your program of choice, instead of plain SQL.
-	ORMs generate objects which map to tables in the database.
-	ORMs translate data/code and create a map that defines the database structure. The ORM can then explain how objects are related in different tables.
-	The ORM then uses its mapping information to convert data between tables to generate the SQL code that matches certain queries to cover the CRUD (create, read, update and delete) functionality.

#### Benefits

The benefits of using an ORM are; it handles the logic required to interact with databases, it improves security and eliminates the possibility of SQL injection attacks, you write less code using ORM tools compared to just using plain SQL queries, it speeds up development time and queries via the ORM can be written irrespective of whatever database is being used in the back end. ORMs are also available for any object orientated language, so it is not specific for just one language. 

#### Drawbacks

The disadvantages of using ORM tools are; it can be time consuming to learn, the processing time can be slower compared to SQL commands and they don’t perform as well when using super complex queries. Also a lot of magic happens behind scenes when using an ORM, so that can create confusion or difficulty in understanding the process. 

### R5 	Endpoints for the API

#### User Endpoints:

#### Public endpoints
- ``` @user.get('/')``` Gets a list of all users
- ```@user.get('/<int:id>')``` Finds a user by id number
- ```@user.get('/admins')``` Gets a list of all admin users
- ```@user.route("/register", methods=["POST"])``` creates a new user and logs them in

#### Protected endpoints
- ```@user.route("/login", methods=["POST"])``` logins in an already registered user
- ```@user.delete('/<int:id>')``` deletes a user

#### Childcare Centre Endpoints:

#### Public endpoints
- ```@childcare_centre.get('/')``` gets a list of all childcare centres
- ```@childcare_centre.get('/<int:id>')``` finds a childcare centre by id number
- ```@childcare_centre.get('/fee_range')``` lists the childcare centres from cheapest to most expensive
- ```@childcare_centre.get('/cheapest')``` finds the cheapest childcare centre
- ```@childcare_centre.get('/small_centres')``` gets a list of childcare centres that have a maximum capacity of under 50 kids
- ```@childcare_centre.get('/maximum_capacity/<int:maximum_capacity>')``` gets a list of childcare centres that have under a specified number of kids

#### Protected endpoints
- ```@childcare_centre.post("/")``` post a new childcare centre
- ```@childcare_centre.route("/<int:id>/", methods=["PUT"])``` update the details of a childcare centre
- ```@childcare_centre.delete('/<int:id>')``` finds a given childcare centre and deletes it.

### Review Routes:

#### Public endpoints
- ```@review.get('/')``` gets a list of all reviews
- ```@review.get('/<int:id>')``` finds a review by id
- ```@review.get('/<int:childcare_centre_id>')``` finds a re view by childcare centre id
- ```@review.get('/rating')``` gets a list of any childcare centres with a parent rating over 8

#### Protected endpoints
- ```@review.post("/")``` posts a new review
- ```@review.delete('/<int:id>')``` finds a review by id and deletes it

### Address Routes

#### Public endpoints
- ```@address.get('/childcare_centre/<int:childcare_centre_id>')``` finds an address by childcare centre id
- ```@address.get('/<string:suburb>')``` gets a list of childcare centres at a certain suburb
- ```@address.get('/postcode/<string:postcode>')``` gets a list of addresses from a specified suburb

#### Protected endpoint
- ```@address.post("/")``` creates a new address

### R6 	An ERD for your app

### R7 	Third party services that the app will use

Flask – Flask is a lightweight WSGI web application framework that allows developers to easily develop web applications. It is simple to use, but also extensible, which means the developer can easily extend its functionality and scale it up for more complex applications. The Flask web framework is written in Python and includes a collection of libraries and modules that allow an application to be built without having to worry about the low-level details of a web application and other protocols. 

Flask-SQLAlchemy – Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy in the application. Flask-SQLAlchemy is an ORM (Object Relational Mapper). It provides developers with a toolkit for the full functionality and flexibility of SQL. It helps to facilitate the communication between the application and the database. It translates Python classes to tables and converts function calls to SQL statements. 

Flask-Marshmallow – Flask-Marshmallow adds a thin integration layer between Flask and Marshmallow that provides additional features and can also optionally integrate with Flask-SQLAlchemy. Marshmallow is a Python library that converts complex data types to native Python data types and vice versa. It provides object serialization/deserialization.

Marshmallow-SQLAlchemy – Marshmallow-SQLAlchemy is a package that allows SQLAlchemy to integrate with the Marshmallow serialization/ library and assists in creating the schema more efficient. 

Flask-JWT-Extended – Flask-JWT-Extended adds support for using JSON Web Tokens. JSON web tokens are used in a Flask application for protecting routes and providing authentication to users. Flask-JWT-Extended has a lot of optional, but helpful features that you can use add to the project to make working with these tokens easier. 

### R8 	Describe your projects models in terms of the relationships they have with each other.

The four models for this project are User, Childcare Centre, Address and Review.

The relationship between User and Childcare Centre is a one-to-many relationship. One User can post many Childcare Centres, but a Childcare centre can only be posted by one User. 

User and Review is also a one-to-many relationship. One User can post many Reviews, but one Review belongs to one User.

Childcare Centre and Address have a one-to-one relationship. One Childcare Centre can have one Address and an Address can only belong to one Childcare Centre. 

Childcare Centre and Review has a one-to-many relationship. One Childcare Centre can have many Reviews, but a Review only belongs to one Childcare Centre. 

### R9 	Discuss the database relations to be implemented in your application

My database is to have four entities or tables: Users, Childcare centres, Reviews and Addresses. The User entity will include a username, password, email address and an attribute for whether a user is an admin or not. The Childcare centre entity will include attributes such as name, description, the cost per day, the maximum capacity of the centre. The Address entity will include address details such as; street number, street name, suburb, postcode and state. The Reviews entity includes attributes such as; parent rating, comment and date posted. 

For this application, a User should be able to register or login with the required details. A User is then able to update or post a new Childcare centre listing. 

A Childcare centre listing can have an Address or zero or more Reviews. 

Reviews belong to a specific Childcare centre. 

Only registered or logged in Users can make posts of update details.

Anyone is able to get a list of Childcare centres, or the Address attached to Childcare centres or the Reviews listed for a Childcare centre. Only an admin can get a list of Users or delete a Childcare centre listing or Review. 

### R10 	Describe the way tasks are allocated and tracked in your project

Trello was used to allocate and track the progress of this project. The project was broken down into smaller tasks with a checklist of things to complete for each task. There were four lists; ‘To Do’, ‘In Progress’, ‘Done’ and ‘In the future’. 

To start with I made a list of the tasks that needed to be done for this project and made a card for each task that was allocated to the ‘To Do’ list. Within each of these tasks, I then broke it down further to create a checklist of everything that needed to be done to complete the task. I added a priority label and due date for each task card to keep myself accountable. I chose the Higher Priority tasks to work on first and would move these into the ‘In Progress’ card list. Some higher priority tasks were creating an ERD, creating the Flask application and setting up a configuration file. All these tasks were essential to be completed before other tasks could start. Once a task was completed and all checklist items ticked off, the task was then moved to the ‘Done’ list. It felt really productive to see tasks sitting in the ‘Done’ list. 

Once tasks were completed, I then added new ‘To Do’ cards to the ‘In Progress’ list and started working on them in the project. These cards often had a medium priority status. They involved setting up the models, schema and routes for each specific entity and then defining the relationships between entities. In hindsight, these tasks could have been broken down further as they were very large tasks to complete and took quite a bit of time. The low priority tasks were the last to be moved into the ‘In Progress’ list as these did not have a massive effect on the project and had no other tasks dependent on them be completed. However, they were still a requirement for the fully functioning project. 

Slowly all task cards moved from ‘To Do, ‘In Progress’ and then to ‘Done’ as the project took shape. Along the way, new cards were created and added to the ‘In the future’ list as I thought of ways to extend my application if more time permitted. One day these can be moved to the ‘To Do’ list, but at this stage were not a requirement for the project. 

![screenshot of trello board](docs/first_screenshot.png)

![screenshot of trello board](docs/second_screenshot.png)

![screenshot of trello board](docs/third_screenshot.png)

![screenshot of trello board](docs/task_screenshot.png)

![screenshot of trello board](docs/task2_screenshot.png)
### References

Abba, I. V. (2022, October 21). What is an ORM – The Meaning of Object Relational Mapping Database Tools. Retrieved from freeCodeCamp: https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/

Features and Philosophy. (n.d.). Retrieved from SQLAlchemy: https://www.sqlalchemy.org/features.html

Lemonaki, D. (2022, April 18). Relational VS Nonrelational Databases – the Difference Between a SQL DB and a NoSQL DB. Retrieved from freeCodeCamp: https://www.freecodecamp.org/news/relational-vs-nonrelational-databases-difference-between-sql-db-and-nosql-db/

Sharda, A. (2021, April 29). What is PostgreSQL? Introduction, Advantages & Disadvantages. Retrieved from LinkedIn: https://www.linkedin.com/pulse/what-postgresql-introduction-advantages-disadvantages-ankita-sharda/


