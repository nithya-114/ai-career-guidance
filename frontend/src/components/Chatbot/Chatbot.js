// src/components/Chatbot/Chatbot.js
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './Chatbot.css';

const API_URL = 'http://localhost:5000/api';

const Chatbot = () => {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
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
    return content.split('\n').map((line, i) => (
      <React.Fragment key={i}>
        {line}
        {i < content.split('\n').length - 1 && <br />}
      </React.Fragment>
    ));
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
    <div className="chatbot-wrapper">
      <div className="chatbot-container">
        {/* Header */}
        <div className="chatbot-header">
          <div className="header-left">
            <div className="bot-avatar-large">
              <span className="icon-sparkles">✨</span>
            </div>
            <div className="header-text">
              <h1 className="header-title">
                AI Career Counsellor
                <span className="status-badge">
                  <span className="status-dot"></span>
                  Online
                </span>
              </h1>
              <p className="header-subtitle">Your personalized career discovery assistant</p>
            </div>
          </div>
          <button onClick={resetChat} className="reset-button">
            <span className="icon-rotate">🔄</span>
            <span className="reset-text">New Session</span>
          </button>
        </div>

        {/* Progress Bar */}
        {progress > 0 && progress < 100 && (
          <div className="progress-section">
            <div className="progress-info">
              <span className="progress-label">Discovery Progress</span>
              <span className="progress-percentage">{progress}%</span>
            </div>
            <div className="progress-bar-outer">
              <div className="progress-bar-inner" style={{ width: `${progress}%` }}></div>
            </div>
          </div>
        )}

        {/* Messages Area */}
        <div className="messages-area">
          {messages.map((msg, index) => (
            <div key={index} className={`message-wrapper ${msg.role === 'user' ? 'user-message' : 'bot-message'}`}>
              <div className={`message-avatar ${msg.role}`}>
                {msg.role === 'bot' ? (
                  <span className="avatar-icon">🤖</span>
                ) : (
                  <span className="avatar-icon">👤</span>
                )}
              </div>
              
              <div className="message-content-wrapper">
                <div className={`message-bubble ${msg.role}`}>
                  <p className="message-text">{formatMessage(msg.content)}</p>
                </div>
                <span className="message-timestamp">
                  {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message-wrapper bot-message">
              <div className="message-avatar bot">
                <span className="avatar-icon">🤖</span>
              </div>
              <div className="message-content-wrapper">
                <div className="message-bubble bot">
                  <div className="typing-indicator">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Recommendations Panel */}
        {showRecommendations && recommendations.length > 0 && (
          <div className="recommendations-section">
            <div className="recommendations-header">
              <span className="rec-icon">⚡</span>
              <h3 className="rec-title">Your Top Career Matches</h3>
            </div>
            
            <div className="recommendations-grid">
              {recommendations.map((rec, index) => (
                <div key={index} className="recommendation-card">
                  <div className="rec-card-header">
                    <h4 className="rec-card-title">{rec.title}</h4>
                    <span className="match-score">
                      {Math.round((rec.match_score / 20) * 100)}%
                    </span>
                  </div>
                  
                  <p className="rec-description">{rec.description}</p>
                  
                  <div className="rec-info">
                    <div className="rec-info-item">
                      <span className="info-icon">💰</span>
                      <span>{rec.salary_range}</span>
                    </div>
                    <div className="rec-info-item">
                      <span className="info-icon">📈</span>
                      <span>{rec.growth_potential} Growth</span>
                    </div>
                  </div>
                  
                  <div className="rec-courses">
                    <div className="courses-header">
                      <span className="courses-icon">📚</span>
                      <span className="courses-label">Recommended Courses</span>
                    </div>
                    <p className="courses-list">{rec.courses.slice(0, 2).join(', ')}</p>
                  </div>
                  
                  <button onClick={() => viewCareerDetails(rec.career_id)} className="details-button">
                    View Details
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="input-section">
          <div className="input-container">
            <div className="input-wrapper">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Share your thoughts, interests, or ask me anything..."
                disabled={isLoading}
                rows="1"
                className="message-input"
              />
              <div className="char-counter">{inputMessage.length}/500</div>
            </div>
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className="send-button"
            >
              {isLoading ? (
                <div className="spinner"></div>
              ) : (
                <span className="send-icon">📤</span>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;