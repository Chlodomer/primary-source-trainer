import React, { useState, useEffect } from 'react';

const JUSTIFICATION_OPTIONS = {
  primary: [
    "The author witnessed the event firsthand",
    "Written at the time of the event (or very close to it)",
    "The closest surviving document to the event",
    "Preserves information from lost sources (making this the closest surviving document)"
  ],
  secondary: [
    "Written long after the event (when closer sources still exist)",
    "Compiles or synthesizes earlier medieval sources",
    "Modern scholarship analyzing other surviving sources",
    "Several transmission steps away from the original event"
  ],
  dependent_on_topic: [
    "Classification changes depending on the research question"
  ]
};

const SourceCard = ({ node, classification, onClassify }) => {
  const [justification, setJustification] = useState(classification?.justification || '');

  // Reset justification when classification is cleared (new scenario)
  useEffect(() => {
    setJustification(classification?.justification || '');
  }, [classification?.justification, node.id]);

  const handleClassification = (type) => {
    onClassify(node.id, type, justification);
  };

  const handleJustificationChange = (e) => {
    const newJustification = e.target.value;
    setJustification(newJustification);
    if (classification?.classification) {
      onClassify(node.id, classification.classification, newJustification);
    }
  };

  if (!node.extant) {
    return (
      <div className="source-card lost">
        <div className="source-header">
          <div>
            <h3 className="source-title">{node.title}</h3>
            <div className="source-meta">
              {node.author_role} • {node.year} CE • <strong>LOST</strong>
            </div>
            {node.place && <div className="source-meta">{node.place}</div>}
          </div>
        </div>
        {node.description && (
          <p style={{ marginTop: '10px', fontSize: '0.9rem', color: '#8D99AE', fontStyle: 'italic' }}>
            {node.description}
          </p>
        )}
        <p style={{ marginTop: '10px', fontSize: '0.9rem', color: '#8D99AE' }}>
          This source is lost and cannot be classified as primary or secondary.
        </p>
      </div>
    );
  }

  return (
    <div className="source-card extant">
      <div className="source-header">
        <div>
          <h3 className="source-title">{node.title}</h3>
          <div className="source-meta">
            {node.author_role} • {node.year} CE
          </div>
          {node.place && <div className="source-meta">{node.place}</div>}
        </div>
      </div>

      {node.description && (
        <p style={{ marginTop: '10px', fontSize: '0.9rem', color: '#52796F' }}>
          {node.description}
        </p>
      )}

      {node.transmission && node.transmission.length > 0 && (
        <div style={{ marginTop: '10px', fontSize: '0.85rem', color: '#8D99AE', fontStyle: 'italic' }}>
          Transmission: {node.transmission.map(t => `${t.type} (${t.year})`).join(' → ')}
        </div>
      )}

      <div className="classification-buttons">
        <button
          className={`classification-btn ${classification?.classification === 'primary' ? 'selected' : ''}`}
          onClick={() => handleClassification('primary')}
        >
          Primary
        </button>
        <button
          className={`classification-btn secondary ${classification?.classification === 'secondary' ? 'selected' : ''}`}
          onClick={() => handleClassification('secondary')}
        >
          Secondary
        </button>
        <button
          className={`classification-btn ${classification?.classification === 'dependent_on_topic' ? 'selected' : ''}`}
          onClick={() => handleClassification('dependent_on_topic')}
        >
          Depends on Topic
        </button>
      </div>

      {classification?.classification && (
        <div className="justification-input">
          <label htmlFor={`justification-${node.id}`} style={{
            display: 'block',
            marginBottom: '5px',
            fontSize: '0.9rem',
            fontWeight: '500'
          }}>
            Why is this {classification.classification.replace(/_/g, ' ')}?
          </label>
          <select
            id={`justification-${node.id}`}
            value={justification}
            onChange={handleJustificationChange}
            style={{
              width: '100%',
              padding: '10px',
              border: '2px solid #C0C7C4',
              borderRadius: '4px',
              fontSize: '0.95rem',
              fontFamily: 'Inter, sans-serif',
              backgroundColor: 'white',
              cursor: 'pointer'
            }}
          >
            <option value="">-- Select a reason --</option>
            {JUSTIFICATION_OPTIONS[classification.classification]?.map((option, i) => (
              <option key={i} value={option}>{option}</option>
            ))}
          </select>
        </div>
      )}
    </div>
  );
};

export default SourceCard;
