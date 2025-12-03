import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useLocation } from "react-router-dom";
import "./App.css";
import axios from "axios";

import CustomerUI from "./UIs/CustomerUI";
import CashierUI from "./UIs/CashierUI";
import KitchenUI from "./UIs/KitchenUI";
import ManagerUI from "./UIs/ManagerUI";

interface ApiResponse {
  message: string;
  status: string;
}

// Home page component
function HomePage() {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem'
    }}>
      <div style={{
        textAlign: 'center',
        color: 'white',
        maxWidth: '900px',
        width: '100%'
      }}>
        <h1 style={{
          fontSize: '3.75rem',
          fontWeight: 'bold',
          marginBottom: '1rem',
          color: 'black'
        }}>🍔 Fast Food Ordering System</h1>
        <p style={{
          fontSize: '1.5rem',
          marginBottom: '3rem',
          color: 'black'
        }}>Select your role to get started</p>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '2rem',
          maxWidth: '800px',
          margin: '0 auto'
        }}>
          <Link
            to="/customer"
            style={{
              backgroundColor: 'lightgray',
              color: 'black',
              padding: '1.5rem 2rem',
              borderRadius: '1rem',
              fontSize: '1.25rem',
              fontWeight: 'bold',
              textDecoration: 'none',
              boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
              transition: 'all 0.2s ease',
              display: 'block'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'gray';
              e.currentTarget.style.transform = 'scale(1.05)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'lightgray';
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            Customer UI
          </Link>
          <Link
            to="/cashier"
            style={{
              backgroundColor: 'lightgray',
              color: 'black',
              padding: '1.5rem 2rem',
              borderRadius: '1rem',
              fontSize: '1.25rem',
              fontWeight: 'bold',
              textDecoration: 'none',
              boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
              transition: 'all 0.2s ease',
              display: 'block'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'gray';
              e.currentTarget.style.transform = 'scale(1.05)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'lightgray';
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            Cashier UI
          </Link>
          <Link
            to="/kitchen"
            style={{
              backgroundColor: 'lightgray',
              color: 'black',
              padding: '1.5rem 2rem',
              borderRadius: '1rem',
              fontSize: '1.25rem',
              fontWeight: 'bold',
              textDecoration: 'none',
              boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
              transition: 'all 0.2s ease',
              display: 'block'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'gray';
              e.currentTarget.style.transform = 'scale(1.05)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'lightgray';
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            Kitchen UI
          </Link>
          <Link
            to="/manager"
            style={{
              backgroundColor: 'lightgray',
              color: 'black',
              padding: '1.5rem 2rem',
              borderRadius: '1rem',
              fontSize: '1.25rem',
              fontWeight: 'bold',
              textDecoration: 'none',
              boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
              transition: 'all 0.2s ease',
              display: 'block'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'gray';
              e.currentTarget.style.transform = 'scale(1.05)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'lightgray';
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            Manager UI
          </Link>
        </div>
      </div>
    </div>
  );
}

// App header component
function AppHeader() {
  const location = useLocation();
  const [apiStatus, setApiStatus] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [isConnected, setIsConnected] = useState<boolean | null>(null);

  useEffect(() => {
    // Test API connection
    const testConnection = async () => {
      setLoading(true);
      try {
        const response = await axios.get<ApiResponse>("/api/test");
        setApiStatus(response.data.message);
        setIsConnected(true);
      } catch (error) {
        setApiStatus("Backend not connected");
        setIsConnected(false);
        console.error("API Error:", error);
      } finally {
        setLoading(false);
      }
    };

    testConnection();
  }, []);

  // Don't show header on home page
  if (location.pathname === "/") {
    return null;
  }

  return (
    <header className="App-header">
      <div className="w-full max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between">
          <Link 
            to="/" 
            style={{
              color: 'white',
              textDecoration: 'none',
              fontSize: '1.25rem',
              fontWeight: '600',
              padding: '0.5rem 1rem',
              borderRadius: '0.5rem',
              transition: 'all 0.2s ease'
            }}
          >
            ← Back to Home
          </Link>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            marginLeft: '20px',
            fontSize: '0.875rem',
            color: "black"
          }}>
            {loading ? (
              <span>Checking...</span>
            ) : (
              <>
                <span>{apiStatus || "Checking..."}</span>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <AppHeader />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/customer" element={<CustomerUI />} />
            <Route path="/cashier" element={<CashierUI />} />
            <Route path="/kitchen" element={<KitchenUI />} />
            <Route path="/manager" element={<ManagerUI />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
