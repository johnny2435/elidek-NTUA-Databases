# ELIDEK - Research and Innovation Management System - Database Development Project

This project involved the complete development of a relational database to manage projects, researchers, organizations, and associated data for a research and innovation management system.

### **Authors**
- **Ioannis Dorkofikis**
- **Despoina Vidali**

## Key Features

### 1. Schema Design and Implementation
- **Conceptual Design**: ER diagrams to define entities and relationships.
- **Logical Design**: Relational model with constraints, primary/foreign keys, and normalization.
- **Physical Design**: SQL scripts for table creation and indexing.

### 2. Data Management and Queries
- Implemented **triggers** to enforce business rules (e.g., ensuring organizational consistency between projects and researchers).
- Designed **views** for easier data retrieval (e.g., projects with associated researchers).
- Added calculated fields, such as **project duration**, using computed columns.

### 3. Integration and Automation
- **Python scripts** were used for establishing a connection to the database and executing queries.
- **HTML-based interface** was created to allow users to perform **CRUD operations** and execute specific queries on the database.

### 4. Advanced Features
- Triggers to enforce complex rules, such as validating organizational alignment.
- **Indexes** to optimize query performance for date fields and text-based searches.

## Technologies Used
- **SQL** for database design and queries.
- **Python** for database connection, query execution, and data generation.
- **HTML** for front-end CRUD functionalities and specific queries.

## Code Highlights
- The database schema includes tables for projects, researchers, organizations (with subtypes for universities, companies, and research centers), and deliverables.
- Views provide summarized information for users, such as `project_researcher_view` and `org_university_view`.
- Triggers enforce business logic, ensuring data integrity during insertion and updates.
