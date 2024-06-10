# TA Scheduling Application

## Overview

Welcome to the TA Scheduling Application project! This project was developed as part of the CS361 course, aimed at automating the process of assigning Teaching Assistants (TAs) to courses, managing their contact information, and implementing role-based access controls. The application is designed to streamline the administration of graduate student TAs, addressing the complexities of their course assignments and information management.

## Features

- **Automated Course Assignments**: Efficiently assigns TAs to courses based on predefined criteria and availability.
- **Contact Information Management**: Maintains up-to-date contact details for all TAs, ensuring easy access for administrators and faculty.
- **Role-Based Access Control**: Implements different access levels for users based on their roles (e.g., administrator, faculty, TA) to ensure data security and appropriate permissions.

## Getting Started

To get started with the TA Scheduling Application, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/ekruse09/CS_361_project]

2. **Install Dependencies**:
Navigate to the project directory and install the required dependencies:

   ```bash
   cd Code

   ```bash
   pip install django

3. **Setup The Database**:
Before migrating, generate migration files for any changes to your models:

   ```bash
   python manage.py makemigrations

   ```bash
   python manage.py migrate

4. **Run The Application**:
   ```bash
   python manage.py runserver

To access the application, open your web browser and navigate to http://localhost:8000.





