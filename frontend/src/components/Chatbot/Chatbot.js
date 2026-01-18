// src/components/Chatbot/Chatbot.js
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './Chatbot.css';

const API_URL = 'http://localhost:5000/api';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [recommendations, setRecommendations] = useState([]);
  const [showRecommendations, setShowRecommendations] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    startChat();
    // Cleanup function
    return () => {
      if (sessionId) {
        endChat();
      }
    };
  }, []);

  const startChat = async () => {
    try {
      setIsLoading(true);
      const response = await axios.post(`${API_URL}/chat/start`, {
        session_id: null
      });

      if (response.data.success) {
        setSessionId(response.data.session_id);
        setMessages([{
          role: 'bot',
          content: response.data.message,
          timestamp: new Date().toISOString()
        }]);
      }
    } catch (error) {
      console.error('Error starting chat:', error);
      setMessages([{
        role: 'bot',
        content: 'Sorry, I encountered an error connecting to the server. Please make sure the backend is running on http://localhost:5000',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const endChat = async () => {
    try {
      await axios.post(`${API_URL}/chat/end/${sessionId}`);
    } catch (error) {
      console.error('Error ending chat:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !sessionId || isLoading) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat/message`, {
        session_id: sessionId,
        message: inputMessage
      });

      if (response.data.success) {
        const botMessage = {
          role: 'bot',
          content: response.data.message,
          timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, botMessage]);

        if (response.data.progress) {
          setProgress(response.data.progress);
        }

        if (response.data.recommendations && response.data.recommendations.length > 0) {
          setRecommendations(response.data.recommendations);
          setShowRecommendations(true);
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'bot',
        content: 'Sorry, I encountered an error. Please try again or check your connection.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const resetChat = async () => {
    if (sessionId) {
      await endChat();
    }
    setMessages([]);
    setRecommendations([]);
    setShowRecommendations(false);
    setProgress(0);
    setSessionId(null);
    startChat();
  };

  const formatMessage = (content) => {
    // Convert markdown-style formatting
    let formatted = content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br/>');
    return { __html: formatted };
  };

  const viewCareerDetails = async (careerId) => {
    try {
      const response = await axios.get(`${API_URL}/chat/career-details/${careerId}`);
      if (response.data.success) {
        alert(`Career: ${response.data.career.title}\n\nDescription: ${response.data.career.description}\n\nSkills: ${response.data.career.skills.join(', ')}`);
      }
    } catch (error) {
      console.error('Error fetching career details:', error);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <div className="header-content">
          <h2>🤖 AI Career Counsellor</h2>
          <p>Let's discover your perfect career path!</p>
        </div>
        <button className="reset-btn" onClick={resetChat} title="Start New Session">
          🔄 Reset
        </button>
      </div>

      {progress > 0 && progress < 100 && (
        <div className="progress-bar-container">
          <div className="progress-bar" style={{ width: `${progress}%` }}>
            <span className="progress-text">{progress}%</span>
          </div>
        </div>
      )}

      <div className="chatbot-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'bot' ? '🤖' : '👤'}
            </div>
            <div className="message-content">
              <div 
                className="message-text"
                dangerouslySetInnerHTML={formatMessage(msg.content)}
              />
              <span className="message-time">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message bot">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {showRecommendations && recommendations.length > 0 && (
        <div className="recommendations-panel">
          <h3>🎯 Your Career Recommendations</h3>
          <div className="recommendations-grid">
            {recommendations.map((rec, index) => (
              <div key={index} className="recommendation-card">
                <div className="rec-header">
                  <h4>{rec.title}</h4>
                  <span className="match-badge">
                    {Math.round((rec.match_score / 20) * 100)}% Match
                  </span>
                </div>
                <p className="rec-description">{rec.description}</p>
                <div className="rec-details">
                  <div className="rec-detail">
                    <span className="detail-icon">💰</span>
                    <span>{rec.salary_range}</span>
                  </div>
                  <div className="rec-detail">
                    <span className="detail-icon">📈</span>
                    <span>{rec.growth_potential}</span>
                  </div>
                </div>
                <div className="rec-courses">
                  <strong>📚 Courses:</strong>
                  <p>{rec.courses.slice(0, 2).join(', ')}</p>
                </div>
                <button 
                  className="view-details-btn"
                  onClick={() => viewCareerDetails(rec.career_id)}
                >
                  View Details
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="chatbot-input">
        <textarea
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here..."
          disabled={isLoading}
          rows="1"
        />
        <button 
          onClick={sendMessage} 
          disabled={isLoading || !inputMessage.trim()}
          className="send-btn"
          title="Send message"
        >
          {isLoading ? '⏳' : '📤'}
        </button>
      </div>
    </div>
  );
};

export default Chatbot;