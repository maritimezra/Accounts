/* eslint-disable no-unused-vars */
import { useMutation, gql } from '@apollo/client';
import React, { useState } from 'react';

const LOGIN_MUTATION = gql`
  mutation Login($email: String!, $password: String!) {
    login(email: $email, password: $password) {
      success
      token
    }
  }
`;

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [login, { data, loading, error }] = useMutation(LOGIN_MUTATION);

  const handleLogin = async () => {
    const response = await login({ variables: { email, password } });
    if (response.data.login.success) {
      localStorage.setItem('token', response.data.login.token);
    }
  };

  return (
    <div>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button onClick={handleLogin}>Log in</button>
      {loading && <p>Loading...</p>}
      {error && <p>{error.message}</p>}
    </div>
  );
};

export default Login;
