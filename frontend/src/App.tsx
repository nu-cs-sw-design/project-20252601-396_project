import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

interface ApiResponse {
  message: string;
  status: string;
}

function App() {
  const [apiStatus, setApiStatus] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    // Test API connection
    const testConnection = async () => {
      setLoading(true);
      try {
        const response = await axios.get<ApiResponse>('/api/test');
        setApiStatus(response.data.message);
      } catch (error) {
        setApiStatus('Failed to connect to backend API');
        console.error('API Error:', error);
      } finally {
        setLoading(false);
      }
    };
    
    testConnection();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🍔 Fast Food Ordering System</h1>
        <p>Welcome to our ordering system!</p>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div>
            <p>Backend Status: {apiStatus || 'Checking...'}</p>
          </div>
        )}
        <p className="App-subtitle">
          React Frontend + Flask Backend
        </p>
      </header>
    </div>
  );
}

export default App;
