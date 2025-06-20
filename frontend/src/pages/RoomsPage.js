import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

function RoomsPage() {
  const [rooms, setRooms] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/');
  };

  const handleBookRoom = async (roomId) => {
    try {
      await api.post('/api/bookings/', {
        room: roomId,
        date: new Date().toISOString().split('T')[0], // today's date
      });
      alert('Room booked!');
    } catch (error) {
      alert('Booking failed.');
      console.error(error);
    }
  };

  useEffect(() => {
    api.get('/api/rooms/')
      .then((response) => {
        setRooms(response.data);
      })
      .catch((error) => {
        console.error(error);
        setError('Could not fetch rooms. You may not be authenticated.');
      });
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Available Rooms</h2>
        <button onClick={handleLogout} style={{ padding: '6px 12px' }}>
          Logout
        </button>
        <button onClick={() => navigate('/bookings')} style={{ marginRight: '10px' }}>
        My Bookings
        </button>

      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <ul>
        {rooms.map((room) => (
          <li key={room.id}>
            <strong>{room.name}</strong> - Capacity: {room.capacity}
            <button
              onClick={() => handleBookRoom(room.id)}
              style={{ marginLeft: '10px' }}
            >
              Book
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RoomsPage;
