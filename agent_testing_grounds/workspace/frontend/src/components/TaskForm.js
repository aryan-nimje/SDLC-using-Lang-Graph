import React, { useState, useEffect } from 'react';
import './TaskForm.css';

const TaskForm = ({ task, categories, onSave, onCancel }) => {
  const [title, setTitle] = useState(task ? task.title : '');
  const [description, setDescription] = useState(task ? task.description : '');
  const [priority, setPriority] = useState(task ? task.priority : 'Medium');
  const [dueDate, setDueDate] = useState(task ? (task.dueDate ? task.dueDate.split('T')[0] : '') : '');
  const [categoryId, setCategoryId] = useState(task ? task.categoryId : '');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Title is required');
      return;
    }
    setError('');
    onSave({ title, description, priority, dueDate, categoryId });
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      {error && <div className="error-message">{error}</div>}
      <label>Title</label>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />

      <label>Description</label>
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <label>Priority</label>
      <select value={priority} onChange={(e) => setPriority(e.target.value)}>
        <option value="Low">Low</option>
        <option value="Medium">Medium</option>
        <option value="High">High</option>
      </select>

      <label>Due Date</label>
      <input
        type="date"
        value={dueDate}
        onChange={(e) => setDueDate(e.target.value)}
      />

      <label>Category</label>
      <select value={categoryId} onChange={(e) => setCategoryId(e.target.value)}>
        <option value="">None</option>
        {categories.map(cat => (
          <option key={cat.id} value={cat.id}>{cat.name}</option>
        ))}
      </select>

      <div className="form-buttons">
        <button type="submit">Save</button>
        <button type="button" onClick={onCancel}>Cancel</button>
      </div>
    </form>
  );
};

export default TaskForm;
