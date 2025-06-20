import React, { useEffect, useState } from 'react';
import api from '../services/api';

function BookingsPage() {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const response = await api.get('/api/reservations/');
        setBookings(response.data);
      } catch (err) {
        console.error('Failed to fetch bookings:', err);
        alert('Could not fetch bookings.');
      }
    })();
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h2>Your Reservations</h2>
      {bookings.length === 0 ? (
        <p>No bookings found.</p>
      ) : (
        <ul>
          {bookings.map((b) => (
            <li key={b.id}>
              <strong>Room:</strong> {b.room?.name || 'N/A'}<br />
              <strong>Date:</strong> {b.date || 'Unknown'}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default BookingsPage;
