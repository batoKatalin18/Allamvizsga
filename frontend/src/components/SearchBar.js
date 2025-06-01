import React from 'react';
import '../App.css';

const SearchBar = ({ query, setQuery, onSearch }) => (
  <div className="search-bar">
    <input
      type="text"
      placeholder="Keresés kulcsszóra, címre, tartalomra..."
      value={query}
      onChange={(e) => setQuery(e.target.value)}
    />
    <button onClick={onSearch}>Keresés</button>
  </div>
);

export default SearchBar;
