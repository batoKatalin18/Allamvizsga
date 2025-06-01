import React from 'react';
import '../App.css';

const FilterPanel = ({ filters, majors, years, onChange }) => (
  <aside className="filters">
    <h3>Szűrés</h3>

    <label>Szakosztály:</label>
    <select name="major" value={filters.major} onChange={onChange}>
      <option value="">Összes</option>
      {majors.map((m, i) => <option key={i} value={m}>{m}</option>)}
    </select>

    <label>Év:</label>
    <select name="year" value={filters.year} onChange={onChange}>
      <option value="">Összes</option>
      {years.map((y, i) => <option key={i} value={y}>{y}</option>)}
    </select>

    <label>Cím:</label>
    <input name="title" value={filters.title} onChange={onChange} />

    <label>Diák:</label>
    <input name="student" value={filters.student} onChange={onChange} />

    <label>Tanár:</label>
    <input name="teacher" value={filters.teacher} onChange={onChange} />
  </aside>
);

export default FilterPanel;
