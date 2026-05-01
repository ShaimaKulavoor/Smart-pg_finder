import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

export const Header = () => {
  const { isAuthenticated, user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setMobileMenuOpen(false);
  };

  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-2xl font-bold hover:opacity-90 transition"
        >
          <span className="text-3xl">🏠</span>
          <span>Smart PG</span>
        </button>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-8">
          {isAuthenticated && (
            <span className="text-sm opacity-90">Welcome, {user?.username}!</span>
          )}
          {isAuthenticated ? (
            <>
              <button
                onClick={() => navigate('/')}
                className="hover:opacity-80 transition"
              >
                Home
              </button>
              <button
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg transition font-semibold"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => navigate('/login')}
                className="hover:opacity-80 transition"
              >
                Login
              </button>
              <button
                onClick={() => navigate('/register')}
                className="bg-white text-blue-600 px-4 py-2 rounded-lg font-semibold hover:bg-gray-100 transition"
              >
                Register
              </button>
            </>
          )}
        </nav>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden text-2xl"
        >
          ☰
        </button>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-blue-700 px-4 py-4 space-y-2">
          {isAuthenticated ? (
            <>
              <button
                onClick={() => {
                  navigate('/');
                  setMobileMenuOpen(false);
                }}
                className="block w-full text-left py-2 hover:opacity-80"
              >
                Home
              </button>
              <button
                onClick={handleLogout}
                className="block w-full text-left py-2 bg-red-500 rounded px-3 font-semibold"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => {
                  navigate('/login');
                  setMobileMenuOpen(false);
                }}
                className="block w-full text-left py-2 hover:opacity-80"
              >
                Login
              </button>
              <button
                onClick={() => {
                  navigate('/register');
                  setMobileMenuOpen(false);
                }}
                className="block w-full text-left py-2 bg-white text-blue-600 rounded px-3 font-semibold"
              >
                Register
              </button>
            </>
          )}
        </div>
      )}
    </header>
  );
};

export const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-300 py-12 mt-16">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <h4 className="text-white font-bold mb-4 flex items-center gap-2 text-lg">
              <span className="text-2xl">🏠</span> Smart PG
            </h4>
            <p className="text-sm opacity-80">
              Find your perfect PG with AI-powered recommendations and smart filtering
            </p>
          </div>
          <div>
            <h4 className="text-white font-bold mb-4">Features</h4>
            <ul className="space-y-2 text-sm opacity-80">
              <li className="flex items-center gap-2">✨ Smart Recommendations</li>
              <li className="flex items-center gap-2">💬 AI Chatbot Assistant</li>
              <li className="flex items-center gap-2">❤️ Save Favorites</li>
              <li className="flex items-center gap-2">🔍 Advanced Filtering</li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-bold mb-4">Get in Touch</h4>
            <ul className="space-y-2 text-sm opacity-80">
              <li>📧 support@smartpg.com</li>
              <li>📱 +91-XXXXX-XXXXX</li>
              <li>📍 Serving All Major Indian Cities</li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-700 pt-8 text-center text-sm opacity-70">
          <p>&copy; 2024 Smart PG Finder. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};
