import React, { useState, useEffect } from 'react';
import axios from 'axios';

function CollegeFinder() {
  const [colleges, setColleges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchColleges = async () => {
      try {
        const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
        console.log('Fetching from:', `${API_URL}/colleges`);
        
        const response = await axios.get(`${API_URL}/colleges`);
        console.log('Received data:', response.data);
        
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

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger">
          <h4>Error loading colleges</h4>
          <p>{error}</p>
          <hr />
          <p className="mb-0">
            Make sure:
            <ul>
              <li>Backend is running on port 5000</li>
              <li>MongoDB is running</li>
              <li>Database has colleges (run populate script)</li>
            </ul>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <h1 className="mb-4">🏫 Kerala College Finder</h1>
      
      {colleges.length === 0 ? (
        <div className="alert alert-warning">
          <h4>No colleges found</h4>
          <p>Run: <code>python populate_kerala_colleges.py</code></p>
        </div>
      ) : (
        <div className="row">
          {colleges.map((college, index) => (
            <div key={index} className="col-md-6 mb-3">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">{college.name}</h5>
                  <p className="text-muted">{college.location}</p>
                  <p className="mb-1">
                    <strong>Type:</strong> {college.type}
                  </p>
                  <p className="mb-1">
                    <strong>Rating:</strong> ⭐ {college.rating}
                  </p>
                  <p className="mb-1">
                    <strong>Fees:</strong> {college.fees_range}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      
      <div className="alert alert-info mt-4">
        <strong>Total Colleges:</strong> {colleges.length}
      </div>
    </div>
  );
}

export default CollegeFinder;