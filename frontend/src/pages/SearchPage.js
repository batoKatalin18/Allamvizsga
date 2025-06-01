// src/pages/SearchPage.js
import React, { useState, useEffect } from 'react';
import SearchBar from '../components/SearchBar';
import FilterPanel from '../components/FilterPanel';
import ResultList from '../components/ResultList';
import '../App.css';


const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState({
    major: '',
    year: '',
    title: '',
    student: '',
    teacher: ''
  });
  const [results, setResults] = useState([]);
  const [years, setYears] = useState([]);
  const [majors, setMajors] = useState([]);
  const [expandedItems, setExpandedItems] = useState(new Set());

  useEffect(() => {
    fetch('http://localhost:8000/filters')
      .then(response => response.json())
      .then(data => {
        setYears(data.years || []);
        setMajors(data.majors || []);
      })
      .catch(error => console.error('Hiba a filterek lekérdezésekor:', error));
  }, []);

  const handleSearch = async () => {
    try {
      const params = new URLSearchParams();
      if (query.trim() !== '') params.append('query', query.trim());

      Object.entries(filters).forEach(([key, value]) => {
        if (value.trim() !== '') params.append(key, value.trim());
      });

      const response = await fetch(`http://localhost:8000/search?${params.toString()}`);
      const data = await response.json();
      setResults(data);
      setExpandedItems(new Set());
    } catch (error) {
      console.error('Hiba a keresés során:', error);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const toggleItem = (index) => {
    setExpandedItems(prev => {
      const newSet = new Set(prev);
      if (newSet.has(index)) {
        newSet.delete(index);
      } else {
        newSet.add(index);
      }
      return newSet;
    });
  };

  return (
    <>
      <SearchBar query={query} setQuery={setQuery} onSearch={handleSearch} />
      <div className="content">
        <FilterPanel
          filters={filters}
          majors={majors}
          years={years}
          onChange={handleFilterChange}
        />
        <ResultList
          results={results}
          expandedItems={expandedItems}
          toggleItem={toggleItem}
        />
      </div>
    </>
  );
};

export default SearchPage;
