// src/components/PapersPerYearChart.js
import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid, ResponsiveContainer } from 'recharts';
import axios from 'axios';

const PapersPerYearChart = () => {
  const [yearData, setYearData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/papers-per-year')
      .then(response => {
        console.log("Kapott év-adatok:", response.data);
        setYearData(response.data);
        
      })
      .catch(error => {
        console.error("Hiba az adatok betöltésekor:", error);
      });
  }, []);

  return (
    <div className="stats-container">
      <h2>📊 Statisztikák</h2>

      <section>
        <h3>Dolgozatok száma évente</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={yearData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </section>
    </div>
  );
};

export default PapersPerYearChart;
