import React, { useState, useEffect } from 'react';
import '../App.css';

function UploadPage() {
  const [file, setFile] = useState(null);
  const [year, setYear] = useState('');
  const [existingYears, setExistingYears] = useState([]);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Bejelentkezéshez szükséges state-ek
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');

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

    setIsLoading(true);
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
    } catch (error) {
      console.error('Hiba feltöltéskor:', error);
      setMessage('Hiba történt a feltöltés során.');
      setMessageType('error');
    } finally {
      setIsLoading(false);
    }
  };

const handleLogin = async () => {
  setLoginError('');
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  try {
    const res = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData.toString(),
    });

    const data = await res.json();

    if (data.success) {
      setIsAuthenticated(true);
    } else {
      setLoginError(data.detail || 'Sikertelen bejelentkezés.');
    }
  } catch (err) {
    console.error('Bejelentkezési hiba:', err);
    setLoginError('Hiba történt a bejelentkezés során.');
  }
};


  if (!isAuthenticated) {
    return (
      <div className="login-wrapper">
        <div className="login-box">
          <h2>Bejelentkezés</h2>
          <input
            type="text"
            placeholder="Felhasználónév"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Jelszó"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleLogin}>Bejelentkezés</button>
          {loginError && <p className="login-error">{loginError}</p>}
        </div>
      </div>
    );
  }

  return (
    <div className="upload-layout">
      <div className="left-column">
        <div className="upload-form">
          <h2>Fájl feltöltése</h2>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <input
            type="text"
            placeholder="Év"
            value={year}
            onChange={(e) => setYear(e.target.value)}
          />
          <button onClick={handleUpload}>Feltöltés</button>
          {isLoading && <div className="spinner" />}
          {message && (
            <p className={messageType === 'success' ? 'success-message' : 'error-message'}>
              {message}
            </p>
          )}
        </div>
        <div className="existing-years">
          <h3>Már feltöltött évek</h3>
          <ul>
            {existingYears.map((y, index) => (
              <li key={index}>{y}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="right-column">
        <div className="json-sample">
          <h3>JSON példa</h3>
          <pre>
{`{
  "major": "Informatika",
  "year": 2015,
  "title": "Dolgozat címe",
  "students": [{"name": "Név", 
                "major": "Sapientia EMTE, Informatika szak, 3. év"}],
  "teachers": [{"name": "Oktató", 
                "university": "Sapientia EMTE"}],
  "content": "Dolgozatom célja ... ",
  "keywords": ["kulcsszó1", "kulcsszó2", ...],
  "generated_keywords": ["kulcsszó3", "kulcsszó4", ...]
}`}
          </pre>
        </div>
      </div>
    </div>
  );
}

export default UploadPage;
