HBnB - Business Logic and API

Overview
This project is part of the Holberton School curriculum and represents the second phase of the HBnB application. The main focus is to implement the core business logic and RESTful API endpoints using Flask and Flask-RESTx, following modular design principles and the Facade pattern.

The goal is to create a maintainable and scalable backend architecture that supports Users, Places, Amenities, and Reviews. Features like JWT authentication and database persistence will be introduced in future stages.

Project Objectives
Organize the application following a modular Python project structure

Implement the core business logic for Users, Places, Amenities, and Reviews

Build RESTful APIs using Flask-RESTx

Use the Facade pattern to abstract and unify business operations

Validate inputs at the logic layer

Perform black-box and unit testing

Document the entire API using Swagger

Technologies Used
Python 3.12

Flask

Flask-RESTx

cURL (manual endpoint testing)

Swagger (API documentation and interactive testing)

In-memory repository (temporary data storage)

Project Structure
hbnb/
├── app/
│ ├── __init__.py
│ ├── api/
│ │ ├── __init__.py
│ │ ├── v1/
│ │ │ ├── __init__.py
│ │ │ ├── users.py
│ │ │ ├── places.py
│ │ │ ├── reviews.py
│ │ │ ├── amenities.py
│ ├── models/
│ │ ├── __init__.py
│ │ ├── user.py
│ │ ├── place.py
│ │ ├── review.py
│ │ ├── amenity.py
│ ├── services/
│ │ ├── __init__.py
│ │ ├── facade.py
│ ├── persistence/
│ │ ├── __init__.py
│ │ ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md

Implementation Resume
Business Logic Layer:
Each model (User, Place, Review, Amenity) is implemented as a Python class with attributes, validation logic, and serialization methods. UUIDs are used for unique IDs. Validation occurs on creation and update.

Facade Pattern:
All business operations are routed through a centralized Facade service, which acts as a bridge between the API layer and business logic, promoting separation of concerns.

API Layer:
Each model has its own Flask-RESTx namespace with documented endpoints. The API handles serialization, error responses, and returns structured JSON.

Endpoints Implemented
User

POST /users/ – Create a user

GET /users/ – Retrieve all users

GET /users/{id} – Retrieve one user by ID

PUT /users/{id} – Update a user

Place

POST /places/ – Create a place

GET /places/ – Retrieve all places

GET /places/{id} – Retrieve a specific place

PUT /places/{id} – Update a place

Amenity

POST /amenities/ – Create an amenity

GET /amenities/ – List all amenities

GET /amenities/{id} – Get an amenity by ID

PUT /amenities/{id} – Update an amenity

Review

POST /reviews/ – Create a review

GET /reviews/ – List all reviews

GET /reviews/{id} – Get a review by ID

PUT /reviews/{id} – Update a review

DELETE /reviews/{id} – Delete a review

GET /reviews/places/{place_id} – Get all reviews for a place

Testing & Validation
Validation Rules:
Input validation is handled in the business logic. It ensures required fields are provided, data types are correct, and entity relationships exist (e.g., a review must belong to a user and a place).

Manual Testing:
All endpoints were tested with:

Swagger (interactive documentation)

cURL (manual black-box testing)

Example cURL command:
POST a user:
curl -X POST http://127.0.0.1:5000/users/ -H "Content-Type: application/json" -d '{"first_name": "Bruno", "last_name": "Barrera", "email": "bruno@example.com"}'

Swagger Documentation
Swagger UI is available at the root URL once the server is running:

http://127.0.0.1:5000/

From here, all endpoints can be tested interactively.

Setup & Installation
Clone the repository:
git clone https://github.com/BrunoBarrera1/holbertonschool-hbnb.git

Navigate to the project folder:
cd holbertonschool-hbnb/part2

Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run the app:
python3 run.py

Resources
Flask Documentation – https://flask.palletsprojects.com/en/stable/

Flask-RESTx – https://flask-restx.readthedocs.io/en/latest/

RESTful API Design – https://restfulapi.net/

Python OOP – https://realpython.com/python3-object-oriented-programming/

Facade Pattern – https://refactoring.guru/design-patterns/facade/python/example

Authors: Bruno Barrera, Juandiego Martinez


