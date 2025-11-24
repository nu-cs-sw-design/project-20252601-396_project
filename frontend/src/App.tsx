import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import axios from "axios";

import CustomerUI from "./pages/CustomerUI";
import CashierUI from "./pages/CashierUI";
import KitchenUI from "./pages/KitchenUI";
import ManagerUI from "./pages/ManagerUI";

interface ApiResponse {
  message: string;
  status: string;
}

function App() {
  const [apiStatus, setApiStatus] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    // Test API connection
    const testConnection = async () => {
      setLoading(true);
      try {
        const response = await axios.get<ApiResponse>("/api/test");
        setApiStatus(response.data.message);
      } catch (error) {
        setApiStatus("Failed to connect to backend API");
        console.error("API Error:", error);
      } finally {
        setLoading(false);
      }
    };

    testConnection();
  }, []);

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <p>🍔</p>
          <div>
            <Link to="/customer" style={{ padding: "1rem" }}>
              Customer UI
            </Link>
            <Link to="/cashier" className="inline-block px-4 py-2">
              Cashier UI
            </Link>
            <Link to="/kitchen" className="inline-block px-4 py-2">
              Kitchen UI
            </Link>
            <Link to="/manager" className="inline-block px-4 py-2">
              Manager UI
            </Link>
          </div>

          {loading ? (
            <p className="text-xs">Loading...</p>
          ) : (
            <p className="text-xs">
              Backend Status: {apiStatus || "Checking..."}
            </p>
          )}
          <p className="text-xs">React Frontend + Flask Backend</p>
        </header>
        <main>
          <Routes>
            <Route path="/customer" element={<CustomerUI />} />
            <Route path="/cashier" element={<CashierUI />} />
            <Route path="/kitchen" element={<KitchenUI />} />
            <Route path="/manager" element={<ManagerUI />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
