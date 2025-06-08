![IMG_6431](https://github.com/user-attachments/assets/2af37ba7-812d-47a7-a8e8-a6b4885407f1)
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
![image](https://github.com/user-attachments/assets/9ea747d4-ede1-4603-ae58-1a915c787db8)
We also have a mermaid chart version in which we specify a bit more the content of each layer.
![highlevelpackagediagram drawio_480](https://github.com/user-attachments/assets/19d9bd0c-3b96-4718-a270-b014c4da4910)
![editor___mermaid_chart-2025-06-06-142358_720](https://github.com/user-attachments/assets/f86e2621-032a-49e5-8e39-7e00eb502dfb)
![editor___mermaid_chart-2025-06-06-141431_720](https://github.com/user-attachments/assets/209d70b5-7ba2-4832-8123-6afee91ea580)
![editor___mermaid_chart-2025-06-06-140700_720](https://github.com/user-attachments/assets/87472865-c803-4621-a206-219f48158cad)
![editor___mermaid_chart-2025-06-06-135630_720](https://github.com/user-attachments/assets/33c9b1b5-4904-4229-908a-0c534310a7b1)
![Editor___Mermaid_Chart-2025-06-04-170558_(2)](https://github.com/user-attachments/assets/80b2e24a-292e-42c6-a60f-2fde852caa35)
