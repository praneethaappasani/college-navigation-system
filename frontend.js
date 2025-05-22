import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [locations, setLocations] = useState([]);
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  const [path, setPath] = useState([]);
  const [cost, setCost] = useState(0);

  useEffect(() => {
    axios.get('/locations').then(res => {
      setLocations(res.data);
    });
  }, []);

  const findPath = () => {
    axios.post('/find-path', { source, destination }).then(res => {
      setPath(res.data.path);
      setCost(res.data.cost);
    });
  };

  return (
    <div className="App">
      <h1>College Navigation System</h1>
      <div className="form">
        <label>Source:</label>
        <select onChange={e => setSource(e.target.value)}>
          <option value="">Select Source</option>
          {locations.map(loc => (
            <option key={loc.name} value={loc.name}>{loc.name}</option>
          ))}
        </select>

        <label>Destination:</label>
        <select onChange={e => setDestination(e.target.value)}>
          <option value="">Select Destination</option>
          {locations.map(loc => (
            <option key={loc.name} value={loc.name}>{loc.name}</option>
          ))}
        </select>

        <button onClick={findPath}>Find Path</button>
      </div>

      {path.length > 0 && (
        <div className="result">
          <h2>Shortest Path</h2>
          <p>{path.join(' -> ')}</p>
          <p>Cost: {cost}</p>
        </div>
      )}
    </div>
  );
}

export default App;
