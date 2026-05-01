import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { recommendationAPI } from '../api/api';
import { BookingModal, ContactOwnerModal, Toast } from '../components/BookingModals';
import { AuthContext } from '../context/AuthContext';

export const DetailsPage = () => {
  const { pgId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useContext(AuthContext);
  
  const [pg, setPG] = useState(null);
  const [similar, setSimilar] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Modal states
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [showContactModal, setShowContactModal] = useState(false);
  const [owner, setOwner] = useState(null);
  
  // Toast notification
  const [toast, setToast] = useState(null);

  useEffect(() => {
    fetchPGDetails();
  }, [pgId]);

  // Handle Book Now button
  const handleBookNow = async () => {
    if (!isAuthenticated) {
      setToast({ message: 'Please login to book', type: 'error' });
      setTimeout(() => navigate('/auth'), 2000);
      return;
    }
    setShowBookingModal(true);
  };

  // Handle Contact Owner button
  const handleContactOwner = async () => {
    if (!owner) {
      try {
        const response = await fetch(`http://localhost:5000/api/booking/get-owner-details/${pgId}`);
        const data = await response.json();
        if (data.status === 'success') {
          setOwner(data.owner);
          setShowContactModal(true);
        } else {
          setToast({ message: 'Unable to load owner details', type: 'error' });
        }
      } catch (err) {
        setToast({ message: 'Network error: ' + err.message, type: 'error' });
      }
    } else {
      setShowContactModal(true);
    }
  };

  const handleBookingSuccess = (message) => {
    setToast({ message, type: 'success' });
  };

  const fetchPGDetails = async () => {
    try {
      setLoading(true);
      const response = await recommendationAPI.getPGDetails(pgId);
      if (response.data.status === 'success') {
        setPG(response.data.pg);
        setSimilar(response.data.pg.similar_pgs || []);
      }
    } catch (err) {
      setError('Failed to load PG details');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading PG details...</p>
        </div>
      </div>
    );
  }

  if (error || !pg) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'PG not found'}</p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <button
        onClick={() => navigate(-1)}
        className="m-4 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
      >
        ← Back
      </button>

      <div className="max-w-6xl mx-auto px-4">
        {/* Hero Section */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden mb-8">
          <img
            src={pg.image_url}
            alt={pg.area_locality}
            className="w-full h-96 object-cover"
          />
          <div className="p-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              {pg.area_locality}
            </h1>
            <p className="text-gray-600 mb-4">{pg.city} • {pg.area_type}</p>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Rent</p>
                <p className="text-2xl font-bold text-blue-600">₹{pg.rent}</p>
                <p className="text-xs text-gray-500">per month</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Rating</p>
                <p className="text-2xl font-bold text-green-600">⭐ {pg.rating}</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">BHK</p>
                <p className="text-2xl font-bold text-purple-600">{pg.bhk}</p>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Size</p>
                <p className="text-2xl font-bold text-orange-600">{pg.size} sq ft</p>
              </div>
            </div>

            <div className="flex gap-4 mb-8">
              <button 
                onClick={handleBookNow}
                className="flex-1 bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Book Now
              </button>
              <button 
                onClick={handleContactOwner}
                className="flex-1 bg-white border-2 border-blue-600 text-blue-600 font-semibold py-3 rounded-lg hover:bg-blue-50 transition-colors"
              >
                Contact Owner
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Details */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Property Details</h2>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <p className="text-gray-600 text-sm font-semibold">Room Type</p>
                  <p className="text-lg font-semibold text-gray-900">{pg.bhk} BHK</p>
                </div>
                <div>
                  <p className="text-gray-600 text-sm font-semibold">Furnishing</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {pg.furnishing_status}
                  </p>
                </div>
                <div>
                  <p className="text-gray-600 text-sm font-semibold">Tenant Type</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {pg.tenant_preferred}
                  </p>
                </div>
                <div>
                  <p className="text-gray-600 text-sm font-semibold">Bathrooms</p>
                  <p className="text-lg font-semibold text-gray-900">{pg.bathroom}</p>
                </div>
                <div>
                  <p className="text-gray-600 text-sm font-semibold">Floor</p>
                  <p className="text-lg font-semibold text-gray-900">{pg.floor}</p>
                </div>
                <div>
                  <p className="text-gray-600 text-sm font-semibold">Contact</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {pg.point_of_contact}
                  </p>
                </div>
              </div>
            </div>

            {/* Amenities */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">What this place offers</h2>

              <div className="grid grid-cols-2 gap-4">
                {pg.amenities && pg.amenities.map((amenity, idx) => (
                  <div
                    key={idx}
                    className={`p-4 rounded-lg border-2 ${
                      amenity.available
                        ? 'border-green-200 bg-green-50'
                        : 'border-gray-200 bg-gray-50'
                    }`}
                  >
                    <p className="text-sm font-semibold text-gray-900">
                      {amenity.available ? '✓' : '✗'} {amenity.name}
                    </p>
                    <p className="text-xs text-gray-600">
                      {amenity.available ? 'Available' : 'Not available'}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Rating & Reviews */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Ratings & Reviews</h2>

            <div className="text-center mb-8">
              <div className="text-5xl font-bold text-blue-600 mb-2">{pg.rating}</div>
              <div className="flex justify-center gap-1 mb-2">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className="text-xl">
                    {i < Math.floor(pg.rating) ? '⭐' : '☆'}
                  </span>
                ))}
              </div>
              <p className="text-gray-600 text-sm">
                {pg.reviews ? pg.reviews.length : 0} reviews
              </p>
            </div>

            {pg.reviews && pg.reviews.length > 0 ? (
              <div className="space-y-4">
                {pg.reviews.slice(0, 3).map((review, idx) => (
                  <div key={idx} className="border-b pb-4">
                    <div className="flex justify-between items-start mb-2">
                      <p className="font-semibold text-gray-900">{review.user}</p>
                      <span className="text-yellow-500">⭐ {review.rating}</span>
                    </div>
                    <p className="text-sm text-gray-600">{review.comment}</p>
                    <p className="text-xs text-gray-400 mt-2">{review.created_at}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-center text-gray-500">No reviews yet</p>
            )}
          </div>
        </div>

        {/* Similar PGs */}
        {similar && similar.length > 0 && (
          <div className="mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Similar PGs You May Like</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {similar.map((sim) => (
                <div
                  key={sim.id}
                  onClick={() => navigate(`/pg/${sim.id}`)}
                  className="bg-white rounded-lg shadow-lg overflow-hidden cursor-pointer hover:shadow-xl transition-shadow"
                >
                  <img
                    src={sim.image_url}
                    alt={sim.area_locality}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4">
                    <h3 className="font-bold text-gray-900 mb-2">{sim.area_locality}</h3>
                    <p className="text-blue-600 font-bold text-xl mb-2">₹{sim.rent}/month</p>
                    <div className="flex justify-between text-sm text-gray-600">
                      <span>{sim.bhk} BHK</span>
                      <span>⭐ {sim.rating}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Modals and Toast */}
      <BookingModal 
        pg={pg}
        isOpen={showBookingModal}
        onClose={() => setShowBookingModal(false)}
        onBookingSuccess={handleBookingSuccess}
      />
      
      <ContactOwnerModal 
        owner={owner}
        isOpen={showContactModal}
        onClose={() => setShowContactModal(false)}
      />
      
      {toast && (
        <Toast 
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
};
