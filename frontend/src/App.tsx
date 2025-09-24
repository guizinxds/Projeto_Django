import { useState, useEffect } from 'react';
import axios from 'axios'; // Importamos o axios que acabamos de instalar
import './App.css';

interface Aluno {
  id: number;
  nome_completo: string;
  email: string;
  cpf_aluno: string;
  turma__escolha_a_turma: string;
}

function App() {
  // Criamos um "estado" para armazenar a lista de alunos que virá da API.
  // Começa como uma lista vazia.
  const [alunos, setAlunos] = useState<Aluno[]>([]);

  // Criamos um estado para sabermos se os dados ainda estão carregando.
  const [loading, setLoading] = useState(true);

  // useEffect é um "gancho" do React que executa um código assim que
  // o componente é montado na tela. Perfeito para buscar dados iniciais.
  useEffect(() => {
    // Função que busca os dados na nossa API Django
    const fetchAlunos = async () => {
      try {
        // Usamos o axios para fazer uma requisição GET para a nossa URL da API.
        const response = await axios.get('http://127.0.0.1:8000/api/alunos/');
        
        // Se a requisição for bem-sucedida, guardamos os dados no nosso estado.
        setAlunos(response.data);

      } catch (error) {
        console.error("Houve um erro ao buscar os alunos:", error);
      } finally {
        // Independentemente de ter dado certo ou errado, paramos o "loading".
        setLoading(false);
      }
    };

    // Chamamos a função para que ela execute.
    fetchAlunos();
  }, []); // O array vazio [] significa que este useEffect rodará apenas uma vez.

  // Se ainda estiver carregando, mostramos uma mensagem.
  if (loading) {
    return <h1>Carregando alunos do sistema...</h1>;
  }

  // Se já carregou, mostramos os dados.
  return (
    <div className="App">
      <h1>Painel de Alunos</h1>
      <p>Dados fornecidos diretamente pelo Django!</p>
      
      <table>
        <thead>
          <tr>
            <th>Nome Completo</th>
            <th>Email</th>
            <th>Turma</th>
          </tr>
        </thead>
        <tbody>
          {/* Usamos .map() para criar uma linha <tr> para cada aluno na lista */}
          {alunos.map((aluno) => (
            <tr key={aluno.id}>
              <td>{aluno.nome_completo}</td>
              <td>{aluno.email}</td>
              <td>{aluno.turma__escolha_a_turma}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;