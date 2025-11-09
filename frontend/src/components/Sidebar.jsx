import { useState, useEffect } from 'react'
import { tutorApi } from '../api/tutorApi'
import './Sidebar.css'

function Sidebar({ onReset, onLoadSample, hasProblem }) {
  const [topics, setTopics] = useState([])
  const [sampleProblems, setSampleProblems] = useState([])
  const [selectedTopic, setSelectedTopic] = useState(null)
  const [showSamples, setShowSamples] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    loadTopics()
  }, [])

  const loadTopics = async () => {
    try {
      const topicsData = await tutorApi.getTopics()
      setTopics(topicsData)
    } catch (error) {
      console.error('Error loading topics:', error)
    }
  }

  const loadSampleProblems = async (topic) => {
    setIsLoading(true)
    try {
      const response = await tutorApi.getSampleProblems({ topic })
      setSampleProblems(response.problems || [])
      setSelectedTopic(topic)
      setShowSamples(true)
    } catch (error) {
      console.error('Error loading sample problems:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-section">
        <h3>📚 How to Use</h3>
        <ol>
          <li>Enter your physics question</li>
          <li>Add options (for MCQ)</li>
          <li>Click "Start Learning"</li>
          <li>Chat with AI tutor</li>
          <li>Request hints when stuck</li>
          <li>Discover the solution!</li>
        </ol>
      </div>

      {hasProblem && (
        <button onClick={onReset} className="reset-button-sidebar">
          🔄 Start New Question
        </button>
      )}

      <div className="sidebar-section">
        <h3>💡 Sample Topics</h3>
        <ul className="topics-list">
          <li>Laws of Motion</li>
          <li>Projectile Motion</li>
          <li>Work & Energy</li>
          <li>Rotation</li>
          <li>Center of Mass</li>
          <li>Friction & Forces</li>
        </ul>
      </div>

      {topics.length > 0 && (
        <div className="sidebar-section">
          <h3>📋 Sample Problems</h3>
          <p className="sample-count">
            {topics.length} topics available
          </p>

          {!showSamples ? (
            <div className="topics-buttons">
              {topics.slice(0, 5).map((topic, index) => (
                <button
                  key={index}
                  onClick={() => loadSampleProblems(topic)}
                  disabled={isLoading}
                  className="topic-button"
                >
                  {topic}
                </button>
              ))}
            </div>
          ) : (
            <div className="samples-list">
              <button
                onClick={() => setShowSamples(false)}
                className="back-button"
              >
                ← Back to Topics
              </button>

              <h4>{selectedTopic}</h4>
              <p>{sampleProblems.length} problems</p>

              {sampleProblems.slice(0, 3).map((problem, index) => (
                <div key={index} className="sample-problem">
                  <p className="problem-id">{problem.id}</p>
                  <p className="problem-preview">
                    {problem.text.substring(0, 100)}...
                  </p>
                  <button
                    onClick={() => {
                      onLoadSample(problem)
                      setShowSamples(false)
                    }}
                    className="load-button"
                  >
                    Load Problem
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <div className="sidebar-footer">
        <p>Made with ❤️ for JEE aspirants</p>
        <p>Powered by AI</p>
      </div>
    </aside>
  )
}

export default Sidebar
