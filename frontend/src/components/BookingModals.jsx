import React, { useState } from 'react';

/**
 * Toast notification component
 */
export const Toast = ({ message, type = 'success', onClose }) => {
  React.useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  const bgColor = type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500';

  return (
    <div className={`fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-slideInRight`}>
      {message}
    </div>
  );
};

/**
 * Booking Modal Component
 */
export const BookingModal = ({ pg, isOpen, onClose, onBookingSuccess }) => {
  const [checkInDate, setCheckInDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleBooking = async () => {
    if (!checkInDate) {
      setError('Please select a check-in date');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Get token from localStorage
      const token = localStorage.getItem('authToken');
      if (!token) {
        setError('Please login to book');
        setLoading(false);
        return;
      }

      const response = await fetch('http://localhost:5000/api/booking/book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          pg_id: pg.id,
          check_in_date: checkInDate
        })
      });

      const data = await response.json();

      if (data.status === 'success') {
        onBookingSuccess(data.message);
        onClose();
      } else {
        setError(data.message || 'Booking failed');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-40">
      <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4 animate-slideUp">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Book This PG</h2>

        <div className="mb-6">
          <div className="bg-blue-50 p-4 rounded-lg mb-4">
            <p className="text-gray-600 text-sm">Property</p>
            <p className="text-lg font-semibold text-gray-900">{pg.area_locality}</p>
            <p className="text-sm text-gray-600">₹{pg.rent}/month</p>
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 font-semibold mb-2">Preferred Move-in Date</label>
            <input
              type="date"
              value={checkInDate}
              onChange={(e) => setCheckInDate(e.target.value)}
              className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
              disabled={loading}
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-lg text-sm mb-4">
              {error}
            </div>
          )}

          <div className="bg-green-50 p-4 rounded-lg mb-4">
            <p className="text-sm text-green-700 font-semibold">✓ Your booking request will be sent to the owner</p>
            <p className="text-xs text-green-600 mt-1">The owner will contact you within 24 hours</p>
          </div>
        </div>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            disabled={loading}
            className="flex-1 px-4 py-2 border-2 border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            onClick={handleBooking}
            disabled={loading}
            className="flex-1 px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Booking...
              </>
            ) : (
              'Confirm Booking'
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

/**
 * Contact Owner Modal Component
 */
export const ContactOwnerModal = ({ owner, isOpen, onClose }) => {
  const [copied, setCopied] = useState('');

  const copyToClipboard = (text, type) => {
    navigator.clipboard.writeText(text);
    setCopied(type);
    setTimeout(() => setCopied(''), 2000);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-40">
      <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4 animate-slideUp">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Contact Owner</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl"
          >
            ✕
          </button>
        </div>

        <div className="space-y-4">
          {/* Owner Name */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-gray-600 text-sm font-semibold">Owner Name</p>
            <p className="text-lg text-gray-900 font-semibold">{owner.name}</p>
          </div>

          {/* Phone */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-gray-600 text-sm font-semibold">Phone Number</p>
            <div className="flex items-center justify-between mt-2">
              <p className="text-lg text-blue-600 font-bold font-mono">{owner.phone}</p>
              <button
                onClick={() => copyToClipboard(owner.phone, 'phone')}
                className={`px-3 py-1 rounded text-sm font-semibold transition-colors ${
                  copied === 'phone'
                    ? 'bg-green-500 text-white'
                    : 'bg-blue-200 text-blue-700 hover:bg-blue-300'
                }`}
              >
                {copied === 'phone' ? '✓ Copied' : 'Copy'}
              </button>
            </div>
          </div>

          {/* Email */}
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-gray-600 text-sm font-semibold">Email Address</p>
            <div className="flex items-center justify-between mt-2">
              <p className="text-sm text-green-700 font-mono break-all">{owner.email}</p>
              <button
                onClick={() => copyToClipboard(owner.email, 'email')}
                className={`px-3 py-1 rounded text-sm font-semibold transition-colors whitespace-nowrap ml-2 ${
                  copied === 'email'
                    ? 'bg-green-500 text-white'
                    : 'bg-green-200 text-green-700 hover:bg-green-300'
                }`}
              >
                {copied === 'email' ? '✓ Copied' : 'Copy'}
              </button>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="flex gap-2 pt-4">
            <a
              href={`tel:${owner.phone}`}
              className="flex-1 bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition-colors text-center"
            >
              📞 Call
            </a>
            <a
              href={`mailto:${owner.email}`}
              className="flex-1 bg-green-600 text-white font-semibold py-2 rounded-lg hover:bg-green-700 transition-colors text-center"
            >
              ✉️ Email
            </a>
          </div>

          <p className="text-xs text-gray-500 text-center pt-4 border-t">
            Contact the owner directly to discuss terms and schedule a visit
          </p>
        </div>

        <button
          onClick={onClose}
          className="w-full mt-6 px-4 py-2 border-2 border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors"
        >
          Close
        </button>
      </div>
    </div>
  );
};
