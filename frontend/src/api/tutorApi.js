import axios from 'axios';

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`[API REQUEST] ${config.method.toUpperCase()} ${config.url}`, config.data);
    return config;
  },
  (error) => {
    console.error('[API REQUEST ERROR]', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for logging
api.interceptors.response.use(
  (response) => {
    console.log(`[API RESPONSE] ${response.config.url}`, response.data);
    return response;
  },
  (error) => {
    console.error('[API RESPONSE ERROR]', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const tutorApi = {
  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Get topics
  getTopics: async () => {
    const response = await api.get('/api/topics');
    return response.data.topics;
  },

  // Get chapters
  getChapters: async () => {
    const response = await api.get('/api/chapters');
    return response.data.chapters;
  },

  // Get sample problems
  getSampleProblems: async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.topic) params.append('topic', filters.topic);
    if (filters.chapter) params.append('chapter', filters.chapter);
    if (filters.difficulty) params.append('difficulty', filters.difficulty);

    const response = await api.get(`/api/problems/samples?${params}`);
    return response.data;
  },

  // Submit question
  submitQuestion: async (questionData) => {
    const response = await api.post('/api/question/submit', questionData);
    return response.data;
  },

  // Chat with AI
  chat: async (problem, conversationHistory, userMessage) => {
    const response = await api.post('/api/chat', {
      problem,
      conversation_history: conversationHistory,
      user_message: userMessage,
    });
    return response.data;
  },

  // Get hint
  getHint: async (problem, conversationHistory, hintLevel) => {
    const response = await api.post('/api/hint', {
      problem,
      conversation_history: conversationHistory,
      hint_level: hintLevel,
    });
    return response.data;
  },

  // Get solution
  getSolution: async (problem) => {
    const response = await api.post('/api/solution', {
      problem,
    });
    return response.data;
  },
};

export default tutorApi;
