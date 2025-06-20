import React, { useState } from 'react';
import api from '../services/api';
import './LoginPage.css';


function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');

  const handleLogin = async (e) => {
  e.preventDefault();
  try {
    const response = await api.post('/api/token/', { username, password });
    const accessToken = response.data.access;
    localStorage.setItem('access_token', accessToken);  // store token
    aler
    t('Login successful!');
    window.location.href = '/rooms';  // redirect to rooms page
  } catch (error) {
    alert('Login failed');
    console.error(error);
  }
};


  return (
    <div  className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        /><br/>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        /><br/>
        <button type="submit">Login</button>
      </form>
      {token && <p>Token: {token}</p>}
    </div>
  );
}

export default LoginPage;
