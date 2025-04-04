# Library API

**Library API** is a RESTful API designed for managing library resources such as books, borrowings, and users. This application aims to automate the management of library data and provide an easy way to interact with the database via an API.

## Features:

- **User management**: User registration and authentication.
- **Book management**: Create, read, update, and delete books data.
- **Borrowings**: Users can borrow books for a specific period and return them.
- **API Documentation**: Swagger provides full documentation for all available endpoints and their functionalities.

## How to Run the Project

To run the project in a Docker container, follow these steps:

### 1. Make sure you have Docker installed.

### 2. Download and build the project:
```bash
docker-compose up --build
```

### 3. Wait for the build and container start to complete. Once done, the application will be available at:

http://localhost:8000

### 4. Register a new user by sending a POST request to the endpoint:
POST /users/

### 5. After registration, you can log in and start using the available API features.

### The tasks below are showing what I've done in my project

## Implement the CRUD functionality for the Books Service

### Initialize the Books App
- Set up a new Django app for books.
  
### Add the Book Model
- Create a model to represent books, including necessary fields such as `title`, `author`, `isbn`, `inventory`, etc.

### Implement the Serializer & Views for All the Endpoints
- Implement a serializer for the book model to handle data validation and transformation.
- Create views for the following endpoints:
  - **Create** a book (Admin only).
  - **Read** (list and detail) books (available to all users, even unauthenticated).
  - **Update** a book (Admin only).
  - **Delete** a book (Admin only).

## Add Permissions to the Books Service
- Only admin users should have permission to create, update, and delete books.
- All users, including unauthenticated users, should be able to list books.
- Use JWT token authentication from the Users service to handle authorization.

## Implement CRUD for the Users Service

### Initialize the Users App
- Set up a new Django app for users.

### Add the User Model with Email
- Create a user model with necessary fields, including an email field for user identification.

### Add JWT Support
- Implement JWT authentication for users, so they can securely log in and interact with the API.

### Modify Authorization Header for JWT Authentication
- For a better experience with the **ModHeader** Chrome extension, change the default `Authorization` header for JWT authentication to `Authorize`. You can refer to the documentation for detailed steps on how to handle it.

### Implement the Serializer & Views for All the Endpoints
- Create the necessary serializers and views to manage user creation, authentication, and other relevant operations.

## Implement the Borrowing List & Detail Endpoint

### Initialize the Borrowings App
- Set up a new Django app for borrowings.

### Add the Borrowing Model
- Create the borrowing model with fields for `borrow_date`, `expected_return_date`, and `actual_return_date`, with constraints on these fields.

### Implement the Read Serializer with Detailed Book Info
- Implement a serializer for the borrowings list and detail views, ensuring it includes detailed information about the associated book.

### Implement the List & Detail Endpoints
- Create endpoints for listing borrowings and viewing details of a specific borrowing.

## Implement the Create Borrowing Endpoint

### Implement Create Serializer
- Create a serializer to handle borrowing creation requests, including validation logic.

### Validate Book Inventory
- Ensure the book is available (i.e., the inventory is not 0) before allowing a borrowing.

### Decrease Inventory by 1 for the Book
- After a borrowing is successfully created, decrease the corresponding book's inventory by 1.

### Attach the Current User to the Borrowing
- Associate the borrowing with the current user (authenticated via JWT).

### Implement the Create Endpoint
- Create an endpoint for creating borrowings, which will use the serializer to process the request.

## Add Filtering for the Borrowings List Endpoint

### Ensure Each Non-Admin Can See Only Their Own Borrowings
- Add filtering logic to allow users to view only their own borrowings.

### Ensure Borrowings Are Available Only for Authenticated Users
- Make sure the borrowings endpoint is accessible only for authenticated users.

### Add the `is_active` Parameter for Filtering Active Borrowings
- Add an `is_active` parameter to allow users to filter borrowings that are still active (not returned yet).

### Add the `user_id` Parameter for Admin Users
- For admin users, allow the option to filter borrowings by `user_id`. If not specified, all borrowings should be visible; otherwise, show borrowings only for a specific user.

## Implement the Return Borrowing Functionality

### Prevent Returning a Borrowing Twice
- Implement logic to prevent a user from returning the same borrowing more than once.

### Add 1 to Book Inventory on Returning
- Increase the inventory of the book by 1 when it is returned.

### Add an Endpoint for Returning Borrowings
- Create an endpoint for returning borrowings, which will trigger the inventory update and prevent multiple returns.

## Setup Docker-Compose

- Set up a `docker-compose.yml` file to define and run the multi-container Docker application.
- Ensure that the Docker containers for the app, database, and any other necessary services (like Redis or Celery, if required) are correctly configured.
