# Scout Management & Location System

#### Video Demo: https://youtu.be/jL6nW5n97vs?si=DOGL4ndoZhGTCfNO

#### Description:

This project is a web-based scout management system developed as my final project for CS50x.  
The purpose of the project is to provide a simple and organized platform for registering scout members, storing their personal information, and visualizing their home locations on an interactive map.

The application is built using **Python with Flask** for the backend, **SQLite** for the database, and **HTML, CSS, JavaScript**, and **Leaflet.js** for the frontend. It applies many of the concepts taught in CS50, including user authentication, database design, sessions, and dynamic web pages.

---

## Project Overview

Scout groups often manage member data manually or using scattered tools.  
This project solves that problem by allowing users to:

- Register an account
- Log in securely
- Store personal information (name, phone number, birthday, and sector)
- Save a home location (latitude and longitude)
- View all registered users on a shared interactive map

Each registered scout appears as a pin on the map, with their name and sector shown when clicking the marker.

---

## Features Implemented

- User registration with password hashing
- User login with session management
- SQLite database with relational tables
- Interactive map using Leaflet.js
- Display of all users’ stored locations on the map
- Responsive layout compatible with desktop and mobile browsers

---

## File Structure

- `app.py`  
  The main Flask application file. Handles routing, authentication, database queries, and rendering templates.

- `scout.sql`  
  SQL schema file that defines the database tables used in the project.

- `templates/`  
  Contains all HTML templates:
  - `layout.html`: Base layout shared across all pages
  - `index_public.html`: Public home page
  - `register.html`: User registration page
  - `map.html`: Map page showing all user locations

- `static/`  
  Contains static files such as:
  - CSS stylesheets
  - Images
  - Video files used in the gallery/about sections

---

## Database Design

The project uses an SQLite database with the following tables:

- `users`: Stores user information such as name, hashed password, phone number, birthday, sector, and approval status.
- `maps`: Stores latitude and longitude associated with each user.
- `gallery`: Prepared for storing media files (not actively used in this version).

The tables are linked using foreign keys to maintain proper relationships between users and their locations.

---

## Design Decisions

- **Flask** was chosen for its simplicity and clarity when building small web applications.
- **SQLite** was used for ease of setup and local development.
- **Leaflet.js** was used to implement the interactive map because it is lightweight and open source.
- Password hashing was implemented to ensure user credentials are stored securely.

---

## Limitations

- There is no admin dashboard in the current version.
- All users are treated equally without roles.
- Media upload functionality is not yet implemented.

These limitations were accepted to keep the project focused and within scope.

---

## Academic Honesty

AI-based tools were used as learning assistants to help understand concepts and debug issues.  
All final decisions, structure, and implementation were done by me.

---

## Conclusion

This project represents my understanding of backend development, database management, and frontend integration as taught in CS50x.  
It demonstrates how multiple technologies can be combined to solve a real-world organizational problem.
