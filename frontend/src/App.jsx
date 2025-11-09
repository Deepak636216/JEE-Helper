import { useState, useEffect } from 'react'
import QuestionForm from './components/QuestionForm'
import ChatInterface from './components/ChatInterface'
import { tutorApi } from './api/tutorApi'
import './App.css'

function App() {
  const [currentProblem, setCurrentProblem] = useState(null)
  const [conversationHistory, setConversationHistory] = useState([])
  const [hintLevel, setHintLevel] = useState(0)
  const [showSolution, setShowSolution] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [apiStatus, setApiStatus] = useState(null)

  // Check API health on mount
  useEffect(() => {
    checkApiHealth()
  }, [])

  const checkApiHealth = async () => {
    try {
      const health = await tutorApi.healthCheck()
      setApiStatus(health)
      console.log('API Health:', health)
    } catch (error) {
      console.error('API health check failed:', error)
      setApiStatus({ status: 'error', error: error.message })
    }
  }

  const handleQuestionSubmit = async (questionData) => {
    setIsLoading(true)
    try {
      const response = await tutorApi.submitQuestion(questionData)

      // Set the problem
      setCurrentProblem(response.problem)

      // Initialize conversation with AI's first message
      setConversationHistory([
        {
          role: 'assistant',
          content: response.initial_message
        }
      ])

      // Reset state
      setHintLevel(0)
      setShowSolution(false)

      console.log('Question submitted successfully:', response)
    } catch (error) {
      console.error('Error submitting question:', error)
      alert('Failed to submit question. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleUserMessage = async (message) => {
    if (!currentProblem || !message.trim()) return

    // Add user message to conversation
    const newHistory = [
      ...conversationHistory,
      { role: 'user', content: message }
    ]
    setConversationHistory(newHistory)
    setIsLoading(true)

    try {
      // Get AI response
      const response = await tutorApi.chat(currentProblem, newHistory, message)

      // Add AI response to conversation
      setConversationHistory([
        ...newHistory,
        { role: 'assistant', content: response.response }
      ])
    } catch (error) {
      console.error('Error getting AI response:', error)
      setConversationHistory([
        ...newHistory,
        { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleRequestHint = async () => {
    if (!currentProblem || hintLevel >= 3) return

    const newHintLevel = hintLevel + 1
    setIsLoading(true)

    try {
      const response = await tutorApi.getHint(currentProblem, conversationHistory, newHintLevel)

      setHintLevel(newHintLevel)
      setConversationHistory([
        ...conversationHistory,
        { role: 'assistant', content: response.hint }
      ])

      if (newHintLevel >= 3) {
        setConversationHistory(prev => [
          ...prev,
          { role: 'assistant', content: "You've used all 3 hints! Would you like to see the complete solution?" }
        ])
      }
    } catch (error) {
      console.error('Error getting hint:', error)
      alert('Failed to get hint. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleShowSolution = async () => {
    if (!currentProblem) return

    setIsLoading(true)
    try {
      const response = await tutorApi.getSolution(currentProblem)
      setShowSolution(response)
    } catch (error) {
      console.error('Error getting solution:', error)
      alert('Failed to get solution. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setCurrentProblem(null)
    setConversationHistory([])
    setHintLevel(0)
    setShowSolution(false)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>JEE Physics AI Tutor</h1>
        <p>Learn through Socratic dialogue</p>
      </header>

      <main className="app-main">
        {!currentProblem ? (
          <QuestionForm onSubmit={handleQuestionSubmit} isLoading={isLoading} />
        ) : (
          <ChatInterface
            problem={currentProblem}
            conversationHistory={conversationHistory}
            onUserMessage={handleUserMessage}
            onRequestHint={handleRequestHint}
            onShowSolution={handleShowSolution}
            onReset={handleReset}
            hintLevel={hintLevel}
            showSolution={showSolution}
            isLoading={isLoading}
          />
        )}
      </main>
    </div>
  )
}

export default App
