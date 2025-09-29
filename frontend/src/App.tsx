import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import AlunoDashboard from './pages/AlunoDashboard';
import ProfessorDashboard from './pages/ProfessorDashboard';
import './App.css'; // Mantém seu estilo CSS original, se houver.

function App() {
  return (
    <Router>
      {/* O componente 'Routes' funciona como um 'switch' para decidir qual página renderizar */}
      <Routes>
        {/* Quando a URL for "/", a página de login será exibida. */}
        <Route path="/" element={<LoginPage />} />

        {/* Quando a URL for "/aluno/dashboard", o painel do aluno será exibido. */}
        <Route path="/aluno/dashboard" element={<AlunoDashboard />} />

        {/* Quando a URL for "/professor/dashboard", o painel do professor será exibido. */}
        <Route path="/professor/dashboard" element={<ProfessorDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;