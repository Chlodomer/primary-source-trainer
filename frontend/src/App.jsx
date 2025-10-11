import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ScenarioView from './components/ScenarioView';
import FinalSummary from './components/FinalSummary';
import './styles/App.css';

const API_URL = import.meta.env.VITE_API_URL || '';

function App() {
  const [scenarios, setScenarios] = useState([]);
  const [currentScenarioIndex, setCurrentScenarioIndex] = useState(0);
  const [sessionResults, setSessionResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [studentName, setStudentName] = useState('');
  const [nameSubmitted, setNameSubmitted] = useState(false);

  useEffect(() => {
    loadScenarios();
  }, []);

  const loadScenarios = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/scenarios`);
      // Only use first 5 scenarios
      setScenarios(response.data.slice(0, 5));
      setLoading(false);
    } catch (err) {
      setError('Failed to load scenarios. Please check if the backend is running.');
      setLoading(false);
    }
  };

  const handleSubmitScenario = async (submission) => {
    try {
      const response = await axios.post(`${API_URL}/api/grade`, submission);
      return response.data;
    } catch (err) {
      throw new Error('Failed to grade submission');
    }
  };

  const handleNextScenario = (result) => {
    setSessionResults(prev => [...prev, result]);
    setCurrentScenarioIndex(prev => prev + 1);
  };

  const handleEmailSubmit = async (studentName, studentEmail) => {
    try {
      const submission = {
        student_name: studentName,
        student_email: studentEmail || null,
        scenario_results: sessionResults
      };

      const response = await axios.post(`${API_URL}/api/submit-session`, submission);

      if (!response.data.success) {
        throw new Error(response.data.message);
      }

      return response.data;
    } catch (err) {
      throw new Error(err.response?.data?.message || 'Failed to send email');
    }
  };

  const handleNameSubmit = (e) => {
    e.preventDefault();
    if (studentName.trim()) {
      setNameSubmitted(true);
    } else {
      alert('Please enter your name to begin.');
    }
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <h2>Loading Primary Source Trainer...</h2>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">
          <h2>Error</h2>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={() => window.location.reload()}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!nameSubmitted) {
    return (
      <div className="app">
        <header className="header">
          <h1>Primary Source Trainer</h1>
          <p>Early Medieval Source Classification Exercise</p>
        </header>

        <div className="scenario-container" style={{ maxWidth: '600px', margin: '40px auto' }}>
          <h2 style={{ marginBottom: '20px', color: '#2B2B2B' }}>Welcome!</h2>
          <p style={{ marginBottom: '20px', color: '#52796F' }}>
            You'll work through <strong>5 historical scenarios</strong> to learn how to classify sources as primary or secondary based on your research question.
          </p>
          <p style={{ marginBottom: '30px', color: '#8D99AE' }}>
            Each scenario has multiple sources to classify. Please enter your name to begin.
          </p>

          <form onSubmit={handleNameSubmit}>
            <div style={{ marginBottom: '20px' }}>
              <label htmlFor="student-name" style={{
                display: 'block',
                marginBottom: '8px',
                fontWeight: '600',
                color: '#2B2B2B'
              }}>
                Your Name:
              </label>
              <input
                id="student-name"
                type="text"
                value={studentName}
                onChange={(e) => setStudentName(e.target.value)}
                placeholder="Enter your full name"
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '2px solid #C0C7C4',
                  borderRadius: '4px',
                  fontSize: '1rem',
                  fontFamily: 'Inter, sans-serif'
                }}
                autoFocus
              />
            </div>

            <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>
              Begin Training →
            </button>
          </form>
        </div>
      </div>
    );
  }

  const isComplete = currentScenarioIndex >= scenarios.length;

  return (
    <div className="app">
      <header className="header">
        <h1>Primary Source Trainer</h1>
        <p>Early Medieval Source Classification Exercise</p>
        <p style={{ marginTop: '8px', color: '#52796F', fontSize: '0.95rem' }}>
          <strong>Student:</strong> {studentName}
        </p>
      </header>

      {!isComplete && (
        <div className="progress-bar">
          <h3>Progress</h3>
          <div className="progress-track">
            <div
              className="progress-fill"
              style={{ width: `${(currentScenarioIndex / scenarios.length) * 100}%` }}
            />
          </div>
          <p className="progress-text">
            Scenario {currentScenarioIndex + 1} of {scenarios.length}
          </p>
        </div>
      )}

      {!isComplete ? (
        <ScenarioView
          scenario={scenarios[currentScenarioIndex]}
          onSubmit={handleSubmitScenario}
          onNext={handleNextScenario}
          studentName={studentName}
        />
      ) : (
        <FinalSummary
          sessionResults={sessionResults}
          onEmailSubmit={handleEmailSubmit}
          initialStudentName={studentName}
        />
      )}

      <footer style={{
        maxWidth: '1200px',
        margin: '40px auto 0',
        padding: '20px',
        textAlign: 'center',
        color: '#8D99AE',
        fontSize: '0.85rem',
        borderTop: '1px solid #C0C7C4'
      }}>
        <p>
          <strong>Learning Goal:</strong> Understand that a primary source is the <em>closest extant document</em> to your research question.
          Classifications change based on what you're studying!
        </p>
        <p style={{ marginTop: '10px' }}>
          Primary Source Trainer • Early Medieval History
        </p>
      </footer>
    </div>
  );
}

export default App;
