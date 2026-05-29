import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { recommendationAPI } from '../api/api';

export const HomePage = () => {
  const navigate = useNavigate();
  
  // Fallback cities list in case API fails
  const fallbackCities = ['Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai'];
  
  const [cities, setCities] = useState(fallbackCities);
  const [city, setCity] = useState('Bangalore');
  const [budget, setBudget] = useState(15000);
  const [tenantType, setTenantType] = useState('Any');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [moveIn, setMoveIn] = useState('');
  const [moveOut, setMoveOut] = useState('');
  const [guests, setGuests] = useState(1);

  useEffect(() => {
    fetchCities();
  }, []);

  const fetchCities = async () => {
    try {
      const response = await recommendationAPI.getCities();
      if (response.data && response.data.cities && Array.isArray(response.data.cities)) {
        setCities(response.data.cities);
        // Set first city as default if available
        if (response.data.cities.length > 0 && !response.data.cities.includes('Bangalore')) {
          setCity(response.data.cities[0]);
        }
      }
    } catch (err) {
      console.error('Error fetching cities:', err);
      // Fallback cities already set in state
    }
  };

  const handleGetRecommendations = async (e) => {
    e.preventDefault();
    
    // Validate form
    if (!city) {
      setError('Please select a city');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Don't pass tenant_type if it's 'Any' - let backend return all
      const queryTenantType = tenantType && tenantType !== 'Any' ? tenantType : undefined;
      
      const response = await recommendationAPI.getRecommendations(
        city,
        budget,
        queryTenantType,
        null,
        10
      );

      if (response.data.status === 'success') {
        if (response.data.recommendations && response.data.recommendations.length > 0) {
          // Navigate to results page with data
          navigate('/results', {
            state: {
              recommendations: response.data.recommendations,
              filters: {
                city,
                budget,
                tenantType,
                moveIn,
                moveOut,
                guests,
              },
            },
          });
        } else {
          setError('No PGs found matching your criteria. Try adjusting your filters.');
        }
      } else {
        setError('No recommendations found. Try adjusting your filters.');
      }
    } catch (err) {
      console.error('Error fetching recommendations:', err);
      setError(
        err.response?.data?.message || 
        'Failed to fetch recommendations. Please check the backend is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-12">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-3 mb-4">
            <span className="text-4xl">🏠</span>
            <h1 className="text-4xl font-bold">Smart PG Finder</h1>
          </div>
          <p className="text-xl opacity-90">AI-powered recommendations for your perfect PG</p>
        </div>
      </div>

      {/* Search Form */}
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="bg-white rounded-lg shadow-2xl p-8">
          <form onSubmit={handleGetRecommendations} className="space-y-6">
            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border-l-4 border-red-500 p-4 text-red-700">
                <p className="font-semibold">⚠️ {error}</p>
              </div>
            )}

            {/* Main Search Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* City Selector */}
              <div>
                <label className="block text-gray-700 font-semibold mb-2">📍 City</label>
                <select
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent bg-white"
                >
                  {cities && cities.length > 0 ? (
                    cities.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))
                  ) : (
                    <option value="">No cities available</option>
                  )}
                </select>
              </div>

              {/* Budget Slider */}
              <div>
                <label className="block text-gray-700 font-semibold mb-2">
                  💰 Budget: ₹{budget.toLocaleString()}
                </label>
                <input
                  type="range"
                  min="5000"
                  max="100000"
                  step="1000"
                  value={budget}
                  onChange={(e) => setBudget(parseInt(e.target.value))}
                  className="w-full h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer accent-blue-600"
                />
                <div className="flex justify-between text-xs text-gray-600 mt-1">
                  <span>₹5K</span>
                  <span>₹100K</span>
                </div>
              </div>

              {/* Tenant Type */}
              <div>
                <label className="block text-gray-700 font-semibold mb-2">👥 Tenant Type</label>
                <select
                  value={tenantType}
                  onChange={(e) => setTenantType(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                >
                  <option value="Any">Any</option>
                  <option value="Bachelors">Bachelors</option>
                  <option value="Family">Family</option>
                  <option value="Bachelors/Family">Bachelors/Family</option>
                </select>
              </div>
            </div>

            {/* Additional Information Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Move-in Date */}
              <div>
                <label className="block text-gray-700 font-semibold mb-2">📅 Move-in Date</label>
                <input
                  type="date"
                  value={moveIn}
                  onChange={(e) => setMoveIn(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                />
              </div>

              {/* Move-out Date */}
              <div>
                <label className="block text-gray-700 font-semibold mb-2">📅 Move-out Date</label>
                <input
                  type="date"
                  value={moveOut}
                  onChange={(e) => setMoveOut(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                />
              </div>

              {/* Guests */}
              <div>
                <label className="block text-gray-700 font-semibold mb-2">👤 Number of Guests</label>
                <div className="flex items-center border-2 border-gray-300 rounded-lg">
                  <button
                    type="button"
                    onClick={() => setGuests(Math.max(1, guests - 1))}
                    className="px-4 py-3 text-lg font-semibold text-blue-600 hover:bg-blue-50"
                  >
                    −
                  </button>
                  <input
                    type="number"
                    value={guests}
                    onChange={(e) => setGuests(Math.max(1, parseInt(e.target.value) || 1))}
                    className="flex-1 text-center py-3 focus:outline-none"
                    min="1"
                  />
                  <button
                    type="button"
                    onClick={() => setGuests(guests + 1)}
                    className="px-4 py-3 text-lg font-semibold text-blue-600 hover:bg-blue-50"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || !city}
              className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white font-bold text-lg py-4 rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
            >
              {loading ? '🔍 Searching...' : '🔍 Get Recommendations'}
            </button>
          </form>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white rounded-lg shadow-lg p-6 text-center">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="font-bold text-xl text-gray-900 mb-2">AI-Powered</h3>
            <p className="text-gray-600">
              Smart recommendations based on your preferences and similar properties
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 text-center">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="font-bold text-xl text-gray-900 mb-2">Instant Results</h3>
            <p className="text-gray-600">
              Get recommendations in seconds using advanced ML algorithms
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 text-center">
            <div className="text-4xl mb-4">💼</div>
            <h3 className="font-bold text-xl text-gray-900 mb-2">Save Favorites</h3>
            <p className="text-gray-600">
              Create an account to save your favorite PGs and get notified
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
