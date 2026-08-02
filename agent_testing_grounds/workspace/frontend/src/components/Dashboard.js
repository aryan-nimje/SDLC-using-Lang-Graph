import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = ({ userId, username }) => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`/api/tasks?userId=${userId}`);
        setTasks(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load tasks');
        setLoading(false);
      }
    };

    if (userId) {
      fetchTasks();
    }
  }, [userId]);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  const pendingTasks = tasks.filter(task => task.status === 'Pending').length;
  const completedTasks = tasks.filter(task => task.status === 'Completed').length;
  const today = new Date().toISOString().split('T')[0];
  const tasksDueToday = tasks.filter(task => task.dueDate && task.dueDate.startsWith(today)).length;

  return (
    <div className="dashboard">
      <h2>Welcome, {username}!</h2>
      <div className="dashboard-cards">
        <div className="card">
          <h3>Pending Tasks</h3>
          <p>{pendingTasks}</p>
        </div>
        <div className="card">
          <h3>Completed Tasks</h3>
          <p>{completedTasks}</p>
        </div>
        <div className="card">
          <h3>Tasks Due Today</h3>
          <p>{tasksDueToday}</p>
        </div>
      </div>
      <div className="recent-activity">
        <h3>Recent Activity</h3>
        <ul>
          {tasks.slice(-5).reverse().map(task => (
            <li key={task.id}>{task.title} - {task.status}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
