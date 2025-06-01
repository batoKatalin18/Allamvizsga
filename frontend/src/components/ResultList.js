import React from 'react';
import '../App.css';

const ResultList = ({ results, expandedItems, toggleItem }) => (
  <main className="results">
    {results.length > 0 && (
      <div className="results-count">
        <strong>Találatok száma:</strong> {results.length}
      </div>
    )}

    {results.length > 0 ? (
      results.map((item, index) => {
        const isExpanded = expandedItems.has(index);
        return (
          <div
            key={index}
            className="result-card"
            onClick={() => toggleItem(index)}
            style={{ cursor: 'pointer', backgroundColor: isExpanded ? '#f9f9f9' : 'white' }}
          >
            <h3>{item.title}</h3>
            <p><strong>Év:</strong> {item.year}</p>
            {isExpanded && (
              <div className="details">
                <p><strong>Diák(ok):</strong> {item.students?.map(s => s.name).join(', ')}</p>
                <p><strong>Tanár(ok):</strong> {item.teachers?.map(t => t.name).join(', ')}</p>
                <p><strong>Kivonat:</strong> {item.content}</p>
              </div>
            )}
          </div>
        );
      })
    ) : (
      <p>Nincsenek találatok.</p>
    )}
  </main>
);

export default ResultList;
