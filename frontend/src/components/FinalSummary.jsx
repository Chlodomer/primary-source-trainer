import React, { useState } from 'react';

const FinalSummary = ({ sessionResults, onEmailSubmit, initialStudentName = '' }) => {
  const [studentName, setStudentName] = useState(initialStudentName);
  const [studentEmail, setStudentEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [emailSent, setEmailSent] = useState(false);
  const [error, setError] = useState('');

  const totalScore = sessionResults.reduce((sum, r) => sum + r.score, 0);
  const totalMax = sessionResults.reduce((sum, r) => sum + r.max_score, 0);
  const percentage = Math.round((totalScore / totalMax) * 100);

  const correctCount = sessionResults.reduce((sum, r) => {
    return sum + r.results.filter(gr => gr.is_correct).length;
  }, 0);

  const totalQuestions = sessionResults.reduce((sum, r) => {
    return sum + r.results.length;
  }, 0);

  const handleSubmit = async () => {
    if (!studentName.trim()) {
      setError('Please enter your name.');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      const reportData = await onEmailSubmit(studentName, studentEmail);

      // Download the results as JSON file
      if (reportData && reportData.report_data) {
        const blob = new Blob([JSON.stringify(reportData.report_data, null, 2)], {
          type: 'application/json'
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = reportData.filename || `primary-source-results-${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }

      setEmailSent(true);
    } catch (err) {
      setError(err.message || 'Failed to generate results. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="final-summary">
      <h2>🎓 Session Complete!</h2>

      <div className="final-score">
        {totalScore}/{totalMax}
        <div style={{ fontSize: '1.5rem', color: '#8D99AE', marginTop: '10px' }}>
          {percentage}%
        </div>
      </div>

      <div className="summary-stats">
        <div className="stat-box">
          <div className="stat-number">{sessionResults.length}</div>
          <div className="stat-label">Scenarios Completed</div>
        </div>
        <div className="stat-box">
          <div className="stat-number">{correctCount}/{totalQuestions}</div>
          <div className="stat-label">Correct Classifications</div>
        </div>
        <div className="stat-box">
          <div className="stat-number">{percentage >= 70 ? '✓' : '○'}</div>
          <div className="stat-label">{percentage >= 70 ? 'Passed' : 'Keep Practicing'}</div>
        </div>
      </div>

      <div style={{ margin: '30px 0', padding: '20px', background: '#F6F4F0', borderRadius: '6px', textAlign: 'left' }}>
        <h3 style={{ marginBottom: '15px', color: '#2B2B2B' }}>Scenario Breakdown:</h3>
        {sessionResults.map((result, i) => {
          const scenarioPct = Math.round((result.score / result.max_score) * 100);
          return (
            <div key={i} style={{ marginBottom: '10px', paddingBottom: '10px', borderBottom: '1px solid #C0C7C4' }}>
              <strong>Scenario {i + 1}:</strong> {result.scenario_id}
              <div style={{ fontSize: '0.9rem', color: '#8D99AE' }}>
                Topic: {result.topic_label}
              </div>
              <div style={{ fontSize: '1rem', color: '#52796F', marginTop: '5px' }}>
                {result.score}/{result.max_score} ({scenarioPct}%)
              </div>
            </div>
          );
        })}
      </div>

      {!emailSent ? (
        <div className="email-form">
          <h3 style={{ marginBottom: '15px' }}>Download Your Results</h3>
          <p style={{ marginBottom: '15px', fontSize: '0.9rem', color: '#8D99AE' }}>
            Download your results file and email it to: <strong>yaniv.fox@biu.ac.il</strong>
          </p>

          {initialStudentName ? (
            <div style={{
              padding: '12px',
              background: '#F6F4F0',
              borderRadius: '4px',
              marginBottom: '15px',
              border: '2px solid #C0C7C4'
            }}>
              <strong>Student:</strong> {studentName}
            </div>
          ) : (
            <input
              type="text"
              placeholder="Your Name (required)"
              value={studentName}
              onChange={(e) => setStudentName(e.target.value)}
            />
          )}

          <input
            type="email"
            placeholder="Your Email (optional)"
            value={studentEmail}
            onChange={(e) => setStudentEmail(e.target.value)}
          />

          {error && (
            <div className="error" style={{ marginTop: '10px' }}>
              {error}
            </div>
          )}

          <button
            className="btn btn-primary"
            onClick={handleSubmit}
            disabled={isSubmitting}
            style={{ marginTop: '15px', width: '100%' }}
          >
            {isSubmitting ? 'Generating...' : 'Download Results'}
          </button>
        </div>
      ) : (
        <div style={{
          padding: '30px',
          background: '#84A98C',
          color: 'white',
          borderRadius: '6px',
          fontSize: '1.1rem'
        }}>
          <strong>✓ Results Downloaded!</strong>
          <p style={{ marginTop: '10px', fontSize: '0.95rem' }}>
            Your results file has been downloaded. Please email it to: <strong>yaniv.fox@biu.ac.il</strong>
            {percentage >= 80 ? ' Excellent work!' : percentage >= 70 ? ' Good job!' : percentage >= 50 ? ' Keep practicing!' : ''}
          </p>
        </div>
      )}

      <div style={{ marginTop: '30px', fontSize: '0.85rem', color: '#8D99AE' }}>
        <p>
          <strong>Key Takeaway:</strong> A primary source is the <em>closest extant document</em> to your research question.
          The same text can be primary for one inquiry and secondary for another!
        </p>
      </div>
    </div>
  );
};

export default FinalSummary;
