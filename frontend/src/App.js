import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RoomsPage from './pages/RoomsPage';
import BookingsPage from './pages/BookingsPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
          <Route path="/rooms" element={<RoomsPage />} />
          <Route path="/bookings" element={<BookingsPage />} />
          <Route path="/bookings" element={<BookingsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
