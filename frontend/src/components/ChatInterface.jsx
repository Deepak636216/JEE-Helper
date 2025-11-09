import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import './ChatInterface.css'

function ChatInterface({
  problem,
  conversationHistory,
  onUserMessage,
  onRequestHint,
  onShowSolution,
  onReset,
  hintLevel,
  showSolution,
  isLoading
}) {
  const [userInput, setUserInput] = useState('')
  const chatEndRef = useRef(null)

  // Auto-scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [conversationHistory])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!userInput.trim() || isLoading) return

    onUserMessage(userInput)
    setUserInput('')
  }

  return (
    <div className="chat-interface">
      <div className="problem-display">
        <div className="problem-text">
          {problem.text}
        </div>

        {problem.options && problem.options.length > 0 && (
          <div className="problem-options">
            {problem.options.map((option) => (
              <div key={option.id} className="option">
                <strong>{option.id.toUpperCase()}.</strong> {option.text}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="main-content">
        <div className="chat-section">
          <div className="chat-messages">
            {conversationHistory.map((message, index) => (
              <div
                key={index}
                className={`message ${message.role === 'user' ? 'user-message' : 'ai-message'}`}
              >
                <div className="message-content">
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message ai-message">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={chatEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="chat-input-form">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Type your answer..."
              disabled={isLoading}
              className="chat-input"
            />
            <button type="submit" disabled={isLoading || !userInput.trim()} className="send-button">
              Send
            </button>
          </form>

          <div className="action-buttons">
            <button
              onClick={onRequestHint}
              disabled={isLoading || hintLevel >= 3}
              className="hint-button"
            >
              Hint {hintLevel > 0 && `(${hintLevel}/3)`}
            </button>

            <button
              onClick={onShowSolution}
              disabled={isLoading || showSolution}
              className="solution-button"
            >
              {showSolution ? 'Solution Shown' : 'Solution'}
            </button>

            <button
              onClick={onReset}
              className="reset-button"
            >
              New Question
            </button>
          </div>
        </div>

        {showSolution && (
          <div className="solution-panel">
            <h3>Complete Solution</h3>
            <div className="solution-content">
              {showSolution.type === 'official' ? (
                <div>
                  {showSolution.solution.steps && showSolution.solution.steps.map((step, index) => (
                    <div key={index} className="solution-step">
                      <h4>Step {step.step_number}: {step.description}</h4>
                      <p><strong>Formula:</strong> <code>{step.formula}</code></p>
                      <p><strong>Calculation:</strong> {step.calculation}</p>
                      <p><strong>Explanation:</strong> {step.explanation}</p>
                      {step.result && (
                        <p className="result"><strong>Result:</strong> {step.result}</p>
                      )}
                    </div>
                  ))}
                  {showSolution.solution.answer_justification && (
                    <div className="answer-box">
                      <strong>Answer:</strong> {showSolution.solution.answer_justification}
                    </div>
                  )}
                </div>
              ) : (
                <ReactMarkdown>{showSolution.solution}</ReactMarkdown>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatInterface
