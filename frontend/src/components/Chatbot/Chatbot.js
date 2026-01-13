import React, { useState, useEffect, useRef } from 'react';
import { Container, Row, Col, Form, Button, Card, Badge } from 'react-bootstrap';
import { FaPaperPlane, FaRobot, FaUser, FaTrash } from 'react-icons/fa';
import { chatAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import './Chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(Date.now().toString());
  const { user } = useAuth();
  const messagesEndRef = useRef(null);
  const [showQuickReplies, setShowQuickReplies] = useState(true);

  const quickReplies = [
    { id: 1, text: "What are my interests?", category: "interests" },
    { id: 2, text: "Tell me about my skills", category: "skills" },
    { id: 3, text: "What careers suit me?", category: "careers" },
    { id: 4, text: "I need help choosing", category: "help" },
  ];

  useEffect(() => {
    // Initial greeting
    const greeting = {
      type: 'bot',
      text: `Hello ${user?.name}! 👋 I'm your AI career counselor. I'm here to help you discover the perfect career path based on your interests, skills, and personality.\n\nLet's start by getting to know you better. What are you passionate about?`,
      timestamp: new Date(),
    };
    setMessages([greeting]);
  }, [user]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async (messageText = input) => {
    if (!messageText.trim()) return;

    const userMessage = {
      type: 'user',
      text: messageText,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setShowQuickReplies(false);

    try {
      const response = await chatAPI.sendMessage({
        message: messageText,
        user_id: user?.id,
        session_id: sessionId,
      });

      const botMessage = {
        type: 'bot',
        text: response.data.response,
        timestamp: new Date(),
        intent: response.data.intent,
      };

      setMessages((prev) => [...prev, botMessage]);
      
      // Show quick replies after bot response
      setTimeout(() => setShowQuickReplies(true), 500);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        type: 'bot',
        text: 'Sorry, I encountered an error. Please try again or rephrase your question.',
        timestamp: new Date(),
        isError: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickReply = (replyText) => {
    handleSend(replyText);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const clearChat = () => {
    const greeting = messages[0];
    setMessages([greeting]);
    setShowQuickReplies(true);
  };

  return (
    <div className="chatbot-page">
      <Container fluid className="h-100">
        <Row className="justify-content-center h-100">
          <Col lg={8} xl={6} className="d-flex flex-column h-100 py-4">
            <Card className="chat-card flex-grow-1 d-flex flex-column shadow-lg border-0">
              {/* Chat Header */}
              <Card.Header className="bg-gradient-primary text-white d-flex justify-content-between align-items-center">
                <div className="d-flex align-items-center">
                  <div className="bot-avatar me-2">
                    <FaRobot size={24} />
                  </div>
                  <div>
                    <h5 className="mb-0">AI Career Counselor</h5>
                    <small className="opacity-75">
                      <span className="status-dot"></span>
                      Online
                    </small>
                  </div>
                </div>
                <Button 
                  variant="outline-light" 
                  size="sm"
                  onClick={clearChat}
                  title="Clear chat"
                >
                  <FaTrash />
                </Button>
              </Card.Header>

              {/* Chat Body */}
              <Card.Body className="chat-body flex-grow-1 overflow-auto p-4">
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`message-wrapper ${msg.type === 'user' ? 'user-wrapper' : 'bot-wrapper'}`}
                  >
                    <div className="message-container">
                      {msg.type === 'bot' && (
                        <div className="message-avatar bot-avatar">
                          <FaRobot />
                        </div>
                      )}
                      
                      <div className={`message-bubble ${msg.type}-message ${msg.isError ? 'error-message' : ''}`}>
                        <p className="message-text">{msg.text}</p>
                        <div className="message-meta">
                          <small className="message-time">
                            {msg.timestamp.toLocaleTimeString([], { 
                              hour: '2-digit', 
                              minute: '2-digit' 
                            })}
                          </small>
                          {msg.intent && (
                            <Badge bg="light" text="dark" className="ms-2 intent-badge">
                              {msg.intent}
                            </Badge>
                          )}
                        </div>
                      </div>

                      {msg.type === 'user' && (
                        <div className="message-avatar user-avatar">
                          <FaUser />
                        </div>
                      )}
                    </div>
                  </div>
                ))}

                {/* Typing Indicator */}
                {loading && (
                  <div className="message-wrapper bot-wrapper">
                    <div className="message-container">
                      <div className="message-avatar bot-avatar">
                        <FaRobot />
                      </div>
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </Card.Body>

              {/* Quick Replies */}
              {showQuickReplies && messages.length > 1 && !loading && (
                <div className="quick-replies-container px-4 py-2">
                  <small className="text-muted d-block mb-2">Quick replies:</small>
                  <div className="d-flex flex-wrap gap-2">
                    {quickReplies.map((reply) => (
                      <Button
                        key={reply.id}
                        variant="outline-primary"
                        size="sm"
                        className="quick-reply-btn"
                        onClick={() => handleQuickReply(reply.text)}
                      >
                        {reply.text}
                      </Button>
                    ))}
                  </div>
                </div>
              )}

              {/* Chat Footer */}
              <Card.Footer className="bg-white border-top p-3">
                <Form onSubmit={(e) => { e.preventDefault(); handleSend(); }}>
                  <div className="input-group">
                    <Form.Control
                      type="text"
                      placeholder="Type your message..."
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyPress={handleKeyPress}
                      disabled={loading}
                      className="chat-input"
                    />
                    <Button
                      variant="primary"
                      type="submit"
                      disabled={loading || !input.trim()}
                      className="send-btn"
                    >
                      <FaPaperPlane />
                    </Button>
                  </div>
                </Form>
                <small className="text-muted d-block mt-2 text-center">
                  Press Enter to send, Shift+Enter for new line
                </small>
              </Card.Footer>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Chatbot;