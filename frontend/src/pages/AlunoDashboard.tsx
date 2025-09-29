import { useState, useEffect } from 'react';
import axios from 'axios';

interface Aluno {
  id: number;
  nome_completo: string;
  email: string;
  cpf_aluno: string;
  turma__escolha_a_turma: string;
}

function AlunoDashboard() {
  const [alunos, setAlunos] = useState<Aluno[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlunos = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/alunos/');
        setAlunos(response.data);
      } catch (error) {
        console.error("Houve um erro ao buscar os alunos:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchAlunos();
  }, []);

  if (loading) {
    return <h1>Carregando informações...</h1>;
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Painel do Aluno</h1>
      <p>Bem-vindo! Aqui estão os alunos cadastrados.</p>
      
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f2f2f2' }}>
            <th style={{ padding: '8px', border: '1px solid #ddd', textAlign: 'left' }}>Nome Completo</th>
            <th style={{ padding: '8px', border: '1px solid #ddd', textAlign: 'left' }}>Email</th>
            <th style={{ padding: '8px', border: '1px solid #ddd', textAlign: 'left' }}>Turma</th>
          </tr>
        </thead>
        <tbody>
          {alunos.map((aluno) => (
            <tr key={aluno.id}>
              <td style={{ padding: '8px', border: '1px solid #ddd' }}>{aluno.nome_completo}</td>
              <td style={{ padding: '8px', border: '1px solid #ddd' }}>{aluno.email}</td>
              <td style={{ padding: '8px', border: '1px solid #ddd' }}>{aluno.turma__escolha_a_turma}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AlunoDashboard;