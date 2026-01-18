import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../assets/css/College.css';

function CollegeFinder() {
  const [colleges, setColleges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Filters
  const [selectedCourse, setSelectedCourse] = useState('all');
  const [selectedDistrict, setSelectedDistrict] = useState('all');
  const [selectedType, setSelectedType] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('rating');
  
  // View mode
  const [viewMode, setViewMode] = useState('grid');
  
  useEffect(() => {
    const fetchColleges = async () => {
      try {
        const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
        const response = await axios.get(`${API_URL}/colleges`);
        setColleges(response.data.colleges || []);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching colleges:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchColleges();
  }, []);

  // Extract unique values for filters
  const courses = ['all', ...new Set(colleges.flatMap(c => c.courses || []))].sort();
  const districts = ['all', ...new Set(colleges.map(c => c.district))].sort();
  const types = ['all', ...new Set(colleges.map(c => c.type))].sort();

  // Filter colleges
  const filteredColleges = colleges.filter(college => {
    const matchesCourse = selectedCourse === 'all' || college.courses?.includes(selectedCourse);
    const matchesDistrict = selectedDistrict === 'all' || college.district === selectedDistrict;
    const matchesType = selectedType === 'all' || college.type === selectedType;
    const matchesSearch = searchQuery === '' || 
      college.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      college.location?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      college.specializations?.some(s => s.toLowerCase().includes(searchQuery.toLowerCase()));
    
    return matchesCourse && matchesDistrict && matchesType && matchesSearch;
  });

  // Sort colleges
  const sortedColleges = [...filteredColleges].sort((a, b) => {
    switch(sortBy) {
      case 'rating':
        return (b.rating || 0) - (a.rating || 0);
      case 'name':
        return (a.name || '').localeCompare(b.name || '');
      case 'fees':
        const getFeesValue = (str) => {
          const match = str?.match(/₹([\d.]+)/);
          return match ? parseFloat(match[1]) : 0;
        };
        return getFeesValue(a.fees_range) - getFeesValue(b.fees_range);
      default:
        return 0;
    }
  });

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p className="loading-text">Discovering Kerala's finest institutions...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-box">
          <h2 className="error-title">⚠️ Connection Error</h2>
          <p className="error-text">{error}</p>
          <div className="error-details">
            <p><strong>Troubleshooting:</strong></p>
            <ul>
              <li>Ensure backend is running on port 5000</li>
              <li>Check MongoDB connection</li>
              <li>Run: <code>python populate_kerala_colleges.py</code></li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <h1 className="title">Kerala College Finder</h1>
          <p className="subtitle">Discover 60+ premier institutions across Kerala's 14 districts</p>
        </div>
      </header>

      {/* Filters Section */}
      <div className="filters-section">
        <div className="filters-container">
          {/* Primary Filters */}
          <div className="primary-filters">
            {/* Course Filter - MOST IMPORTANT */}
            <div className="filter-group">
              <label className="filter-label">
                <span className="label-icon">🎓</span>
                Course
              </label>
              <select 
                className="filter-select"
                value={selectedCourse}
                onChange={(e) => setSelectedCourse(e.target.value)}
              >
                <option value="all">All Courses</option>
                {courses.slice(1).map(course => (
                  <option key={course} value={course}>{course}</option>
                ))}
              </select>
            </div>

            {/* District Filter */}
            <div className="filter-group">
              <label className="filter-label">
                <span className="label-icon">📍</span>
                District
              </label>
              <select 
                className="filter-select"
                value={selectedDistrict}
                onChange={(e) => setSelectedDistrict(e.target.value)}
              >
                <option value="all">All Districts</option>
                {districts.slice(1).map(district => (
                  <option key={district} value={district}>{district}</option>
                ))}
              </select>
            </div>

            {/* Type Filter */}
            <div className="filter-group">
              <label className="filter-label">
                <span className="label-icon">🏛️</span>
                Type
              </label>
              <select 
                className="filter-select"
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
              >
                <option value="all">All Types</option>
                {types.slice(1).map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Secondary Controls */}
          <div className="secondary-controls">
            {/* Search */}
            <div className="search-box">
              <span className="search-icon">🔍</span>
              <input
                type="text"
                placeholder="Search colleges, specializations..."
                className="search-input"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>

            {/* Sort */}
            <div className="sort-group">
              <label className="sort-label">Sort by:</label>
              <select 
                className="sort-select"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
              >
                <option value="rating">Rating</option>
                <option value="name">Name</option>
                <option value="fees">Fees</option>
              </select>
            </div>

            {/* View Toggle */}
            <div className="view-toggle">
              <button
                className={`view-button ${viewMode === 'grid' ? 'active' : ''}`}
                onClick={() => setViewMode('grid')}
                title="Grid View"
              >
                ⊞
              </button>
              <button
                className={`view-button ${viewMode === 'list' ? 'active' : ''}`}
                onClick={() => setViewMode('list')}
                title="List View"
              >
                ☰
              </button>
            </div>
          </div>
        </div>

        {/* Results Count */}
        <div className="results-bar">
          <p className="results-text">
            Found <strong>{sortedColleges.length}</strong> colleges
            {selectedCourse !== 'all' && ` offering ${selectedCourse}`}
            {selectedDistrict !== 'all' && ` in ${selectedDistrict}`}
          </p>
          {(selectedCourse !== 'all' || selectedDistrict !== 'all' || selectedType !== 'all' || searchQuery) && (
            <button 
              className="clear-button"
              onClick={() => {
                setSelectedCourse('all');
                setSelectedDistrict('all');
                setSelectedType('all');
                setSearchQuery('');
              }}
            >
              Clear Filters
            </button>
          )}
        </div>
      </div>

      {/* Colleges Grid/List */}
      {sortedColleges.length === 0 ? (
        <div className="no-results">
          <div className="no-results-content">
            <span className="no-results-icon">🔍</span>
            <h3 className="no-results-title">No colleges found</h3>
            <p className="no-results-text">Try adjusting your filters or search terms</p>
          </div>
        </div>
      ) : (
        <div className={viewMode === 'grid' ? 'colleges-grid' : 'colleges-list'}>
          {sortedColleges.map((college, index) => (
            <CollegeCard 
              key={index} 
              college={college} 
              viewMode={viewMode}
              animationDelay={index * 0.05}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function CollegeCard({ college, viewMode, animationDelay }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div 
      className={`college-card ${viewMode === 'list' ? 'list-view' : ''}`}
      style={{ animationDelay: `${animationDelay}s` }}
    >
      {/* Header */}
      <div className="card-header">
        <div className="card-header-top">
          <h3 className="college-name">{college.name}</h3>
          <div className="rating-badge">
            <span className="rating-stars">⭐</span>
            <span className="rating-value">{college.rating}</span>
          </div>
        </div>
        <p className="college-location">
          <span className="location-icon">📍</span>
          {college.location}
        </p>
      </div>

      {/* Tags */}
      <div className="tags">
        <span className="tag">{college.type}</span>
        <span className="tag">{college.primary_course}</span>
        {college.established && (
          <span className="tag-secondary">Est. {college.established}</span>
        )}
      </div>

      {/* Info Grid */}
      <div className="info-grid">
        <div className="info-item">
          <span className="info-label">Affiliation</span>
          <span className="info-value">{college.affiliation}</span>
        </div>
        <div className="info-item">
          <span className="info-label">Fees Range</span>
          <span className="info-value">{college.fees_range}</span>
        </div>
        <div className="info-item">
          <span className="info-label">Admission</span>
          <span className="info-value">{college.admission_criteria}</span>
        </div>
        {college.placements && (
          <div className="info-item">
            <span className="info-label">Avg. Placement</span>
            <span className="info-value">{college.placements.average}</span>
          </div>
        )}
      </div>

      {/* Expandable Details */}
      {expanded && (
        <div className="expanded-content">
          {/* Specializations */}
          {college.specializations && college.specializations.length > 0 && (
            <div className="detail-section">
              <h4 className="detail-title">Specializations</h4>
              <div className="specializations-list">
                {college.specializations.map((spec, idx) => (
                  <span key={idx} className="specialization-chip">{spec}</span>
                ))}
              </div>
            </div>
          )}

          {/* Facilities */}
          {college.facilities && college.facilities.length > 0 && (
            <div className="detail-section">
              <h4 className="detail-title">Facilities</h4>
              <div className="facilities-list">
                {college.facilities.map((facility, idx) => (
                  <span key={idx} className="facility-item">✓ {facility}</span>
                ))}
              </div>
            </div>
          )}

          {/* Contact */}
          <div className="contact-section">
            {college.website && (
              <a 
                href={`https://${college.website}`} 
                className="contact-link" 
                target="_blank" 
                rel="noopener noreferrer"
              >
                🌐 Website
              </a>
            )}
            {college.contact && (
              <a href={`tel:${college.contact}`} className="contact-link">
                📞 {college.contact}
              </a>
            )}
          </div>
        </div>
      )}

      {/* Expand Button */}
      <button 
        className="expand-button"
        onClick={() => setExpanded(!expanded)}
      >
        {expanded ? '△ Show Less' : '▽ Show More'}
      </button>
    </div>
  );
}

export default CollegeFinder;