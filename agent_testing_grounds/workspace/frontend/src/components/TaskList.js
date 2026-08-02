import React from 'react';
import './TaskList.css';

const TaskList = ({ tasks, onEdit, onDelete, onToggleComplete }) => {
  return (
    <table className="task-list">
      <thead>
        <tr>
          <th>Title</th>
          <th>Priority</th>
          <th>Status</th>
          <th>Due Date</th>
          <th>Category</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {tasks.map(task => (
          <tr key={task.id} className={task.status === 'Completed' ? 'completed' : ''}>
            <td>{task.title}</td>
            <td>{task.priority}</td>
            <td>{task.status}</td>
            <td>{task.dueDate ? new Date(task.dueDate).toLocaleDateString() : '-'}</td>
            <td>{task.categoryName || '-'}</td>
            <td>
              <button onClick={() => onToggleComplete(task)}>
                {task.status === 'Completed' ? 'Mark Pending' : 'Mark Completed'}
              </button>
              <button onClick={() => onEdit(task)}>Edit</button>
              <button onClick={() => onDelete(task)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TaskList;
