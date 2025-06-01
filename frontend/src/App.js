// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import SearchPage from './pages/SearchPage';
import UploadPage from './pages/UploadPage';
import StatisticsPage from './pages/StatisticsPage';


function App() {
  return (
    <Router>
      <header className="navbar">
        <div className="navbar-title">📚 TDK Böngésző</div>
        <nav className="navbar-links">
          <Link to="/" className="nav-button">Keresés</Link>
          <Link to="/upload" className="nav-button">Feltöltés</Link>
          <Link to="/stats" className="nav-button">Statisztikák</Link>
        </nav>
      </header>
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/stats" element={<StatisticsPage />} />
      </Routes>
    </Router>
  );
}

export default App;

