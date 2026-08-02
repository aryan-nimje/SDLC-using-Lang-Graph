import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import TaskList from './components/TaskList';
import TaskForm from './components/TaskForm';
import CategoryList from './components/CategoryList';
import Login from './components/Login';
import Register from './components/Register';
import './App.css';

const App = () => {
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [editingTask, setEditingTask] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user) {
      fetchTasks();
      fetchCategories();
    }
  }, [user]);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const categoryFilter = selectedCategory ? `&categoryId=${selectedCategory}` : '';
      const response = await axios.get(`/api/tasks?userId=${user.id}${categoryFilter}`);
      setTasks(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch tasks');
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`/api/categories?userId=${user.id}`);
      setCategories(response.data);
    } catch (err) {
      setError('Failed to fetch categories');
    }
  };

  const handleLogin = (data) => {
    setUser({ id: data.userId, username: data.username, token: data.token });
    axios.defaults.headers.common['Authorization'] = `Bearer ${data.token}`;
  };

  const handleLogout = () => {
    setUser(null);
    setTasks([]);
    setCategories([]);
    setSelectedCategory(null);
    setEditingTask(null);
    delete axios.defaults.headers.common['Authorization'];
  };

  const handleCreateTask = () => {
    setEditingTask({});
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
  };

  const handleDeleteTask = async (task) => {
    if (window.confirm(`Are you sure you want to delete the task "${task.title}"?`)) {
      try {
        await axios.delete(`/api/tasks/${task.id}`);
        fetchTasks();
      } catch (err) {
        setError('Failed to delete task');
      }
    }
  };

  const handleToggleComplete = async (task) => {
    try {
      await axios.put(`/api/tasks/${task.id}`, {
        status: task.status === 'Completed' ? 'Pending' : 'Completed'
      });
      fetchTasks();
    } catch (err) {
      setError('Failed to update task status');
    }
  };

  const handleSaveTask = async (taskData) => {
    try {
      if (editingTask.id) {
        await axios.put(`/api/tasks/${editingTask.id}`, taskData);
      } else {
        await axios.post('/api/tasks', { ...taskData, userId: user.id });
      }
      setEditingTask(null);
      fetchTasks();
    } catch (err) {
      setError('Failed to save task');
    }
  };

  const handleCancelTask = () => {
    setEditingTask(null);
  };

  const handleSelectCategory = (categoryId) => {
    setSelectedCategory(categoryId);
  };

  return (
    <Router>
      <Navbar isLoggedIn={!!user} onLogout={handleLogout} />
      <div className="app-container">
        {user && <Sidebar />}
        <main className="main-content">
          <Routes>
            <Route path="/" element={user ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
            <Route path="/login" element={<Login onLogin={handleLogin} />} />
            <Route path="/register" element={<Register onRegister={handleLogin} />} />
            <Route path="/dashboard" element={user ? <Dashboard userId={user.id} username={user.username} /> : <Navigate to="/login" />} />
            <Route path="/tasks" element={user ? (
              <>
                <button onClick={handleCreateTask}>New Task</button>
                {loading ? <p>Loading tasks...</p> : (
                  <TaskList
                    tasks={tasks}
                    onEdit={handleEditTask}
                    onDelete={handleDeleteTask}
                    onToggleComplete={handleToggleComplete}
                  />
                )}
                {editingTask && (
                  <TaskForm
                    task={editingTask.id ? editingTask : null}
                    categories={categories}
                    onSave={handleSaveTask}
                    onCancel={handleCancelTask}
                  />
                )}
              </>
            ) : <Navigate to="/login" />} />
            <Route path="/categories" element={user ? (
              <CategoryList categories={categories} onSelectCategory={handleSelectCategory} />
            ) : <Navigate to="/login" />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
