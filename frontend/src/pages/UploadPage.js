import React, { useState, useEffect } from 'react';
import '../App.css';

function UploadPage() {
  const [file, setFile] = useState(null);
  const [year, setYear] = useState('');
  const [existingYears, setExistingYears] = useState([]);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'success' vagy 'error'

  useEffect(() => {
    fetch('http://localhost:8000/filters')
      .then(res => res.json())
      .then(data => setExistingYears(data.years || []))
      .catch(err => {
        console.error('Hiba az évek lekérésénél:', err);
        setMessage('Nem sikerült lekérni a már feltöltött éveket.');
        setMessageType('error');
      });
  }, []);

  const handleUpload = async () => {
    if (!file || !year) {
      setMessage('Tölts fel egy fájlt és adj meg egy évet!');
      setMessageType('error');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('year', year);

    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await res.json();

      if (res.ok && result.message) {
        setMessage(result.message);
        setMessageType('success');
        setExistingYears(prev => [...prev, year]);
      } else if (result.detail) {
        setMessage(result.detail);
        setMessageType('error');
      } else {
        setMessage('Ismeretlen hiba.');
        setMessageType('error');
      }
    } catch (err) {
      setMessage('Hálózati hiba: ' + err.message);
      setMessageType('error');
    }
  };

  return (
    <div className="upload-container">
      <h2>Új JSON feltöltése</h2>

      <input type="file" accept=".json" onChange={(e) => setFile(e.target.files[0])} />
      <input
        type="number"
        placeholder="Év (pl. 2023)"
        value={year}
        onChange={(e) => setYear(e.target.value)}
      />
      <button onClick={handleUpload}>Feltöltés</button>

      {message && (
        <p className={messageType === 'success' ? 'message success' : 'message error'}>
          {message}
        </p>
      )}

      <h3>Már feltöltött évek:</h3>
      <ul>
        {existingYears.map((y, i) => <li key={i}>{y}</li>)}
      </ul>
    </div>
  );
}

export default UploadPage;
