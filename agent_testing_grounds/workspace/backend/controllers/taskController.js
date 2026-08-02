const { Task } = require('../models');

exports.getTasks = async (req, res) => {
  try {
    const { userId, status, priority, categoryId, search } = req.query;
    if (!userId) {
      return res.status(400).json({ message: 'User ID is required' });
    }

    let filter = { userId };

    if (status) {
      filter.status = status;
    }
    if (priority) {
      filter.priority = priority;
    }
    if (categoryId) {
      filter.categoryId = categoryId;
    }
    if (search) {
      filter.title = { $like: `%${search}%` };
    }

    const tasks = await Task.findAll({ where: filter, order: [['dueDate', 'ASC']] });
    res.json(tasks);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

exports.createTask = async (req, res) => {
  try {
    const { title, description, status, priority, dueDate, userId, categoryId } = req.body;
    if (!title || !userId) {
      return res.status(400).json({ message: 'Title and User ID are required' });
    }

    const newTask = await Task.create({ title, description, status, priority, dueDate, userId, categoryId });
    res.status(201).json(newTask);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

exports.updateTask = async (req, res) => {
  try {
    const taskId = req.params.id;
    const { title, description, status, priority, dueDate, categoryId } = req.body;

    const task = await Task.findByPk(taskId);
    if (!task) {
      return res.status(404).json({ message: 'Task not found' });
    }

    task.title = title || task.title;
    task.description = description || task.description;
    task.status = status || task.status;
    task.priority = priority || task.priority;
    task.dueDate = dueDate || task.dueDate;
    task.categoryId = categoryId || task.categoryId;

    await task.save();
    res.json(task);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

exports.deleteTask = async (req, res) => {
  try {
    const taskId = req.params.id;
    const task = await Task.findByPk(taskId);
    if (!task) {
      return res.status(404).json({ message: 'Task not found' });
    }

    await task.destroy();
    res.json({ message: 'Task deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};
