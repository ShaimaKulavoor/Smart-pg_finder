import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { SkeletonLoader } from '../components/Skeleton';

export const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [sortBy, setSortBy] = useState('price');

  const recommendations = location.state?.recommendations || [];
  const filters = location.state?.filters || {};

  // Sort recommendations
  const sorted = [...recommendations].sort((a, b) => {
    if (sortBy === 'price') return a.rent - b.rent;
    if (sortBy === 'rating') return b.rating - a.rating;
    if (sortBy === 'size') return b.size - a.size;
    return 0;
  });

  if (recommendations.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <button
            onClick={() => navigate('/')}
            className="mb-6 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
          >
            ← Back to Search
          </button>

          <div className="text-center py-16">
            <p className="text-2xl text-gray-600 mb-4">No recommendations found</p>
            <p className="text-gray-500 mb-8">
              Try adjusting your search filters
            </p>
            <button
              onClick={() => navigate('/')}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
            >
              Search Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/')}
            className="mb-4 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
          >
            ← Back to Search
          </button>

          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Recommended for you
            </h1>
            <p className="text-gray-600 mb-4">
              {recommendations.length} matching places found{filters.city ? ` in ${filters.city}` : ''}
            </p>

            {/* Applied Filters */}
            <div className="flex flex-wrap gap-2">
              {filters.city && (
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                  📍 {filters.city}
                </span>
              )}
              {filters.budget && (
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                  💰 Up to ₹{filters.budget}
                </span>
              )}
              {filters.tenantType && filters.tenantType !== 'Any' && (
                <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm">
                  👥 {filters.tenantType}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Sort Options */}
        <div className="mb-6 flex justify-between items-center">
          <h2 className="text-xl font-bold text-gray-900">Results</h2>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
          >
            <option value="price">Sort by: Price (Low to High)</option>
            <option value="rating">Sort by: Rating</option>
            <option value="size">Sort by: Size</option>
          </select>
        </div>

        {/* PG Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sorted.map((pg, index) => (
            <div
              key={pg.id}
              onClick={() => navigate(`/pg/${pg.id}`)}
              className="bg-white rounded-lg shadow-lg overflow-hidden cursor-pointer hover:shadow-2xl transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 animate-fadeIn"
              style={{
                animationDelay: `${index * 50}ms`,
              }}
            >
              {/* Image Container with Overlay */}
              <div className="relative group overflow-hidden h-48">
                <img
                  src={pg.image_url}
                  alt={pg.area_locality}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                  onError={(e) => {
                    e.target.src = '/images/pg/pg_placeholder_1.svg';
                  }}
                />
                {/* Overlay Gradient */}
                <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-0 group-hover:opacity-60 transition-opacity duration-300"></div>
                
                {/* Rating Badge */}
                <div className="absolute top-4 left-4 bg-white rounded-full px-3 py-1 shadow-md transition-transform duration-300 group-hover:scale-110">
                  <span className="font-bold text-yellow-500">⭐ {pg.rating}</span>
                </div>

                {/* View Details Overlay Text */}
                <div className="absolute bottom-4 left-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <p className="text-white font-semibold text-sm">👉 View Details</p>
                </div>
              </div>

              {/* Content */}
              <div className="p-5">
                <h3 className="font-bold text-lg text-gray-900 mb-1 truncate">
                  {pg.area_locality}
                </h3>
                <p className="text-gray-600 text-sm mb-4">📍 {pg.city}</p>

                {/* Price */}
                <div className="mb-4">
                  <p className="text-blue-600 font-bold text-2xl">
                    ₹{pg.rent}
                  </p>
                  <p className="text-gray-500 text-xs">/month</p>
                </div>

                {/* Details Grid */}
                <div className="grid grid-cols-3 gap-2 text-xs text-gray-600 mb-4 pb-4 border-b">
                  <div>
                    <p className="font-semibold">BHK</p>
                    <p className="text-gray-900 font-bold">{pg.bhk}</p>
                  </div>
                  <div>
                    <p className="font-semibold">Size</p>
                    <p className="text-gray-900 font-bold">{pg.size} sqft</p>
                  </div>
                  <div>
                    <p className="font-semibold">Bath</p>
                    <p className="text-gray-900 font-bold">{pg.bathroom}</p>
                  </div>
                </div>

                {/* Tags */}
                <div className="flex flex-wrap gap-1 mb-4">
                  <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full font-medium">
                    {pg.furnishing_status}
                  </span>
                  <span className="bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full font-medium">
                    {pg.tenant_preferred}
                  </span>
                </div>

                {/* View Details Button */}
                <button className="w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white font-semibold py-2 rounded-lg hover:shadow-lg transition-all transform hover:scale-105 active:scale-95">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
