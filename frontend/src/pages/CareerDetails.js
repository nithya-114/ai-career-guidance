import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './CareerDetails.css';

const CareerDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [career, setCareer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCareerDetails();
  }, [id]);

  const fetchCareerDetails = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:5000/api/careers/${id}`);
      setCareer(response.data);
    } catch (err) {
      console.error('Error fetching career details:', err);
      setError('Failed to load career details');
    } finally {
      setLoading(false);
    }
  };

  // Helper function to convert career_path string to array
  const getCareerPathArray = (careerPath) => {
    if (!careerPath) return [];
    
    // If it's already an array, return it
    if (Array.isArray(careerPath)) {
      return careerPath;
    }
    
    // If it's a string, split it
    if (typeof careerPath === 'string') {
      // Split by arrow symbols or commas
      return careerPath
        .split(/[→,]/)
        .map(step => step.trim())
        .filter(step => step.length > 0);
    }
    
    return [];
  };

  // Helper function to ensure array
  const ensureArray = (value) => {
    if (!value) return [];
    if (Array.isArray(value)) return value;
    if (typeof value === 'string') return [value];
    return [];
  };

  if (loading) {
    return (
      <div className="career-details-loading">
        <div className="spinner"></div>
        <p>Loading career details...</p>
      </div>
    );
  }

  if (error || !career) {
    return (
      <div className="career-details-error">
        <h2>Error</h2>
        <p>{error || 'Career not found'}</p>
        <button onClick={() => navigate('/careers')} className="btn-back">
          ← Back to Careers
        </button>
      </div>
    );
  }

  const careerPathSteps = getCareerPathArray(career.career_path);
  const skills = ensureArray(career.skills);
  const topCompanies = ensureArray(career.top_companies);
  const entranceExams = ensureArray(career.entrance_exams);
  const topColleges = ensureArray(career.top_colleges);
  const dayToDay = ensureArray(career.day_to_day);
  const pros = ensureArray(career.pros);
  const cons = ensureArray(career.cons);

  return (
    <div className="career-details-container">
      {/* Header */}
      <div className="career-details-header">
        <button onClick={() => navigate('/careers')} className="btn-back">
          ← Back to Careers
        </button>
        
        <div className="career-header-content">
          <span className="career-category-badge">{career.category}</span>
          <h1 className="career-title">{career.title || career.name}</h1>
          <p className="career-description">{career.description}</p>
          
          <div className="career-quick-stats">
            <div className="stat-item">
              <span className="stat-icon">💰</span>
              <div>
                <span className="stat-label">Salary Range</span>
                <span className="stat-value">{career.salary_range}</span>
              </div>
            </div>
            
            <div className="stat-item">
              <span className="stat-icon">📈</span>
              <div>
                <span className="stat-label">Growth Potential</span>
                <span className="stat-value">{career.growth_potential}</span>
              </div>
            </div>
            
            <div className="stat-item">
              <span className="stat-icon">💼</span>
              <div>
                <span className="stat-label">Job Outlook</span>
                <span className="stat-value">{career.job_outlook}</span>
              </div>
            </div>

            <div className="stat-item">
              <span className="stat-icon">📍</span>
              <div>
                <span className="stat-label">Work Environment</span>
                <span className="stat-value">{career.work_environment}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="career-details-content">
        {/* About Section */}
        {career.detailed_description && (
          <section className="details-section">
            <h2>📖 About This Career</h2>
            <p className="detailed-description">{career.detailed_description}</p>
          </section>
        )}

        {/* Education Requirements */}
        <section className="details-section">
          <h2>🎓 Education Requirements</h2>
          <div className="education-content">
            <div className="education-item">
              <h3>Required Education</h3>
              <p>{career.education}</p>
            </div>
            
            {entranceExams.length > 0 && (
              <div className="education-item">
                <h3>Entrance Exams</h3>
                <div className="tag-list">
                  {entranceExams.map((exam, index) => (
                    <span key={index} className="tag exam-tag">{exam}</span>
                  ))}
                </div>
              </div>
            )}
            
            {topColleges.length > 0 && (
              <div className="education-item">
                <h3>Top Colleges</h3>
                <ul className="colleges-list">
                  {topColleges.map((college, index) => (
                    <li key={index}>
                      🏛️ {college}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </section>

        {/* Skills Required */}
        {skills.length > 0 && (
          <section className="details-section">
            <h2>🏆 Skills Required</h2>
            <div className="skills-grid">
              {skills.map((skill, index) => (
                <div key={index} className="skill-card">
                  ✓ <span>{skill}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Career Path */}
        {careerPathSteps.length > 0 && (
          <section className="details-section">
            <h2>📈 Career Progression</h2>
            <div className="career-path">
              {careerPathSteps.map((step, index) => (
                <React.Fragment key={index}>
                  <div className="career-path-step">
                    <div className="step-number">{index + 1}</div>
                    <div className="step-content">
                      <h4>{step}</h4>
                    </div>
                  </div>
                  {index < careerPathSteps.length - 1 && (
                    <div className="career-path-arrow">→</div>
                  )}
                </React.Fragment>
              ))}
            </div>
          </section>
        )}

        {/* Day to Day Activities */}
        {dayToDay.length > 0 && (
          <section className="details-section">
            <h2>⏰ Day-to-Day Activities</h2>
            <ul className="activity-list">
              {dayToDay.map((activity, index) => (
                <li key={index}>
                  ✓ {activity}
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* Top Companies */}
        {topCompanies.length > 0 && (
          <section className="details-section">
            <h2>🏢 Top Companies</h2>
            <div className="companies-grid">
              {topCompanies.map((company, index) => (
                <div key={index} className="company-card">
                  🏢 <span>{company}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Pros and Cons */}
        {(pros.length > 0 || cons.length > 0) && (
          <section className="details-section">
            <h2>⚖️ Pros and Cons</h2>
            <div className="pros-cons-grid">
              {pros.length > 0 && (
                <div className="pros-section">
                  <h3>✅ Advantages</h3>
                  <ul>
                    {pros.map((pro, index) => (
                      <li key={index}>
                        ✓ {pro}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              {cons.length > 0 && (
                <div className="cons-section">
                  <h3>⚠️ Challenges</h3>
                  <ul>
                    {cons.map((con, index) => (
                      <li key={index}>
                        • {con}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </section>
        )}

        {/* Call to Action */}
        <section className="details-section cta-section">
          <h2>🚀 Ready to Pursue This Career?</h2>
          <p>Take our comprehensive career assessment to see if this career is right for you.</p>
          <div className="cta-buttons">
            <button 
              className="btn-primary"
              onClick={() => navigate('/quiz')}
            >
              📝 Take Career Quiz
            </button>
            <button 
              className="btn-secondary"
              onClick={() => navigate('/counsellors')}
            >
              👥 Talk to a Counsellor
            </button>
          </div>
        </section>
      </div>
    </div>
  );
};

export default CareerDetails;