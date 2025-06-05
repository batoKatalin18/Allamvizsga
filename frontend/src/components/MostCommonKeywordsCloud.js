// src/components/MostCommonKeywordsCloud.js
import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import * as d3 from 'd3';
import cloud from 'd3-cloud';
import '../css/MostCommonKeywordsCloud.css';

const MostCommonKeywordsCloud = () => {
  const [years, setYears] = useState([]);
  const [majors, setMajors] = useState([]);
  const [selectedYear, setSelectedYear] = useState('');
  const [selectedMajor, setSelectedMajor] = useState('');
  const [keywords, setKeywords] = useState([]);
  const svgRef = useRef();

  useEffect(() => {
    axios.get('http://localhost:8000/api/available-years')
      .then(res => {
        const yearList = ['all', ...res.data];
        setYears(yearList);
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
        .catch(() => {
          setMajors([]);
          setSelectedMajor('all');
        });
    } else {
      setMajors([]);
      setSelectedMajor('all');
    }
  }, [selectedYear]);

  useEffect(() => {
    if (selectedYear) {
      let url = `http://localhost:8000/api/most-common-keywords?year=${selectedYear}`;
      if (selectedMajor !== 'all') {
        url += `&major=${encodeURIComponent(selectedMajor)}`;
      }

      axios.get(url)
        .then(res => setKeywords(res.data));
    }
  }, [selectedYear, selectedMajor]);

  useEffect(() => {
  if (keywords.length > 0) {
    const colors = ["#ea5545", "#f46a9b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6", "#ef9b20", "#edbf33", "#ede15b"];

    const layout = cloud()
      .size([600, 400])
      .words(keywords.map(d => ({ text: d.text, size: 10 + d.value * 3 })))
      .padding(5)
      .rotate(() => ~~(Math.random() * 2) * 90)
      .font('Impact')
      .fontSize(d => d.size)
      .on('end', draw);

    layout.start();

    function draw(words) {
      const svg = d3.select(svgRef.current);
      svg.selectAll('*').remove();

      svg
        .attr('width', 600)
        .attr('height', 400)
        .append('g')
        .attr('transform', 'translate(300,200)')
        .selectAll('text')
        .data(words)
        .enter()
        .append('text')
        .style('font-size', d => `${d.size}px`)
        .style('font-family', 'Impact')
        .style('fill', () => colors[Math.floor(Math.random() * colors.length)])
        .attr('text-anchor', 'middle')
        .attr('transform', d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
        .text(d => d.text);
    }
  }
}, [keywords]);


return (
  <div className="stats-container">
    <h3>Leggyakoribb kulcsszavak</h3>

    <div className="dropdown-group">
      <label>Válassz évet:</label>
      <select value={selectedYear} onChange={e => setSelectedYear(e.target.value)}>
        {years.map(year => (
          <option key={year} value={year}>{year === 'all' ? 'Összes év' : year}</option>
        ))}
      </select>

      {selectedYear !== 'all' && (
        <>
          <label>Válassz szakot:</label>
          <select value={selectedMajor} onChange={e => setSelectedMajor(e.target.value)}>
            {majors.map(m => (
              <option key={m} value={m}>{m === 'all' ? 'Összes szak' : m}</option>
            ))}
          </select>
        </>
      )}
    </div>

    <div className="wordcloud-svg">
      <svg ref={svgRef}></svg>
    </div>
  </div>
);

};

export default MostCommonKeywordsCloud;
