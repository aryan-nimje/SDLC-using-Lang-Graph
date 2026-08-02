# TaskFlow

TaskFlow is a personal task management application designed to help users organize and manage their daily tasks efficiently. It features user authentication, task and category management, and a responsive, modern user interface.

## Features

- User registration, login, and logout
- Dashboard with task statistics and recent activity
- Create, edit, delete, and mark tasks as completed
- Assign priority and due dates to tasks
- Categorize tasks and filter by status, priority, and category
- Responsive navigation bar and sidebar
- Confirmation dialogs and loading indicators
- RESTful API backend with Sequelize ORM and SQLite database

## Installation Instructions

### Backend

1. Navigate to the `backend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the backend server:
   ```bash
   node app.js
   ```

### Frontend

1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the frontend development server:
   ```bash
   npm start
   ```

## Project Folder Structure

```
TaskFlow/
├── backend/
│   ├── config/
│   │   └── database.js
│   ├── controllers/
│   │   ├── categoryController.js
│   │   ├── taskController.js
│   │   └── userController.js
│   ├── models/
│   │   ├── categoryModel.js
│   │   ├── index.js
│   │   ├── taskModel.js
│   │   └── userModel.js
│   ├── routes/
│   │   ├── categoryRoutes.js
│   │   ├── taskRoutes.js
│   │   └── userRoutes.js
│   └── app.js
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CategoryList.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Login.js
│   │   │   ├── Navbar.js
│   │   │   ├── Register.js
│   │   │   ├── Sidebar.js
│   │   │   ├── TaskForm.js
│   │   │   ├── TaskList.js
│   │   │   └── styles (CSS files)
│   │   ├── App.js
│   │   ├── index.css
│   │   └── index.js
└── README.md
```

## API Endpoint Summary

### User Authentication

- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login user and get JWT token
- `POST /api/users/logout` - Logout user (mock)

### Tasks

- `GET /api/tasks` - Get tasks (query params: userId, status, priority, categoryId, search)
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/:id` - Update a task
- `DELETE /api/tasks/:id` - Delete a task

### Categories

- `GET /api/categories` - Get categories (query param: userId)
- `POST /api/categories` - Create a new category
- `PUT /api/categories/:id` - Update a category
- `DELETE /api/categories/:id` - Delete a category

## Notes

- Passwords are securely hashed using bcrypt.
- JWT tokens are used for authentication (mocked in frontend).
- The database uses SQLite for simplicity.
- Input validation and error handling are implemented.
- The frontend is built with React and uses Axios for API calls.

---

This project is designed to be modular, maintainable, and easy to extend.
