import React from 'react';
import './CategoryList.css';

const CategoryList = ({ categories, onSelectCategory }) => {
  return (
    <ul className="category-list">
      {categories.map(category => (
        <li key={category.id} onClick={() => onSelectCategory(category.id)}>
          {category.name}
        </li>
      ))}
    </ul>
  );
};

export default CategoryList;
