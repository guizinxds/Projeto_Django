import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode'; 
import './LoginPage.css';

// Define a estrutura do token decodificado
interface DecodedToken {
  profile_type: 'aluno' | 'trabalhador' | 'desconhecido' | 'sem_perfil';
}

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError('');

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/token/', {
        username: username,
        password: password,
      });

      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);

      const decodedToken = jwtDecode<DecodedToken>(response.data.access);
      
      if (decodedToken.profile_type === 'aluno') {
        navigate('/aluno/dashboard');
      } else if (decodedToken.profile_type === 'trabalhador') {
        navigate('/professor/dashboard');
      } else {
        setError('Tipo de perfil não reconhecido.');
      }

    } catch (err) {
      console.error('Erro no login:', err);
      setError('Usuário ou senha inválidos. Tente novamente.');
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2>Acessar o Sistema</h2>
        {error && <p className="error-message">{error}</p>}
        <div className="input-group">
          <label htmlFor="username">Usuário</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="password">Senha</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="login-button">Entrar</button>
      </form>
    </div>
  );
}

export default LoginPage;