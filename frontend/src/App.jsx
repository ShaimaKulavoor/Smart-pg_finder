import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Header, Footer } from './components/Layout';
import { ChatBot } from './components/ChatBot';
import { PrivateRoute } from './components/PrivateRoute';
import { HomePage } from './pages/HomePage';
import { ResultsPage } from './pages/ResultsPage';
import { DetailsPage } from './pages/DetailsPage';
import { LoginPage, RegisterPage } from './pages/AuthPages';
import './index.css';

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="container-app flex flex-col min-h-screen">
          <Header />

          <main className="flex-grow">
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<HomePage />} />
              <Route path="/results" element={<ResultsPage />} />
              <Route path="/pg/:pgId" element={<DetailsPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />

              {/* Catch all */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>

          <Footer />

          {/* Global Chatbot */}
          <ChatBot />
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
