// src/components/MajorsPerYearChart.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { PieChart, Pie, Tooltip, Cell, ResponsiveContainer, Legend } from 'recharts';
import '../css/MajorsPerYearChart.css';


const COLORS = ["#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6","#f46a9b"];

const MajorsPerYearChart = () => {
  const [years, setYears] = useState([]);
  const [selectedYear, setSelectedYear] = useState(null);
  const [majorData, setMajorData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/available-years')
      .then(res => {
        setYears(res.data);
        if (res.data.length > 0) {
          setSelectedYear(res.data[0]);  // default to first year
        }
      })
      .catch(err => console.error('Hiba az évek lekérésekor:', err));
  }, []);

  useEffect(() => {
    if (selectedYear) {
      axios.get(`http://localhost:8000/api/majors-by-year?year=${selectedYear}`)
        .then(res => setMajorData(res.data))
        .catch(err => console.error('Hiba a szakosztályadatok lekérésekor:', err));
    }
  }, [selectedYear]);

  return (
    <div className="stats-container">
      <h3>Szakosztályok dolgozatai évente</h3>

      <label htmlFor="year-select">Válassz évet:</label>
      <select id="year-select" onChange={e => setSelectedYear(e.target.value)} value={selectedYear}>
        {years.map(year => (
          <option key={year} value={year}>{year}</option>
        ))}
      </select>

      {majorData.length > 0 ? (
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={majorData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={100}
              fill="#8884d8"
              label
            >
              {majorData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend verticalAlign="bottom" height={36} />
          </PieChart>
        </ResponsiveContainer>
      ) : (
        <p>Nincs adat az adott évre.</p>
      )}
    </div>
  );
};

export default MajorsPerYearChart;
