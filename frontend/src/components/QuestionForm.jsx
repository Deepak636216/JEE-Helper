import { useState } from 'react'
import './QuestionForm.css'

function QuestionForm({ onSubmit, isLoading }) {
  const [questionText, setQuestionText] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()

    if (!questionText.trim()) {
      alert('Please enter a question')
      return
    }

    const questionData = {
      text: questionText,
      type: 'numerical', // Default, AI will handle detection
      difficulty: 'medium',
      topic: 'General Physics'
    }

    onSubmit(questionData)
  }

  return (
    <div className="question-form-container">
      <div className="hero-section">
        <h2>Paste Your Physics Question</h2>
        <p>I'll guide you to the solution using the Socratic method</p>
      </div>

      <form onSubmit={handleSubmit} className="question-form">
        <textarea
          value={questionText}
          onChange={(e) => setQuestionText(e.target.value)}
          placeholder="Example: A ball is thrown from a 45m cliff at 20 m/s horizontally. Find the range."
          rows={8}
          required
          className="question-input"
        />

        <button
          type="submit"
          className="submit-button"
          disabled={isLoading}
        >
          {isLoading ? 'Loading...' : 'Start Learning'}
        </button>
      </form>

      <div className="examples-section">
        <p className="examples-title">Try these examples:</p>
        <ul>
          <li>A projectile is launched at 30° with velocity 50 m/s. Find maximum height.</li>
          <li>Two blocks of mass 2kg and 3kg are connected by a string over a pulley. Find tension.</li>
          <li>A wheel of radius 0.5m rotates at 120 rpm. Find angular velocity in rad/s.</li>
        </ul>
      </div>
    </div>
  )
}

export default QuestionForm
