import React, { useState, useEffect } from 'react';
import Timeline from './Timeline';
import SourceCard from './SourceCard';
import SourceGraph from './SourceGraph';

const ScenarioView = ({ scenario, onSubmit, onNext, studentName }) => {
  const [selectedTopic, setSelectedTopic] = useState(scenario.topics[0]);
  const [classifications, setClassifications] = useState({});
  const [results, setResults] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Reset state when scenario changes
  useEffect(() => {
    setSelectedTopic(scenario.topics[0]);
    setClassifications({});
    setResults(null);
    setIsSubmitting(false);
  }, [scenario.id]);

  const handleClassify = (nodeId, classification, justification) => {
    setClassifications(prev => ({
      ...prev,
      [nodeId]: { node_id: nodeId, classification, justification }
    }));
  };

  const handleSubmit = async () => {
    const classificationArray = Object.values(classifications);

    if (classificationArray.length === 0) {
      alert('Please classify at least one source before submitting.');
      return;
    }

    setIsSubmitting(true);

    try {
      const result = await onSubmit({
        scenario_id: scenario.id,
        topic_id: selectedTopic.id,
        student_name: studentName || "Anonymous",
        classifications: classificationArray
      });

      setResults(result);
    } catch (error) {
      alert('Error submitting: ' + error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleTopicChange = (e) => {
    const newTopic = scenario.topics.find(t => t.id === e.target.value);
    setSelectedTopic(newTopic);
    // Clear results when topic changes
    setResults(null);
  };

  const handleNextScenario = () => {
    if (results) {
      onNext(results);
    }
  };

  const extantNodes = scenario.nodes.filter(n => n.extant);
  const allClassified = extantNodes.every(n => classifications[n.id]);

  return (
    <div className="scenario-container">
      <div className="scenario-header">
        {scenario.event.image_url && (
          <div style={{ marginBottom: '20px', textAlign: 'center' }}>
            <img
              src={scenario.event.image_url}
              alt={scenario.event.title}
              style={{
                maxWidth: '100%',
                maxHeight: '300px',
                borderRadius: '8px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
              }}
            />
          </div>
        )}
        <h2>{scenario.event.title}</h2>
        <div className="scenario-meta">
          <span><strong>Year:</strong> {scenario.event.year} CE</span>
          <span><strong>Place:</strong> {scenario.event.place}</span>
          <span><strong>Difficulty:</strong> {scenario.difficulty}</span>
        </div>
        {scenario.event.description && (
          <p style={{ marginTop: '15px', color: '#52796F' }}>{scenario.event.description}</p>
        )}
        {scenario.event.composition_info && (
          <div style={{
            marginTop: '15px',
            padding: '12px',
            background: '#F6F4F0',
            borderLeft: '3px solid #B2643C',
            borderRadius: '4px'
          }}>
            <p style={{
              fontSize: '0.9rem',
              color: '#2B2B2B',
              margin: 0,
              fontStyle: 'italic',
              lineHeight: '1.6'
            }}>
              <strong>📜 About the sources:</strong> {scenario.event.composition_info}
            </p>
          </div>
        )}
      </div>

      <div style={{ marginTop: '20px', marginBottom: '20px', padding: '15px', background: '#F6F4F0', borderRadius: '6px', borderLeft: '3px solid #84A98C' }}>
        <p style={{ fontSize: '0.95rem', color: '#52796F', margin: 0 }}>
          <strong>📚 Research Question:</strong> {selectedTopic.label}
        </p>
      </div>

      <SourceGraph scenario={scenario} selectedTopic={selectedTopic} />

      <Timeline scenario={scenario} selectedTopic={selectedTopic} />

      <div className="source-classification">
        <h3 style={{ marginBottom: '20px', color: '#2B2B2B' }}>
          Classify Each Source ({Object.keys(classifications).length}/{extantNodes.length})
        </h3>

        {scenario.nodes.map(node => (
          <SourceCard
            key={node.id}
            node={node}
            classification={classifications[node.id]}
            onClassify={handleClassify}
          />
        ))}
      </div>

      <div className="action-buttons">
        {!results ? (
          <button
            className="btn btn-primary"
            onClick={handleSubmit}
            disabled={isSubmitting || !allClassified}
          >
            {isSubmitting ? 'Grading...' : 'Submit & Grade'}
          </button>
        ) : (
          <button
            className="btn btn-primary"
            onClick={handleNextScenario}
          >
            Next Scenario →
          </button>
        )}
      </div>

      {results && (
        <div className="results-container">
          <div className="score-display">
            Score: {results.score}/{results.max_score} ({Math.round(results.score / results.max_score * 100)}%)
          </div>

          <h3 style={{ marginBottom: '15px' }}>Results for: {results.topic_label}</h3>

          {results.results.map((result, i) => (
            <div key={i} className={`result-item ${result.is_correct ? 'correct' : 'incorrect'}`}>
              <div className="result-header">
                <span><strong>{result.node_id}</strong></span>
                <span className={`result-status ${result.is_correct ? 'correct' : 'incorrect'}`}>
                  {result.is_correct ? '✓ Correct' : '✗ Incorrect'} (+{result.points} pts)
                </span>
              </div>
              <div>
                <span style={{ fontSize: '0.9rem' }}>
                  Your answer: <strong>{result.student_answer}</strong> |
                  Correct: <strong>{result.correct_answer}</strong>
                </span>
              </div>
              <div className="feedback-text">{result.feedback}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ScenarioView;
