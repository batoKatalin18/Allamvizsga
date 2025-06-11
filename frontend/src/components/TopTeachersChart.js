import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';


const TopTeachersChart = () => {
  const [years, setYears] = useState([]);
  const [majors, setMajors] = useState([]);
  const [selectedYear, setSelectedYear] = useState('');
  const [selectedMajor, setSelectedMajor] = useState('');
  const [teacherData, setTeacherData] = useState([]);

useEffect(() => {
  axios.get('http://localhost:8000/api/available-years')
    .then(res => {
      const yearsList = ['all', ...res.data];
      setYears(yearsList);
      setSelectedYear('all');
    });
}, []);

useEffect(() => {
  if (selectedYear !== 'all') {
    axios.get(`http://localhost:8000/api/majors-by-year?year=${selectedYear}`)
      .then(res => {
        const majorList = ['all', ...res.data.map(m => m.name)];
        setMajors(majorList);
        setSelectedMajor('all');
      })
      .catch(error => {
        console.error("Hiba a major lekérdezésekor:", error);
        setMajors([]);
        setSelectedMajor('all');
      });
  } else {
    // year = 'all' esetén nincs major dropdown
    setMajors([]);
    setSelectedMajor('all');
  }
}, [selectedYear]);



useEffect(() => {
  if (selectedYear) {
    if (selectedYear === 'all') {
      axios.get(`http://localhost:8000/api/top-teachers?year=all`)
        .then(res => setTeacherData(res.data));
    } else if (selectedMajor === 'all') {
      axios.get(`http://localhost:8000/api/top-teachers?year=${selectedYear}`)
        .then(res => setTeacherData(res.data));
    } else {
      axios.get(`http://localhost:8000/api/top-teachers?year=${selectedYear}&major=${encodeURIComponent(selectedMajor)}`)
        .then(res => setTeacherData(res.data));
    }
  }
}, [selectedYear, selectedMajor]);


return (
  <div className="stats-container">
    <h3>Legaktívabb tanárok</h3>

    <div className="dropdown-group">
      <label>Válassz évet:</label>
      <select value={selectedYear} onChange={e => setSelectedYear(e.target.value)}>
        {years.map(year => (
          <option key={year} value={year}>
            {year === 'all' ? 'Összes év' : year}
          </option>
        ))}
      </select>

      {selectedYear !== 'all' && (
        <>
          <label>Válassz szakot:</label>
          <select value={selectedMajor} onChange={e => setSelectedMajor(e.target.value)}>
            {majors.map(m => (
              <option key={m} value={m}>
                {m === 'all' ? 'Összes szak' : m}
              </option>
            ))}
          </select>
        </>
      )}
    </div>

    {teacherData.length > 0 ? (
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={teacherData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" angle={-30} textAnchor="end" interval={0} height={100} />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#f589b0" />
        </BarChart>
      </ResponsiveContainer>
    ) : (
      <p>Nincs adat a kiválasztott évre és szakra.</p>
    )}
  </div>
);

};

export default TopTeachersChart;
