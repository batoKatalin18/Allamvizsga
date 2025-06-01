// src/pages/StatisticsPage.js
import React, { useEffect, useState } from 'react';
import {
  BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#FF6384', '#36A2EB'];

function StatisticsPage() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/stats')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error('Hiba a statisztikák lekérésekor:', err));
  }, []);

  if (!stats) return <p>Statisztikák betöltése...</p>;

  // Adat átalakítás Recharts formára
  const yearData = Object.entries(stats.papers_per_year).map(([year, count]) => ({ year, count }));
  const majorData = Object.entries(stats.majors_distribution).map(([major, count]) => ({ name: major, value: count }));
  const teacherData = Object.entries(stats.top_teachers).map(([name, count]) => ({ name, count }));
  const keywordData = Object.entries(stats.top_keywords).map(([word, count]) => ({ name: word, count }));

  return (
    <div className="stats-container">
      <h2>📊 Statisztikák</h2>

      <section>
        <h3>Dolgozatok száma évente</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={yearData}>
            <XAxis dataKey="year" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </section>

      <section>
        <h3>Szakirányok megoszlása</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={majorData}
              dataKey="value"
              nameKey="name"
              outerRadius={100}
              fill="#82ca9d"
              label
            >
              {majorData.map((entry, index) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </section>

      <section>
        <h3>Legaktívabb tanárok</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={teacherData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#ff7300" />
          </BarChart>
        </ResponsiveContainer>
      </section>

      <section>
        <h3>Leggyakoribb kulcsszavak</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={keywordData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#00c49f" />
          </BarChart>
        </ResponsiveContainer>
      </section>
    </div>
  );
}

export default StatisticsPage;
