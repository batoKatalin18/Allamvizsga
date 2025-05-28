import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      const response = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query)}`);
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Hiba a keresés során:', error);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>TDK Keresés</h1>
      <input
        type="text"
        placeholder="Írd be a keresett nevet vagy címet..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ padding: '0.5rem', width: '300px', marginRight: '1rem' }}
      />
      <button onClick={handleSearch} style={{ padding: '0.5rem 1rem' }}>Keresés</button>

      <ul style={{ marginTop: '2rem' }}>
        {results.map((item, index) => (
          <li key={index} style={{ marginBottom: '1rem' }}>
            <strong>{item.title}</strong>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
