![IMG_6431](https://github.com/user-attachments/assets/944aa549-f562-4ff2-a964-74e949a307f4)
# HBNB Documentation

## Introduction & Objectives

The **HBNB** documentation project aims to provide a clear mapping of an Airbnb-inspired application architecture, relationships, and workflows to facilitate future frontend and backend development.

- **Authors**: Bruno Barrera and Juan Diego Martínez (#C26)
- **Goal**: Document system layers, data models, and process flows to ensure maintainability, scalability, and ease of onboarding in the future.

# Content of the documentation:

The main content of the documentation is divided into 3 types of documents listed together with the software we used to make the diagrams

## Technologies & Tools

| Level | Tool | Primary Use |
| --- | --- | --- |
| Diagramming | Draw.io, Mermaid | Package and flow diagrams |
| Diagramming | Mermaid | Class diagrams |
| Sequence Flows | Mermaid | Sequence diagrams |
| Documentation | Notion | Collaborative authoring |

## Project Architecture and Diagrams

### High-Level Package Diagram

Our high-level package diagram offers a “big-picture” view of the system. It shows how a user’s request flows from the moment it enters the Presentation Layer, is processed by the Business Logic Layer, and finally interacts with the Persistence Layer before a response is returned. This diagram shows each layer’s responsibility and how they collaborate to complete every operation.

### Layers

**Presentation Layer**

This is the application’s frontend. It handles all incoming user interactions—whether through web pages, forms, or API calls—and ensures that each request is authenticated and validated before reaching the core logic. Its main components are:

- **User Interface (UI):** Screens, forms, and navigation elements for direct user interaction.
- **API Service:** Controllers and validators that receive HTTP requests, enforce security rules, invoke business operations, and format the outgoing responses (JSON).

**Business Logic Layer**

Consider this the heart of our application. It encapsulates domain rules and directs workflows that implement the app’s core functionality. Key elements include:

- **Facade Services:** Simplified entry points that group together multiple operations into high-level methods.
- **Domain Entities:** In-memory models of core concepts such as User, Place, and Review.
- **Workflow & Validation Modules:** Components that enforce business rules (for example, pricing calculations or review approval) and coordinate calls between services, repositories, and external systems.

**Persistence Layer**

This layer is responsible for all data storage and retrieval, ensuring that the state of domain entities is syncronized with the database. Its components are:

- **Repositories:** Abstractions that translate between objects in code and records in the database.
- **Database Connectors & Transaction Managers:** Utilities to open connections, manage transactions (commit/rollback), and handle retries or failures.
- ![highlevelpackagediagram drawio_480](https://github.com/user-attachments/assets/3fa99ff3-8dc8-4fe0-afd5-52f575e4a7fe)
 
 We also have a mermaid chart version in which we specify a bit more the content of each layer.

- ![image](https://github.com/user-attachments/assets/12f78c08-1609-48c9-8ceb-d252a32e67fd)
  
 ### Class Diagram

The class diagram illustrates the key entities in the system and how they relate to one another. It provides a clear overview of each class’s role and its connections, ensuring that developers can quickly understand the domain model.

**Core Classes**

- **BaseModel**
    
    Serves as the superclass for all domain objects. It centralizes common functionality—automatic `id` generation and creation/update timestamps—so that every model inherits these capabilities without duplication.
    
- **User**
    
    Represents a registered platform user. Beyond basic profile data, this class acts as the owner of any places they list and as the author of reviews they submit.
    
- **Place**
    
    Models a property listing (house or apartment). It includes details like location, description, and pricing, and it maintains associations with its owner (`User`), any reviews it has received, and available amenities.
    
- **Review**
    
    Captures user feedback on a particular `Place`. Each review records a rating, comments, and references both the `User` who wrote it and the `Place` being reviewed.
    
- **Amenity**
    
    Defines optional features or services (“Wi-Fi,” “Pool,” “Parking”) that can be attached to a `Place`. Amenities help guests understand what a listing offers at a glance.
    

**Relationships**

- Every domain class inherits from **BaseModel**, ensuring consistent handling of identifiers and timestamps.
- A single **User** may own multiple **Place** listings, reflecting a one-to-many relationship.
- A **Place** can accumulate multiple **Review** entries, representing feedback from different users.
- **Place** and **Amenity** share a many-to-many relationship: each place can offer multiple amenities, and each amenity can apply to multiple places.
- Each **Review** is linked to exactly one **User** (the reviewer) and one **Place** (the subject), enforcing referential integrity in the feedback process.
![Editor___Mermaid_Chart-2025-06-04-170558_(2)](https://github.com/user-attachments/assets/36b77710-2ed1-4f03-954e-4cbda1a414e7)

### Sequence Diagrams

Sequence diagrams map out the real-time interactions between components across the Presentation, Business Logic, and Persistence layers for key operations. They are invaluable for:

- **Clarifying Flow**: Visualizing the exact order of method calls, data validations, and database interactions.
- **Onboarding Developers**: Helping team members quickly unserstand how API requests are processed end-to-end.
- Debugging: Identifying potential bottlenecks or missing steps in request handling.

### User Registration Flow

This diagram illustrates each step from when a new user submits the registration form to the final response:

1. **Client Request**: The UI sends a `POST /register` request with user credentials.
2. **Validation**: The API Service validates input (email format, password strength).
3. **Business Processing**: The Registration Facade checks for existing users, applies hashing to the password, and creates a `User` entity.
4. **Persistence**: The User Repository saves the new record to the database.
5. **Response**: A success message (or error) is returned to the client.
6. ![editor___mermaid_chart-2025-06-06-135630_720](https://github.com/user-attachments/assets/6487fdff-0ce7-4b80-acff-d8394a2ea1e3)
7. 
8. ### Create Place Example

This diagram shows the sequence of operations when a user creates a new place:

1. The client sends a request to create a new place (`POST /places`).
2. The API service checks authentication and validates the request data.
3. The business logic processes the data and creates a `Place` object, associating it with the user.
4. The persistence layer saves the `Place` to the database.
5. A response containing the newly created place is returned to the client.
6. ![editor___mermaid_chart-2025-06-06-140700_720](https://github.com/user-attachments/assets/ad5971e7-b2d4-4c20-a1aa-d92e19883c94)

### Review Example

This sequence diagram illustrates what happens when a user posts a review:

1. The client sends a request to review a place (`POST /places/:id/reviews`).
2. The API service authenticates the user and validates the input.
3. The business logic creates a `Review` object, linking it to both the `User` and `Place`.
4. The persistence layer stores the review in the database.
5. The API returns a confirmation ![editor___mermaid_chart-2025-06-06-141431_720](https://github.com/user-attachments/assets/6af8ee15-7c94-4ca0-8574-7c97007a6304)
or the created review object.

7. ### List of Places Request Example

This diagram shows what happens when a user requests a list of available places:

1. The client sends a request (`GET /places`).
2. The API service processes the request and parses any query parameters (filters).
3. The business logic requests the data from the persistence layer.
4. The database returns a list of `Place` objects.
5. The API formats and sends the list back to the client.
![editor___mermaid_chart-2025-06-06-142358_720](https://github.com/user-attachments/assets/4d4f2bb4-669f-4ee3-8aef-1e4be3e32b81)

## Overall Purpose

Together, these diagrams offer both **structural clarity** and **behavioral insight**, forming a comprehensive understanding of how the system is built and how it operates in practice.

This dual perspective is crucial for:

- Onboarding new developers
- Maintaining a clean and scalable architecture
- Facilitating refactoring and testing
- Ensuring alignment between the codebase and the original system design
- Supporting long-term maintainability and collaboration

Ultimately, these visual models turn abstract code into something concrete and under, ensuring that everyone on the team technical or not can speak the same language when it comes to the system’s design.


