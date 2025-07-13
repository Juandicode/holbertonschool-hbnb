![HBnB Logo](./hbnb_logo.png)

# HBnB – Part 3: Enhanced Backend with Authentication and Database Integration

This repository contains the third part of the HBnB project: a secure, database‑backed backend powered by Flask, SQLAlchemy, JWT authentication, and role‑based access control. In this stage you replace in‑memory storage with a persistent relational database, introduce user authentication and authorization, and produce a visual model of your schema with Mermaid.js.

---

## Table of Contents

1. [Features](#features)  
2. [Getting Started](#getting-started)  
3. [Configuration](#configuration)  
4. [Database Setup](#database-setup)  
5. [Running the Application](#running-the-application)  
6. [API Endpoints](#api-endpoints)  
7. [Data Models & Relationships](#data-models--relationships)  
8. [Mermaid ER Diagram](#mermaid-er-diagram)  
9. [Testing](#testing)  
10. [Roadmap](#roadmap)

---

## Features

- **JWT Authentication**  
  Secure login and token issuance with `flask-jwt-extended`.

- **Role‑Based Access Control**  
  Admin users (`is_admin`) can manage all resources; regular users can only modify their own.

- **SQLAlchemy Persistence**  
  SQLite in development, easily switchable to MySQL for production.

- **CRUD Endpoints**  
  Full create, read, update, and delete operations for Users, Places, Reviews, and Amenities.

- **Data Validation & Security**  
  Bcrypt password hashing, request payload validation, and proper HTTP status codes.

- **Schema Visualization**  
  ER diagram rendered with Mermaid.js for clear documentation of relationships.

---

## Getting Started

### Prerequisites

- Python 3.8+  
- Virtual environment tool (venv, pipenv, etc.)  
- PostgreSQL or MySQL for production (SQLite is used by default)  
- Node.js (for Mermaid live preview, optional)

### Install Dependencies

```bash
git clone https://github.com/BrunoBarrera1/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Configuration
Copy the sample configuration and update with your credentials:

bash
cp instance/config.py.example instance/config.py
Edit instance/config.py:

python
class Config:
    SECRET_KEY               = "a‑very‑secret‑key"
    SQLALCHEMY_DATABASE_URI  = "sqlite:///data/hbnb_dev.db"
    JWT_SECRET_KEY           = "another‑secret‑key"
    # For production (MySQL):
    # SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://user:password@host/db_name"
Database Setup
Create migrations

bash
flask db init
flask db migrate -m "Initial schema"
flask db upgrade
Seed initial data (optional)

bash
python scripts/seed_data.py
Running the Application
Start the development server:

bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
By default, the API will be available at http://127.0.0.1:5000/api/v1.

API Endpoints
POST /api/v1/auth/login
Authenticate user and receive JWT tokens.

POST /api/v1/users/
Register a new user (admin only).

GET /api/v1/users/<id>
Retrieve user profile (self or admin).

GET /api/v1/states, POST /api/v1/states, etc.
Full CRUD for States, Cities, Places, Reviews, Amenities.

See API_DOCUMENTATION.md for full details.

Data Models & Relationships
Entity	Attributes
User	id, first_name, last_name, email, password_hash, is_admin
Place	id, title, description, price, latitude, longitude, owner_id
Review	id, text, rating, user_id, place_id
Amenity	id, name
PlaceAmenity	place_id, amenity_id

A User can own many Places (one‑to‑many).

A Place can have many Reviews (one‑to‑many) and many Amenities (many‑to‑many via PlaceAmenity).

A Review belongs to one User and one Place.

Mermaid ER Diagram
mermaid
erDiagram
    USER {
        int    id PK
        string first_name
        string last_name
        string email
        string password_hash
        bool   is_admin
    }
    PLACE {
        int    id PK
        string title
        string description
        float  price
        float  latitude
        float  longitude
        int    owner_id FK
    }
    REVIEW {
        int    id PK
        string text
        int    rating
        int    user_id FK
        int    place_id FK
    }
    AMENITY {
        int    id PK
        string name
    }
    PLACE_AMENITY {
        int place_id  FK
        int amenity_id FK
    }

    USER ||--o{ PLACE          : owns
    USER ||--o{ REVIEW         : writes
    PLACE ||--o{ REVIEW         : has
    PLACE ||--o{ PLACE_AMENITY  : links
    AMENITY ||--o{ PLACE_AMENITY : linked_by
Paste the above into a Mermaid live editor or include directly in your Markdown for a rendered diagram.

Developed by Bruno Barrera and Juan Diego Martinez
