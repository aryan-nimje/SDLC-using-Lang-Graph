const User = require('./userModel');
const Task = require('./taskModel');
const Category = require('./categoryModel');

// Associations
User.hasMany(Task, { foreignKey: 'userId', onDelete: 'CASCADE' });
Task.belongsTo(User, { foreignKey: 'userId' });

User.hasMany(Category, { foreignKey: 'userId', onDelete: 'CASCADE' });
Category.belongsTo(User, { foreignKey: 'userId' });

Category.hasMany(Task, { foreignKey: 'categoryId', onDelete: 'SET NULL' });
Task.belongsTo(Category, { foreignKey: 'categoryId' });

module.exports = {
  User,
  Task,
  Category
};
